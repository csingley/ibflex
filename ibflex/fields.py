# coding: utf-8
""" Type converters / validators for Interactive Brokers Flex XML data """

# stdlib imports
import sys
import decimal
import datetime
from xml.sax import saxutils


PYVERSION = sys.version_info[0]


# We want Py3K string behavior (everything is unicode) but to remain portable
# we'll retain Py2K semantics
if PYVERSION > 2:
    unicode = str
    basestring = str


class FlexTypeWarning(UserWarning):
    """ Base class for warnings in this module """
    pass


class Field(object):
    """
    """
    def __init__(self, *args, **kwargs):
        self.required = kwargs.pop('required', False)
        args, kwargs = self._init(*args, **kwargs)
        if args or kwargs:
            raise ValueError("Unknown args for '%s'- args: %r; kwargs: %r"
                             % (self.__class__.__name__, args, kwargs))

    def _init(self, *args, **kwargs):
        """ Define in subclass """
        return args, kwargs

    def convert(self, value):
        value = value or None
        if value is None:
            if self.required:
                raise ValueError("Value is required")
            else:
                return None
        return self._convert(value)

    def _convert(self, value):
        raise NotImplementedError

    def __repr__(self):
        repr = "<{} required={}>"
        return repr.format(self.__class__.__name__, self.required)


class Boolean(Field):
    mapping = {'Y': True, 'N': False}

    def _convert(self, value):
        # Pass through values already converted to bool
        if isinstance(value, bool):
            return value
        try:
            return self.mapping[value]
        except KeyError as e:
            raise ValueError("%s is not one of the allowed values %s" % (
                e.args[0], self.mapping.keys(), ))


class String(Field):
    def _convert(self, value):
        value = unicode(value)

        # Unescape XML control characters,
        return saxutils.unescape(value,
                                 {'&nbsp;': ' ', '&apos;': "'", '%quot;': '"'}
                                 )


class Integer(Field):
    def _convert(self, value):
        return int(value)


class Decimal(Field):
    def _init(self, *args, **kwargs):
        precision = 2
        if args:
            precision = args[0]
            args = args[1:]
        self.precision = decimal.Decimal('0.' + '0'*(precision-1) + '1')
        return args, kwargs

    def _convert(self, value):
        # IB writes numbers with comma separators
        value = value.replace(',', '')
        value = decimal.Decimal(value)

        return value.quantize(self.precision)


class OneOf(Field):
    def _init(self, *args, **kwargs):
        self.valid = set(args)
        return (), kwargs

    def _convert(self, value):
        if value in self.valid:
            return value
        raise ValueError("'%s' is not OneOf %r" % (value, self.valid))


class List(Field):
    """
    IB sends lists comma-delimited without enclosing brackets.
    """
    def _init(self, *args, **kwargs):
        self.valid = kwargs.pop('valid', None)
        return args, kwargs

    def _convert(self, value):
        values = [v.strip() for v in value.split(',')]
        if self.valid:
            for val in values:
                if val not in self.valid:
                    raise ValueError  # FIXME
        return values


def parse_isodate(value, dayfirst):
    """
    Parse ISO8601 format date strings (yyyy-MM-dd) into year, month, day.

    Args: value - type str
          dayfirst - ignored here
    Returns: 3-tuple (year, month, day), all type int
    """
    year = int(value[:4])
    month = int(value[5:7])
    day = int(value[8:])
    return year, month, day


def parse_yyyyMMdd(value, dayfirst):
    """
    Parse yyyyMMdd format date strings into year, month, day.

    Args: value - type str
          dayfirst - ignored here
    Returns: 3-tuple (year, month, day), all type int
    """
    year = int(value[:4])
    month = int(value[4:6])
    day = int(value[6:])
    return year, month, day


