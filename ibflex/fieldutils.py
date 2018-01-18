# coding: utf-8
"""
Utilities used by Field converters for Interactive Brokers Flex XML data
"""


class FlexFieldError(Exception):
    """ Base class for errors in this module """
    pass


def check_month_day(month, day):
    if month < 1 or month > 12:
        raise ValueError("Month out of range")
    if day < 1 or day > 31:
        raise ValueError("Day out of range")

def parse_isodate(value, dayfirst):
    """
    Parse ISO8601 format date strings (YYYY-mm-dd) into year, month, day.

    Args: value - type str
          dayfirst - ignored here
    Returns: 3-tuple (year, month, day), all type int
    """
    if value.count('-') != 2:
        msg = "{} can't be parsed as YYYY-mm-dd"
        raise FlexFieldError(msg.format(value))
    year, month, day = value.split('-')
    if len(year) != 4 or len(month) != 2 or len(day) != 2:
        msg = "{} can't be parsed as YYYY-mm-dd"
        raise FlexFieldError(msg.format(value))
    year = int(year)
    month = int(month)
    day = int(day)
    try:
        check_month_day(month, day)
    except ValueError as err:
        msg = "{}: {}".format(value, err)
        raise FlexFieldError(msg)
    return year, month, day


def parse_YYYYmmdd(value, dayfirst):
    """
    Parse YYYYmmdd format date strings into year, month, day.

    Args: value - type str
          dayfirst - ignored here
    Returns: 3-tuple (year, month, day), all type int
    """
    if len(value) != 8:
        msg = "{} can't be parsed as YYYYmmdd"
        raise FlexFieldError(msg.format(value))
    year = value[:4]
    month = value[4:6]
    day = value[6:]
    if len(month) != 2 or len(day) !=2 or len(year) != 4:
        msg = "{} can't be parsed as YYYYmmdd"
        raise FlexFieldError(msg.format(value))
    year = int(year)
    month = int(month)
    day = int(day)
    try:
        check_month_day(month, day)
    except ValueError as err:
        msg = "{}: {}".format(value, err)
        raise FlexFieldError(msg)
    return year, month, day


def parse_mmddYYYY(value, dayfirst):
    """
    Parse mm/dd/YYYY (or dd/mm/YYYY) format date strings into year, month, day.

    Args: value - type str
          dayfirst - type bool; False: mm/dd/YYYY; True: dd/mm/YYYY
    Returns: 3-tuple (year, month, day), all type int
    """
    if value.count('/') != 2:
        msg = "{} can't be parsed as mm/dd/YYYY"
        raise FlexFieldError(msg.format(value))
    month, day, year = value.split('/')
    if len(month) != 2 or len(day) != 2 or len(year) != 4:
        msg = "{} can't be parsed as mm/dd/YYYY"
        raise FlexFieldError(msg.format(value))
    month = int(month)
    day = int(day)
    year = int(year)

    if dayfirst:
        day, month = month, day

    try:
        check_month_day(month, day)
    except ValueError as err:
        msg = "{}: {}".format(value, err)
        raise FlexFieldError(msg)
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


def parse_mmddyy(value, dayfirst):
    """
    Parse mm/dd/yy (or dd/mm/yy) format date strings into year, month, day.

    Args: value - type str
          dayfirst - type bool; False: mm/dd/yy; True: dd/mm/yy
    Returns: 3-tuple (year, month, day), all type int
    """
    if value.count('/') != 2:
        msg = "{} can't be parsed as mm/dd/yy"
        raise FlexFieldError(msg.format(value))
    month, day, year = value.split('/')
    if len(month) != 2 or len(day) !=2 or len(year) != 2:
        msg = "{} can't be parsed as mm/dd/yy"
        raise FlexFieldError(msg.format(value))
    month = int(month)
    day = int(day)
    year = int(year)
    if not (0 <= year < 100):
        msg = "{}: year must be between 0 and 99".format(value)
        raise FlexFieldError(msg)
    try:
        check_month_day(month, day)
    except ValueError as err:
        msg = "{}: {}".format(value, err)
        raise FlexFieldError(msg)
    year = prepend_century(year)

    if dayfirst:
        day, month = month, day
    return year, month, day


def parse_ddbbbyy(value, dayfirst):
    """
    Parse dd-bbb-yy format date strings (e.g. '13-JUL-97')
    into year, month, day.

    Args: value - type str
          dayfirst - ignored here
    Returns: 3-tuple (year, month, day), all type int
    """
    if value.count('-') != 2:
        msg = "{} can't be parsed as dd-bbb-yy"
        raise FlexFieldError(msg.format(value))
    day, month, year = value.split('-')
    if len(month) != 3 or len(day) != 2 or len(year) != 2:
        msg = "{} can't be parsed as dd-bbb-yy"
        raise FlexFieldError(msg.format(value))
    day = int(day)
    try:
        month = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
                 'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}[month]
    except KeyError:
        msg = "{}: unknown month {}".format(value, month)
        raise FlexFieldError(msg)
    year = int(year)
    if not (0 <= year < 100):
        msg = "{}: year must be between 0 and 99".format(value)
        raise FlexFieldError(msg)
    year = prepend_century(year)
    try:
        check_month_day(month, day)
    except ValueError as err:
        msg = "{}: {}".format(value, err)
        raise FlexFieldError(msg)
    return year, month, day


# date_parsers is a nested dict keyed first by string length, then by
# count of '/' within the date string.
date_parsers = {8: {0: parse_YYYYmmdd, 2: parse_mmddyy},
                9: {0: parse_ddbbbyy},
                10: {0: parse_isodate, 2: parse_mmddYYYY}}


# Currency codes
ISO4217 = ('AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG',
           'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND',
           'BOB', 'BOV', 'BRL', 'BSD', 'BTN', 'BWP', 'BYR', 'BZD', 'CAD',
           'CDF', 'CHE', 'CHF', 'CHW', 'CLF', 'CLP', 'CNY', 'COP', 'COU',
           'CRC', 'CUC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD',
           'EEK', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD', 'FKP', 'GBP', 'GEL',
           'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK',
           'HTG', 'HUF', 'IDR', 'ILS', 'INR', 'IQD', 'IRR', 'ISK', 'JMD',
           'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KRW', 'KWD',
           'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LTL', 'LVL',
           'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRO',
           'MUR', 'MVR', 'MWK', 'MXN', 'MXV', 'MYR', 'MZN', 'NAD', 'NGN',
           'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP',
           'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR',
           'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLL', 'SOS', 'SRD',
           'STD', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP',
           'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'USN', 'USS',
           'UYI', 'UYU', 'UZS', 'VEF', 'VND', 'VUV', 'WST', 'XAF', 'XAG',
           'XAU', 'XBA', 'XBB', 'XBC', 'XBD', 'XCD', 'XDR', 'XOF', 'XPD',
           'XPF', 'XPT', 'XTS', 'XXX', 'YER', 'ZAR', 'ZMK', 'ZWL')

CURRENCY_CODES = ISO4217 + ('CNH', 'BASE_SUMMARY')
