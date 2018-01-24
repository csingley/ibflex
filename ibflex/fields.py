# coding: utf-8
""" Type converters / validators for Interactive Brokers Flex XML data """

# stdlib imports
import sys
import decimal
import datetime


# local imports
from ibflex import fieldutils
from ibflex.fieldutils import FlexFieldError


PYVERSION = sys.version_info[0]


# We want Py3K string behavior (everything is unicode) but to remain portable
# we'll retain Py2K semantics
if PYVERSION > 2:
    unicode = str


class Field(object):
    """
    Base type convertor/validator class.

    Pass validation parameters to __init__() as args/kwargs
    when defining a Schema subclass.
    """
    def __init__(self, *args, **kwargs):
        self.required = kwargs.pop('required', False)
        args, kwargs = self._init(*args, **kwargs)
        if args or kwargs:
            raise FlexFieldError("Unknown args for '%s'- args: %r; kwargs: %r"
                                 % (self.__class__.__name__, args, kwargs))

    def _init(self, *args, **kwargs):
        """ Define in subclass """
        return args, kwargs

    def convert(self, value):
        """
        Convert empty strings to None and enforce ``required`` parameter
        """
        if value == '':
            value = None
        if value is None:
            if self.required:
                raise FlexFieldError("Value is required")
            else:
                return None
        return self._convert(value)

    def _convert(self, value):
        """ Define in subclass """
        raise NotImplementedError

    def __repr__(self):
        repr = "<{}(required={})>"
        return repr.format(self.__class__.__name__, self.required)


class String(Field):
    def _convert(self, value):
        return unicode(value)


class Integer(Field):
    def _convert(self, value):
        try:
            return int(value)
        except ValueError:
            msg = "{} can't be converted to an integer"
            raise FlexFieldError(msg.format(value))


class Boolean(Field):
    """ IB sends 'Y'/'N' for True/False """
    mapping = {'Y': True, 'N': False}

    def _convert(self, value):
        try:
            return self.mapping[value]
        except KeyError as err:
            msg = "{} is not one of the allowed values {}"
            raise FlexFieldError(msg.format(err.args[0], self.mapping.keys()))


class Decimal(Field):
    """ IB writes numbers with comma separators """
    def _convert(self, value):
        try:
            return decimal.Decimal(value.replace(',', ''))
        except decimal.InvalidOperation:
            msg = "Can't convert {} to Decimal"
            raise FlexFieldError(msg.format(value))


class OneOf(Field):
    def _init(self, *args, **kwargs):
        # args are sequence of valid values
        self.valid = set(args)
        return (), kwargs

    def _convert(self, value):
        if value in self.valid:
            return value
        raise FlexFieldError("'%s' is not OneOf %r" % (value, self.valid))


class List(Field):
    """
    IB sends lists as comma- or string-delimited strings.
    """
    separator = ','

    def _init(self, *args, **kwargs):
        # If present, `separator` kwarg overrides default separator (the comma)
        separator = kwargs.pop('separator', None)
        if separator:
            self.separator = separator
        # If present, `valid` kwarg is sequence of valid values
        self.valid = kwargs.pop('valid', None)
        return args, kwargs

    def convert(self, value):
        """
        Convert empty string to empty list and enforce ``required`` parameter
        """
        if value in ('', None):
            value = []
        if value == []:
            if self.required:
                raise FlexFieldError("Value is required")
            else:
                return value 
        return self._convert(value)

    def _convert(self, value):
        values = [v.strip() for v in value.split(self.separator)]
        if self.valid:
            for val in values:
                if val not in self.valid:
                    msg = "{} is not one of the valid values: {}"
                    raise FlexFieldError(msg.format(val, self.valid))
        return values

    def __repr__(self):
        repr = "<{}({}, required={})>"
        return repr.format(self.__class__.__name__, ','.join(self.valid),
                           self.required)


