# coding: utf-8
""" Unit tests for ibflex.fieldutils module """
# stdlib imports
import unittest


# local imports
from ibflex import fieldutils


class ParseIsoDateTestCase(unittest.TestCase):
    parser = staticmethod(fieldutils.parse_isodate)
    goodDate = ("2011-01-02", (2011, 1, 2))
    badLength = ["20111-01-02", "2011-011-02", "2011-01-022"]
    badMonth = ["2011-00-02", "2011-13-02"]
    badDay = ["2011-01-00", "2011-01-32"]
    badSep = ["01-02-2011", "2011/01/02"]

    def testGoodDate(self):
        input, expected = self.goodDate
        output = self.parser(input, False)
        self.assertEqual(output, expected)

    def testBadLength(self):
        for badDate in self.badLength:
            with self.assertRaises(fieldutils.FlexFieldError):
                self.parser(badDate, False)

    def testBadMonth(self):
        for badDate in self.badMonth:
            with self.assertRaises(fieldutils.FlexFieldError):
                self.parser(badDate, False)

    def testBadDay(self):
        for badDate in self.badDay:
            with self.assertRaises(fieldutils.FlexFieldError):
                self.parser(badDate, False)

    def testBadSep(self):
        for badDate in self.badSep:
            with self.assertRaises(fieldutils.FlexFieldError):
                self.parser(badDate, False)

    def testDayFirst(self):
        # dayFirst arg should be ignored
        input, expected = self.goodDate
        self.assertEqual(self.parser(input, False), self.parser(input, True))


class ParseYYYYmmddTestCase(ParseIsoDateTestCase):
    parser = staticmethod(fieldutils.parse_YYYYmmdd)
    goodDate = ("20110102", (2011, 1, 2))
    badLength = ["201101020", "2011010"]
    badMonth = ["20110002", "20111302"]
    badDay = ["20110100", "20110132"]
    badSep = ["2011-01-02", ]


class ParseMmddYYYYTestCase(ParseIsoDateTestCase):
    parser = staticmethod(fieldutils.parse_mmddYYYY)
    goodDate = ("01/02/2011", (2011, 1, 2))
    badLength = ["01/02/20111", "01/022/2011", "011/02/2011"]
    badMonth = ["00/02/2011", "13/02/2011"]
    badDay = ["01/00/2011", "01/32/2011"]
    badSep = ["01-02-2011", "2011/01/02"]

    def testDayFirst(self):
        self.assertEqual(self.parser("01/02/2011", True), (2011, 2, 1))


class ParseMmddyyTestCase(ParseIsoDateTestCase):
    parser = staticmethod(fieldutils.parse_mmddyy)
    goodDate = ("01/02/11", (2011, 1, 2))
    badLength = ["01/02/111", "01/022/11", "011/02/11"]
    badMonth = ["00/02/11", "13/02/11"]
    badDay = ["01/00/11", "01/32/11"]
    badSep = ["01-02-11", ]

    def testDayFirst(self):
        self.assertEqual(self.parser("01/02/11", True), (2011, 2, 1))


class ParseDdbbbyyTestCase(ParseIsoDateTestCase):
    parser = staticmethod(fieldutils.parse_ddbbbyy)
    goodDate = ("02-JAN-11", (2011, 1, 2))
    badLength = ["02-JAN-111", "022-JAN-111"]
    badMonth = ["02-FOO-11", ]
    badDay = ["00-JAN-11", "32-JAN-11"]
    badSep = ["02/JAN/11", ]


class DateParsersTestCase(unittest.TestCase):
    parsers = [("2011-01-02", fieldutils.parse_isodate),
               ("20110102", fieldutils.parse_YYYYmmdd),
               ("01/02/2011", fieldutils.parse_mmddYYYY),
               ("01/02/11", fieldutils.parse_mmddyy),
               ("02-JAN-11", fieldutils.parse_ddbbbyy), ]

    def testDateParsers(self):
        for value, parser in self.parsers:
            length = len(value)
            slashes = value.count('/')
            self.assertEqual(fieldutils.date_parsers[length][slashes], parser)


class CurrencyCodesTestCase(unittest.TestCase):
    def testISO4217(self):
        self.assertEqual(len(fieldutils.ISO4217), 179)
        for currency in fieldutils.ISO4217:
            self.assertIsInstance(currency, str)
            self.assertEqual(len(currency), 3)

    def testCurrencyCodes(self):
        self.assertEqual(len(fieldutils.CURRENCY_CODES),
                         len(fieldutils.ISO4217)+2)
        self.assertIn('CNH', fieldutils.CURRENCY_CODES)
        self.assertIn('BASE_SUMMARY', fieldutils.CURRENCY_CODES)


if __name__ == '__main__':
    unittest.main(verbosity=3)
