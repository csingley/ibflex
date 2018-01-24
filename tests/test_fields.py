# coding: utf-8
""" Unit tests for ibflex.fields module """
# stdlib imports
import unittest
from decimal import Decimal
from datetime import date, time, datetime


# local imports
from ibflex import fields


class FieldTestCase(unittest.TestCase):
    field = fields.Field
    values = []
    badValues = []

    def testExtraArgs(self):
        with self.assertRaises(fields.FlexFieldError):
            self.field('foo')

    def testExtraKwargs(self):
        with self.assertRaises(fields.FlexFieldError):
            self.field(foo='bar')

    def testRequired(self):
        instance = self.field(required=True)
        with self.assertRaises(fields.FlexFieldError):
            instance.convert(None)

    def testNotRequired(self):
        instance = self.field(required=False)
        self.assertEqual(instance.convert(None), None)

    def testConvertEmptyString(self):
        instance = self.field(required=False)
        self.assertEqual(instance.convert(''), None)

    def testConvert(self):
        instance = self.field()
        for value, expected in self.values:
            self.assertEqual(instance.convert(value), expected)

    def testConvertBad(self):
        instance = self.field()
        for value in self.badValues:
            with self.assertRaises(fields.FlexFieldError):
                instance.convert(value)


class StringTestCase(FieldTestCase):
    field = fields.String
    values = [('foo', 'foo'), (1, '1')]


class IntegerTestCase(FieldTestCase):
    field = fields.Integer
    values = [('01', 1), (1, 1), ]
    badValues = ['foo', ]


class BooleanTestCase(FieldTestCase):
    field = fields.Boolean
    values = [('Y', True), ('N', False)]
    badValues = ['y', 'n', True, False, 1, 0]


class DecimalTestCase(FieldTestCase):
    field = fields.Decimal
    values = [('-1234.56', Decimal('-1234.56')),
              ('1,234.56', Decimal('1234.56')), ]
    badValues = ['foo', '192.168.1.100']

    def testExtraArgs(self):
        with self.assertRaises(fields.FlexFieldError):
            self.field(2, 4)

    def testBadArgs(self):
        with self.assertRaises(fields.FlexFieldError):
            self.field('foo')


class OneOfTestCase(FieldTestCase):
    field = fields.OneOf
    valid = ('foo', 'bar', '1')
    values = [('foo', 'foo'), ('bar', 'bar'), ('1', '1')]
    badValues = ['baz', 1, 0]

    def testExtraArgs(self):
        # Doesn't apply to OneOf.__init__(), which accepts unlimited args
        pass

    def testRequired(self):
        instance = self.field(*self.valid, required=True)
        with self.assertRaises(fields.FlexFieldError):
            instance.convert(None)

    def testNotRequired(self):
        instance = self.field(*self.valid, required=False)
        self.assertEqual(instance.convert(None), None)

    def testConvertEmptyString(self):
        instance = self.field(*self.valid, required=False)
        self.assertEqual(instance.convert(''), None)

    def testConvert(self):
        instance = self.field(*self.valid)
        for value, expected in self.values:
            self.assertEqual(instance.convert(value), expected)

    def testConvertBad(self):
        instance = self.field(*self.valid)
        for value in self.badValues:
            with self.assertRaises(fields.FlexFieldError):
                instance.convert(value)


class ListTestCase(FieldTestCase):
    field = fields.List
    values = [('foo, bar,1,2', ['foo', 'bar', '1', '2']), ('foo', ['foo'])]
    badValue = ['Foo,bar,1,2', ]

    def testExtraArgs(self):
        with self.assertRaises(fields.FlexFieldError):
            self.field('foo')

    def testNotRequired(self):
        instance = self.field(required=False)
        self.assertEqual(instance.convert(None), [])

    def testConvertEmptyString(self):
        instance = self.field(required=False)
        self.assertEqual(instance.convert(''), [])

    def testValid(self):
        instance = self.field(valid=['foo', 'bar'])
        self.assertEqual(instance.convert('bar,foo'), ['bar', 'foo'])
        with self.assertRaises(fields.FlexFieldError):
            instance.convert('foo,bar, baz')

    def testSeparator(self):
        instance = self.field(separator=';')
        self.assertEqual(instance.convert('foo;bar'), ['foo', 'bar'])
        self.assertEqual(instance.convert('bar,foo'), [ 'bar,foo'])