class Date(Field):
    """
    Format-agnostic date string.

    We can't easily distinguish between e.g. MM/dd/yyyy and dd/MM/yyyy,
    so this is configured by setting the ``dayfirst`` class attribute,
    which by default is American style (MM/dd) not Euro style (dd/MM).

    Seriously though, just configure Flex queries for ISO format (YYYY-MM-dd).
    """
    dayfirst = False

    @classmethod
    def parse(cls, value):
        parser = fieldutils.date_parsers[len(value)][value.count('/')]
        return parser(value, cls.dayfirst)

    def _convert(self, value):
        return datetime.date(*self.parse(value))


class EuroDate(Date):
    """
    Format-agnostic date string, using Euro style dd/MM date formats.

    This isn't used in any Schema; it's just for testing.
    """
    dayfirst = True


def first_hit(make_parser, separators, value):
    """
    Feed each of the given separators to make_parser(); use the resulting
    function to parse() the given value.  Return the first valid result.
    """
    value = value or None
    if value is not None:
        valid = False
        for sep in separators:
            try:
                value = make_parser(sep)(value)
                valid = True
                break
            except:
                pass
        if not valid:
            msg = "{} can't be parsed by any of the separators: {}"
            raise FlexFieldError(msg.format(value, separators))
    return value


class Time(Field):
    """
    Format-agnostic time string.
    """
    separators = [':', '']

    @staticmethod
    def make_parser(separator):
        """
        Factory returning a function that splits input string according to the
        given separator, and returns a series of integers
        (hour, minute, second)
        """
        if separator == '':
            def parse(value):
                if len(value) != 6:
                    msg = "{} can't be parsed as a time".format(value)
                    raise FlexFieldError(msg)
                hours = value[:2]
                minutes = value[2:4]
                seconds = value[4:]
                return int(hours), int(minutes), int(seconds)
        else:
            def parse(value):
                if value.count(separator) != 2:
                    msg = "{} can't be parsed as a time".format(value)
                    raise FlexFieldError(msg)
                hours, minutes, seconds = value.split(separator)
                if not (len(hours) == len(minutes) == len(seconds) == 2):
                    msg = "{} can't be parsed as a time".format(value)
                    raise FlexFieldError(msg)
                return int(hours), int(minutes), int(seconds)
        return parse

    @classmethod
    def parse(cls, value):
        return first_hit(cls.make_parser, cls.separators, value)

    def _convert(self, value):
        return datetime.time(*self.parse(value))


class DateTime(Field):
    """
    Format-agnostic datetime string.
    """
    separators = [';', ',', ' ', '']
    dateField = Date

    @classmethod
    def make_parser(cls, separator):
        """
        Factory returning a function that splits input string into date & time
        according to the given separator, and returns a series of integers
        (year, month, day, hour, minute, second)
        """
        if separator == '':
            def parse(value):
                for sep in Time.separators:
                    try:
                        parse_time = Time.make_parser(sep)
                        timeLength = 6 + 2*len(sep)
                        time = value[-timeLength:]
                        time = parse_time(time)
                        date = value[:-timeLength]
                        return cls.dateField.parse(date) + time
                    except:
                        continue
                msg = "{} can't be parsed as a datetime".format(value)
                raise FlexFieldError(msg)
        else:
            def parse(value):
                if value.count(separator) != 1:
                    msg = "{} can't be parsed as a datetime".format(value)
                    raise FlexFieldError(msg)
                date, time = value.split(separator)
                return cls.dateField.parse(date) + Time.parse(time)
        return parse

    def _convert(self, value):
        if len(value) < 12:
            # Just a date, with no time info
            return datetime.datetime(*self.dateField.parse(value))
        else:
            return datetime.datetime(*first_hit(self.make_parser, self.separators, value))


class EuroDateTime(DateTime):
    """
    Format-agnostic datetime string, using Euro style dd/MM date formats.

    This isn't used in any Schema; it's just for testing.
    """
    dateField = EuroDate
