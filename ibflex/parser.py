# coding: utf-8
"""
Parser/type converter for data in Interactive Brokers' Flex XML format.

https://www.interactivebrokers.com/en/software/reportguide/reportguide.htm#reportguide/activity_flex_query_reference.htm
"""
# stdlib imports
import xml.etree.ElementTree as ET


# local imports
from ibflex import schemata
from ibflex.schemata import elementSchemata


class FlexParserError(Exception):
    """ Base class for errors in this module """
    pass


class FlexResponseParser(object):
    def __init__(self, source):
        self.source = source

    def parse(self):
        tree = ET.ElementTree()
        tree.parse(self.source)
        root = tree.getroot()
        return self.parse_response(root)

    @classmethod
    def parse_response(cls, elem):
        response = schemata.FlexQueryResponse.convert(elem)
        flexStmts = elem.findall('FlexStatements')

        # Sanity check
        if len(flexStmts) != 1:
            msg = ("FlexQueryResponse must contain exactly 1 FlexStatements, "
                   "not {}")
            raise FlexParserError(msg.format(len(flexStmts)))
        response['FlexStatements'] = cls.parse_stmts(flexStmts[0])

        return response

    @classmethod
    def parse_stmts(cls, elem):
        attrs = schemata.FlexStatements.convert(elem)
        count = attrs['count']
        flexStmt = elem.findall('FlexStatement')

        # Sanity check
        if len(flexStmt) != count:
            msg = ("FlexStatements declares count={} "
                   "but contains {} FlexStatement elements")
            raise FlexParserError(msg.format(count, len(flexStmt)))

        return [cls.parse_stmt(stmt) for stmt in flexStmt]

    @classmethod
    def parse_stmt(cls, elem):
        stmt = schemata.FlexStatement.convert(elem)
        children = dict([cls.parse_stmt_child(child) for child in elem])
        stmt.update(children)
        return stmt

    @classmethod
    def parse_stmt_child(cls, elem):
        parser = cls.stmt_child_parser(elem)
        return parser(elem)

    @classmethod
    def stmt_child_parser(cls, elem):
        # If the tag isn't one of the special cases defined in ``parsers``,
        # by default treat it as a list container
        parsers = {'AccountInformation': cls.parse_acctinfo,
                   'ConversionRates': cls.parse_rates,
                   'FxPositions': cls.parse_fxpos, }
        return parsers.get(elem.tag, cls.parse_list)

    @staticmethod
    def parse_acctinfo(elem):
        return 'AccountInformation', schemata.AccountInformation.convert(elem)

    @classmethod
    def parse_rates(cls, elem):
        return 'ConversionRates', dict(cls.parse_rate(rate) for rate in elem)

    @staticmethod
    def parse_rate(elem):
        """
        Use input schema to convert element.

        Return duple of ((currency, date), rate) suitable for use
        as a dict item.
        """
        rate = schemata.ConversionRate.convert(elem)
        return (rate['fromCurrency'], rate['reportDate']), rate['rate']

    @classmethod
    def parse_fxpos(cls, elem):
        if len(elem) == 0:
            items = []
        else:
            # Sanity check
            if len(elem) != 1:
                msg = "<{}> has more than 1 child: {}".format(
                    elem.tag,
                    ', '.join(["<{}>".format(child.tag) for child in elem])
                )
                raise FlexParserError(msg)
            fxLots = elem[0]
            if fxLots.tag != 'FxLots':
                msg = "<{}> can only contain <FxLots>, not <{}>"
                raise FlexParserError(msg.format(elem.tag, fxLots))

            attrName, items = cls.parse_list(fxLots)

        return 'FxPositions', items

    @staticmethod
    def parse_list(elem):
        """
        Use container tag to look up conversion schema for contained items.

        Return duple of (container tag, list of converted items).
        """
        tag = elem.tag
        try:
            schema = elementSchemata[tag]
        except KeyError:
            msg = "Don't know the schema to parse items in {}"
            raise FlexParserError(msg.format(tag))
        items = [schema.convert(item) for item in elem]
        return tag, items

    # subparsers = {'AccountInformation': parse_acctinfo,
                  # 'ConversionRates': parse_rates,
                  # 'FxPositions': parse_fxpos, }

##############################################################################
# CLI SCRIPT
###############################################################################
def main():
    from argparse import ArgumentParser

    argparser = ArgumentParser(
        description='Parse Interactive Brokers Flex XML data')
    argparser.add_argument('file', nargs='+', help='XML data file(s)')
    args = argparser.parse_args()

    for file in args.file:
        print(file)
        parser = FlexResponseParser(file)
        response = parser.parse()
        # print(response)
        for stmt in response['FlexStatements']:
            for trade in stmt['Trades']:
                print(trade)


if __name__ == '__main__':
    main()