class DateTestCase(FieldTestCase):
    field = fields.Date
    values = [('2011-01-02', date(2011, 1, 2)),
              ('20110102', date(2011, 1, 2)),
              ('01/02/2011', date(2011, 1, 2)),
              ('01/02/11', date(2011, 1, 2)),
              ('02-JAN-11', date(2011, 1, 2)), ]


class EuroDateTestCase(FieldTestCase):
    field = fields.EuroDate
    values = [('2011-01-02', date(2011, 1, 2)),
              ('20110102', date(2011, 1, 2)),
              ('01/02/2011', date(2011, 2, 1)),
              ('01/02/11', date(2011, 2, 1)),
              ('02-JAN-11', date(2011, 1, 2)), ]


class TimeTestCase(FieldTestCase):
    field = fields.Time
    values = [('135645', time(13, 56, 45)),
              ('13:56:45', time(13, 56, 45)), ]


class DateTimeTestCase(FieldTestCase):
    field = fields.DateTime
    values = [('2011-01-02;135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('2011-01-02;13:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('2011-01-02,135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('2011-01-02,13:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('2011-01-02 135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('2011-01-02 13:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('2011-01-02135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('2011-01-0213:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('20110102;135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('20110102;13:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('20110102,135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('20110102,13:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('20110102 135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('20110102 13:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('20110102135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('2011010213:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('01/02/2011;135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('01/02/2011;13:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('01/02/2011,135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('01/02/2011,13:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('01/02/2011 135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('01/02/2011 13:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('01/02/2011135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('01/02/201113:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('01/02/11;135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('01/02/11;13:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('01/02/11,135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('01/02/11,13:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('01/02/11 135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('01/02/11 13:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('01/02/11135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('01/02/1113:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('02-JAN-11;135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('02-JAN-11;13:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('02-JAN-11,135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('02-JAN-11,13:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('02-JAN-11 135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('02-JAN-11 13:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('02-JAN-11135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('02-JAN-1113:56:45', datetime(2011, 1, 2, 13, 56, 45)), ]


class EuroDateTimeTestCase(FieldTestCase):
    field = fields.EuroDateTime
    values = [('2011-01-02;135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('2011-01-02;13:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('2011-01-02,135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('2011-01-02,13:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('2011-01-02 135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('2011-01-02 13:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('2011-01-02135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('2011-01-0213:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('20110102;135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('20110102;13:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('20110102,135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('20110102,13:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('20110102 135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('20110102 13:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('20110102135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('2011010213:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('01/02/2011;135645', datetime(2011, 2, 1, 13, 56, 45)),
              ('01/02/2011;13:56:45', datetime(2011, 2, 1, 13, 56, 45)),
              ('01/02/2011,135645', datetime(2011, 2, 1, 13, 56, 45)),
              ('01/02/2011,13:56:45', datetime(2011, 2, 1, 13, 56, 45)),
              ('01/02/2011 135645', datetime(2011, 2, 1, 13, 56, 45)),
              ('01/02/2011 13:56:45', datetime(2011, 2, 1, 13, 56, 45)),
              ('01/02/2011135645', datetime(2011, 2, 1, 13, 56, 45)),
              ('01/02/201113:56:45', datetime(2011, 2, 1, 13, 56, 45)),
              ('01/02/11;135645', datetime(2011, 2, 1, 13, 56, 45)),
              ('01/02/11;13:56:45', datetime(2011, 2, 1, 13, 56, 45)),
              ('01/02/11,135645', datetime(2011, 2, 1, 13, 56, 45)),
              ('01/02/11,13:56:45', datetime(2011, 2, 1, 13, 56, 45)),
              ('01/02/11 135645', datetime(2011, 2, 1, 13, 56, 45)),
              ('01/02/11 13:56:45', datetime(2011, 2, 1, 13, 56, 45)),
              ('01/02/11135645', datetime(2011, 2, 1, 13, 56, 45)),
              ('01/02/1113:56:45', datetime(2011, 2, 1, 13, 56, 45)),
              ('02-JAN-11;135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('02-JAN-11;13:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('02-JAN-11,135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('02-JAN-11,13:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('02-JAN-11 135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('02-JAN-11 13:56:45', datetime(2011, 1, 2, 13, 56, 45)),
              ('02-JAN-11135645', datetime(2011, 1, 2, 13, 56, 45)),
              ('02-JAN-1113:56:45', datetime(2011, 1, 2, 13, 56, 45)), ]


if __name__ == '__main__':
    unittest.main(verbosity=3)
