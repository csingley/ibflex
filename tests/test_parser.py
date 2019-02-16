# coding: utf-8
""" Unit tests for ibflex.parser module """
# stdlib imports
import unittest
from unittest.mock import Mock, patch, call, sentinel
import xml.etree.ElementTree as ET


# local imports
from ibflex import fields, schemata, parser


class FlexParserTestCase(unittest.TestCase):
    # @patch('xml.etree.ElementTree.ElementTree')
    # @patch('parser.parse_response')
    # def testParse(self, mock_etree, mock_parse_response_method):
        # instance = mock_etree.return_value
        # instance.parse.return_value = 'FOO'
        # parser.parse('foo')
        # print(mock_etree.mock_calls)
        # print(instance.parse.mock_calls)

    @patch('ibflex.parser.parse_stmts')
    def testParseResponse(self, mock_parse_stmts):
        data = ET.Element('FlexQueryResponse', {'queryName': 'Test', 'type': ''})
        ET.SubElement(data, 'FlexStatements', {'count': '1'})
        output = parser.parse_response(data)

        self.assertEqual(mock_parse_stmts.mock_calls,
                         [call.convert(e) for e in data])

        self.assertIsInstance(output, dict)
        self.assertEqual(len(output), 3)
        self.assertEqual(output['queryName'], 'Test')
        self.assertEqual(output['type'], None)
        self.assertIn('FlexStatements', output)

    def testParseResponseNoFlexStatements(self):
        data = ET.Element('FlexQueryResponse', {'queryName': 'Test', 'type': ''})
        with self.assertRaises(parser.FlexParserError):
            parser.parse_response(data)

    def testParseResponseTooManyFlexStatements(self):
        data = ET.Element('FlexQueryResponse', {'queryName': 'Test', 'type': ''})
        ET.SubElement(data, 'FlexStatements', {'count': '1'})
        ET.SubElement(data, 'FlexStatements', {'count': '1'})
        with self.assertRaises(parser.FlexParserError):
            parser.parse_response(data)

    @patch('ibflex.parser.parse_stmt')
    def testParseStmts(self, mock_parse_stmt_method):
        data = ET.Element('FlexStatements', {'count': '2'})
        ET.SubElement(data, 'FlexStatement')
        ET.SubElement(data, 'FlexStatement')
        output = parser.parse_stmts(data)

        self.assertEqual(mock_parse_stmt_method.mock_calls,
                         [call(e) for e in data])

        self.assertIsInstance(output, list)
        self.assertEqual(len(output), 2)

    def testParseStmt(self):
        pass

    # @patch('ibflex.parser.parse_acctinfo')
    # def testParseStmtChild(self, mock_parse_acctinfo):
        # """
        # parse_stmt_child() looks up the Element.tag in stmt_child_parsers,
        # passes the Element to the looked-up parser, and returns the result.
        # """
        # element = ET.Element('AccountInformation')
        # output = parser.parse_stmt_child(element)
        # print(output)

    @patch.object(schemata.AccountInformation, 'convert', return_value=sentinel.dict)
    def testParseAcctInfo(self, mock_convert_method):
        output = parser.parse_acctinfo(sentinel.elem)

        self.assertEqual(mock_convert_method.mock_calls, [call(sentinel.elem)])

        self.assertIsInstance(output, tuple)
        self.assertEqual(len(output), 2)
        tag, conversion = output
        self.assertEqual(tag, 'AccountInformation')
        self.assertIs(conversion, sentinel.dict)

    @patch('ibflex.parser.parse_rate', wraps=lambda rate: (rate, None))
    def testParseRates(self, mock_parse_rate_method):
        """
        parse_rates() passes each child of input element to parse_rate,
        and collects the returned values into a dict.
        """
        elem = [sentinel.rate1, sentinel.rate2]
        output = parser.parse_rates(elem)

        self.assertEqual(mock_parse_rate_method.mock_calls,
                         [call(sentinel.rate1), call(sentinel.rate2)])

        self.assertIsInstance(output, tuple)
        self.assertEqual(len(output), 2)
        tag, conversion = output
        self.assertEqual(tag, 'ConversionRates')
        self.assertIsInstance(conversion, dict)
        self.assertEqual(len(conversion), 2)
        self.assertIn(sentinel.rate1, conversion)
        self.assertIn(sentinel.rate2, conversion)

    @patch.object(schemata.ConversionRate, 'convert',
                  return_value={'fromCurrency': sentinel.fromCurrency,
                                'toCurrency': sentinel.toCurrency,
                                'reportDate': sentinel.reportDate,
                                'rate': sentinel.rate})
    def testParseRate(self, mock_convert_method):
        output = parser.parse_rate(sentinel.elem)

        self.assertEqual(mock_convert_method.mock_calls, [call(sentinel.elem)])

        self.assertIsInstance(output, tuple)
        self.assertEqual(len(output), 2)
        key, rate = output

        self.assertIsInstance(key, tuple)
        self.assertEqual(len(key), 3)
        fromCurrency, toCurrency, reportDate = key
        self.assertIs(fromCurrency, sentinel.fromCurrency)
        self.assertIs(toCurrency, sentinel.toCurrency)
        self.assertIs(reportDate, sentinel.reportDate)

        self.assertIs(rate, sentinel.rate)

    @patch('ibflex.parser.parse_list', return_value=(None, sentinel.fxLots))
    def testParseFxpos(self, mock_parse_list_method):
        elem = ET.Element('DoesNotMatter')
        subelem = ET.SubElement(elem, 'FxLots')
        output = parser.parse_fxpos(elem)

        self.assertEqual(mock_parse_list_method.mock_calls, [call(subelem)])

        self.assertIsInstance(output, tuple)
        self.assertEqual(len(output), 2)
        tag, items = output
        self.assertEqual(tag, 'FxPositions')
        self.assertIs(items, sentinel.fxLots)

    def testParseFxposEmptyContainer(self):
        elem = ET.Element('DoesNotMatter')
        output = parser.parse_fxpos(elem)
        self.assertIsInstance(output, tuple)
        self.assertEqual(len(output), 2)
        tag, items = output
        self.assertEqual(tag, 'FxPositions')
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    def testParseFxposTooManyChildren(self):
        elem = ET.Element('DoesNotMatter')
        ET.SubElement(elem, 'AlsoDoesNotMatter')
        ET.SubElement(elem, 'StillDoesNotMatter')
        with self.assertRaises(parser.FlexParserError):
            parser.parse_fxpos(elem)

    def testParseFxposChildTagIsNotFxlots(self):
        elem = ET.Element('DoesNotMatter')
        ET.SubElement(elem, 'NotFxLots')
        with self.assertRaises(parser.FlexParserError):
            parser.parse_fxpos(elem)

    @patch.dict('ibflex.schemata.elementSchemata', {'List': Mock(name='MockSchema')}, clear=True)
    def testParseList(self):
        """
        parser.parse_list() looks up item schema by list tag
        and calls schema.convert() on each item
        """
        data = ET.Element('List')
        ET.SubElement(data, 'Item', {'foo': 'hello', 'bar': '1', 'baz': 'Y'})
        ET.SubElement(data, 'Item', {'foo': 'hi', 'bar': '2', 'baz': 'N'})
        output = parser.parse_list(data)
        self.assertEqual(len(output), 2)
        tag, items = output
        self.assertIsInstance(tag, str)
        self.assertEqual(tag, 'List')
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

        mockSchema = schemata.elementSchemata['List']
        self.assertEqual(mockSchema.mock_calls, [call.convert(data[0]),
                                                 call.convert(data[1])])

    def testParseListUnknownTag(self):
        unknownTag = 'List'
        self.assertNotIn(unknownTag, schemata.elementSchemata)
        data = ET.Element(unknownTag)
        ET.SubElement(data, 'Item', {'foo': 'hello', 'bar': '1', 'baz': 'Y'})
        with self.assertRaises(parser.FlexParserError):
            parser.parse_list(data)

    def testStmtChildParsers(self):
        self.assertEqual(parser.stmt_child_parsers['AccountInformation'],
                         parser.parse_acctinfo)
        self.assertEqual(parser.stmt_child_parsers['ConversionRates'],
                         parser.parse_rates)
        self.assertEqual(parser.stmt_child_parsers['FxPositions'],
                         parser.parse_fxpos)


if __name__ == '__main__':
    unittest.main(verbosity=3)