def parse_MMddyyyy(value, dayfirst):
    """
    Parse MM/dd/yyyy (or dd/MM/yyyy) format date strings into year, month, day.

    Args: value - type str
          dayfirst - type bool; False: MM/dd/yyyy; True: dd/MM/yyyy
    Returns: 3-tuple (year, month, day), all type int
    """
    month = int(value[:2])
    day = int(value[3:4])
    year = int(value[6:])

    if dayfirst:
        day, month = month, day

    return year, month, day


def prepend_century(year):
    """
    Turn a 2-digit year into a 4-digit year.

    Args: 2-digit int
    Returns: type int
    """
    assert 0 <= year < 100
    century = {True: 1900, False: 2000}[year > 68]
    return century + int(year)


def parse_MMddyy(value, dayfirst):
    """
    Parse MM/dd/yy (or dd/MM/yy) format date strings into year, month, day.

    Args: value - type str
          dayfirst - type bool; False: MM/dd/yy; True: dd/MM/yy
    Returns: 3-tuple (year, month, day), all type int
    """
    month = int(value[:2])
    day = int(value[3:5])
    year = prepend_century(int(value[6:]))

    if dayfirst:
        day, month = month, day
    return year, month, day


def parse_ddMMMyy(value, dayfirst):
    """
    Parse dd-MMM-yy format date strings (e.g. '13-JUL-97')
    into year, month, day.

    Args: value - type str
          dayfirst - ignored here
    Returns: 3-tuple (year, month, day), all type int
    """
    day = int(value[:2])
    month = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
             'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}[value[3:6]]
    year = prepend_century(int(value[7:]))
    return year, month, day


class Date(Field):
    """
    Format-agnostic date string.
    """
    # date_parsers is a nested dict keyed first by string length, then by
    # count of '/' within the date string.  We can't easily distinguish
    # between e.g. MM/dd/yyyy and dd/MM/yyyy, so this is configured by
    # setting Date.dayfirst, which by default is American style (MM/dd)
    # not Euro style (dd/MM).
    #
    # Seriously though, just configure Flex queries for ISO format (YYYY-MM-dd)
    date_parsers = {8: {0: parse_yyyyMMdd, 2: parse_MMddyy},
                    9: {0: parse_ddMMMyy},
                    10: {0: parse_isodate, 2: parse_MMddyyyy}}
    dayfirst = False

    @classmethod
    def parse(cls, value):
        parser = cls.date_parsers[len(value)][value.count('/')]
        return parser(value, cls.dayfirst)

    def _convert(self, value):
        return datetime.date(*self.parse(value))


def first_hit(make_parser, value, separators):
    """
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
            raise ValueError  # FIXME
    return value


class Time(Field):
    """
    Format-agnostic time string.
    """
    separators = [':', '']

    @staticmethod
    def make_parser(separator):
        """
        Factory returning a function
        """
        def fn(value):
            valid = separator == '' or value.count(separator) == 2
            if not valid:
                raise ValueError  # FIXME
            hours = int(value[:2])
            minutes = int(value[2 + len(separator):4 + len(separator)])
            seconds = int(value[4 + 2 * len(separator):])
            return hours, minutes, seconds
        return fn

    @classmethod
    def parse(cls, value):
        return first_hit(cls.make_parser, value, cls.separators)

    def _convert(self, value):
        return datetime.time(*self.parse(value))


class DateTime(Field):
    """
    Format-agnostic datetime string.
    """
    separators = [';', ',', ' ', '']

    @staticmethod
    def make_parser(separator):
        """
        Factory returning a function
        """
        def fn(value):
            valid = separator == '' or value.count(separator) == 1
            if not valid:
                raise ValueError  # FIXME
            date, time = value.split(separator)
            return Date.parse(date) + Time.parse(time)
        return fn

    def _convert(self, value):
        if not value:  # Falsy values, e.g. '', None, [] are not valid
            raise self.fail('invalid')
        if len(value) < 12:
            # Just a date, with no time info
            return datetime.datetime(*Date.parse(value))
        else:
            return datetime.datetime(*first_hit(self.make_parser, value, self.separators))
