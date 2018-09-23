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


def parse(source):
    tree = ET.ElementTree()
    tree.parse(source)
    root = tree.getroot()
    return parse_response(root)


def parse_response(elem):
    response = schemata.FlexQueryResponse.convert(elem)
    flexStmts = elem.findall('FlexStatements')

    # Sanity check
    if len(flexStmts) != 1:
        msg = ("FlexQueryResponse must contain exactly 1 FlexStatements, "
               "not {}")
        raise FlexParserError(msg.format(len(flexStmts)))

    response['FlexStatements'] = parse_stmts(flexStmts[0])
    return response


def parse_stmts(elem):
    attrs = schemata.FlexStatements.convert(elem)
    count = attrs['count']
    flexStmt = elem.findall('FlexStatement')

    # Sanity check
    if len(flexStmt) != count:
        msg = ("FlexStatements declares count={} "
               "but contains {} FlexStatement elements")
        raise FlexParserError(msg.format(count, len(flexStmt)))

    return [parse_stmt(stmt) for stmt in flexStmt]


def parse_stmt(elem):
    stmt = schemata.FlexStatement.convert(elem)
    children = dict(parse_stmt_child(child) for child in elem)
    stmt.update(children)
    return stmt


def parse_stmt_child(elem):
    # If the tag isn't one of the special cases defined in stmt_child_parsers,
    # by default treat it as a list container
    parser = stmt_child_parsers.get(elem.tag, parse_list)
    return parser(elem)


def parse_acctinfo(elem):
    return 'AccountInformation', schemata.AccountInformation.convert(elem)


def parse_rates(elem):
    return 'ConversionRates', dict(parse_rate(rate) for rate in elem)


def parse_rate(elem):
    """
    Use input schema to convert element.

    Return duple of ((currency, date), rate) suitable for use
    as a dict item.
    """
    rate = schemata.ConversionRate.convert(elem)
    return (rate['fromCurrency'], rate['reportDate']), rate['rate']


def parse_fxpos(elem):
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

        attrName, items = parse_list(fxLots)

    return 'FxPositions', items


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


def parse_nav(elem):
    return 'ChangeInNAV', schemata.ChangeInNAV.convert(elem)


stmt_child_parsers = {'AccountInformation': parse_acctinfo,
                      'ConversionRates': parse_rates,
                      'FxPositions': parse_fxpos,
                      'ChangeInNAV': parse_nav}


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
        response = parse(file)
        # print(response)
        for stmt in response['FlexStatements']:
            for trade in stmt['Trades']:
                print(trade)


if __name__ == '__main__':
    main()
