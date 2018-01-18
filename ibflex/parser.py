# coding: utf-8
"""
"""
# stdlib imports
import xml.etree.ElementTree as ET


# local imports
from ibflex import schemata
from ibflex.schemata import elementSchemata


class FlexQueryResponse(object):
    """ Simple container for parsed <FlexQueryResponse> data """
    def __init__(self, queryName, type):
        self.queryName = queryName
        self.type = type

    def __repr__(self):
        return ('FlexQueryResponse(queryName={}, type={}, '
                'len(flexStatements)={})').format(repr(self.queryName),
                                                  repr(self.type),
                                                  len(self.flexStatements))


class FlexStatement(object):
    """ Simple container for parsed <FlexStatement> data """
    def __init__(self, accountId, fromDate, toDate, period, whenGenerated):
        self.accountId = accountId
        self.fromDate = fromDate
        self.toDate = toDate
        self.period = period
        self.whenGenerated = whenGenerated

    def __repr__(self):
        rep = ('FlexStatement(accountId={}, fromDate={}, toDate={}, '
               'period={}, whenGenerated={}')
        rep_vals = [repr(self.accountId), repr(self.fromDate),
                    repr(self.toDate), repr(self.period),
                    repr(self.whenGenerated)]
        
        init_args = ['accountId', 'fromDate', 'toDate', 'period',
                     'whenGenerated']
        lists = [(attr, getattr(self, attr)) for attr in dir(self)
                 if attr not in init_args
                 and not attr.startswith('_')
                 and len(getattr(self, attr)) > 0]
        for attr, list_ in lists:
            rep += ', len(' + attr + ')={}'
            rep_vals.append(len(list_))

        rep += ')'
        return rep.format(*rep_vals)


class FlexResponseParser(object):
    def __init__(self, source):
        self.source = source
        self.statements = []

    def parse(self):
        tree = ET.ElementTree()
        tree.parse(self.source)
        root = tree.getroot()
        response = schemata.FlexQueryResponse.convert(root)

        flexStmts = root.findall('FlexStatements')
        if len(flexStmts) != 1:
            msg = ("FlexQueryResponse must contain exactly 1 FlexStatements, "
                   "not {}")
            raise ValueError(msg.format(len(flexStmts)))
        flexStmts = flexStmts[0]
        flexStmts_attrs = schemata.FlexStatements.convert(flexStmts)
        count = flexStmts_attrs['count']
        flexStmt = flexStmts.findall('FlexStatement')
        if len(flexStmt) != count:
            msg = ("FlexStatements declares count={} "
                   "but contains {} FlexStatement elements")
            raise ValueError(msg.format(count, len(flexStmt)))

        response['FlexStatements'] = [self.parse_stmt(stmt) for stmt in flexStmt]
        return response

    def parse_stmt(self, elem):
        stmt = schemata.FlexStatement.convert(elem)
        for child in elem:
            if child.tag == 'AccountInformation':
                acctinfo = schemata.AccountInformation.convert(elem)
                stmt['AccountInformation'] = acctinfo
            elif child.tag == 'ConversionRates':
                # IB ConversionRates are always forex to account base currency
                # Store as dict keyed by (currency, date)
                schema = schemata.ConversionRate()
                baseCurrency = stmt['AccountInformation']['currency']

                stmt['ConversionRates'] = {self.parse_rate(schema, elem, baseCurrency) for elem in child}
            elif child.tag == 'FxPositions':
                # FxPositions contains FxLots list; maybe more?
                for grandchild in child:
                    attrName, items = self.parse_list(grandchild)
                    stmt[attrName] = items
            else:
                # All other children of FlexStatement should be lists
                attrName, items = self.parse_list(child)
                stmt[attrName] = items
        return stmt

    @staticmethod
    def parse_rate(schema, elem, baseCurrency):
        rate = schema.convert(elem)
        return (rate['fromCurrency'], rate['reportDate']), rate['rate']

    def parse_list(self, elem):
        tag = elem.tag
        try:
            schema = elementSchemata[tag]
        except KeyError:
            raise  # FIXME
        items = [schema.convert(item) for item in elem]
        return tag, items


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
