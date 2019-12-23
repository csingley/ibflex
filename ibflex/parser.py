# coding: utf-8
"""Parser/type converter for data in Interactive Brokers' Flex XML format.

https://www.interactivebrokers.com/en/software/reportguide/reportguide.htm

Flex report configuration needed by this module:
    Date format: choose yyyy-MM-dd
    Trades: uncheck "Symbol Summary", "Asset Class", "Orders"
"""
import xml.etree.ElementTree as ET
import datetime
import decimal
import itertools
import functools
from typing import Tuple, Union, Optional, Any, Callable, Iterable

from ibflex import Types, enums, utils


class FlexParserError(Exception):
    """ Error experienced while parsing Flex XML data. """


DataType = Union[
    None, str, int, bool, decimal.Decimal, datetime.date, datetime.time,
    datetime.datetime, enums.EnumType, Tuple[str, ...], Tuple[enums.Code, ...]
]
"""Possible type annotations for class attributes of a FlexElement that is
a data element (not a container).
"""


###############################################################################
#  PARSE FUNCTIONS
###############################################################################
def parse(source) -> Types.FlexQueryResponse:
    """Parse Flex XML data into a hierarchy of ibflex.Types class instances.

    Args:
        source: file name, file object, or bytes.
    """
    tree = ET.ElementTree()

    #  Accept output of client.download(), which is bytes.
    if isinstance(source, bytes):
        root = ET.XML(source)
    #  Accept file name or file object.
    else:
        root = tree.parse(source)

    if root.tag != "FlexQueryResponse":
        raise FlexParserError("Not a FlexQueryResponse")
    parsed = parse_element(root)
    assert isinstance(parsed, Types.FlexQueryResponse)
    return parsed


def parse_element(
    elem: ET.Element
) -> Union[Types.FlexElement, Tuple[Types.FlexElement, ...]]:
    """Distinguish XML data element from container element; dispatch accordingly.

    Flex format stores data as XML element attributes, while container elements
    have no attributes.  The only exception is <FlexStatements>, which has a
    `count` attribute as a check on its contents.
    """
    if elem.tag == "FlexStatements":
        #  Verify that # of contained <FlexStatement> elements matches
        #  what's reported in <FlexStatements count> attribute.
        try:
            count = int(elem.get("count", ""))
            assert len(elem) == count
        except (ValueError):
            msg = f"Malformed FlexStatements.count={elem.get('count', '')}"
            raise FlexParserError(msg)
        except AssertionError:
            msg = f"Wrong FlexStatements.count={count} vs. {len(elem)}"
            raise FlexParserError(msg)

        return parse_element_container(elem)

    if not elem.attrib:
        return parse_element_container(elem)

    return parse_data_element(elem)


def parse_element_container(elem: ET.Element) -> Tuple[Types.FlexElement, ...]:
    """Parse XML element container into FlexElement subclass instances.
    """
    tag = elem.tag

    if tag == "FxPositions":
        #  <FxPositions> contains an <FxLots> wrapper per currency.
        #  Element structure here is:
        #       <FxPositions><FxLots><FxLot /></FxLots></FxPositions>
        #  Flatten the nesting to create FxPositions as a tuple of FxLots
        fxlots = (parse_element_container(child) for child in elem)
        return tuple(itertools.chain.from_iterable(fxlots))

    instances = tuple(parse_data_element(child) for child in elem)
    return instances


def parse_data_element(
    elem: ET.Element
) -> Types.FlexElement:
    """Parse an XML data element into a Types.FlexElement subclass instance.
    """
    #  Look up XML element's matching FlexElement subclass in ibflex.Types.
    Class = getattr(Types, elem.tag)

    #  Parse element attributes
    try:
        attrs = dict(
            parse_element_attr(Class, k, v)
            for k, v in elem.attrib.items()
        )
    except KeyError as exc:
        msg = f"{Class.__name__} has no attribute " + str(exc)
        raise FlexParserError(msg)

    #  FlexQueryResponse & FlexStatement are the only data elements
    #  that contain other data elements.
    contained_elements = {child.tag: parse_element(child) for child in elem}
    if contained_elements:
        assert elem.tag in ("FlexQueryResponse", "FlexStatement")
        attrs.update(contained_elements)

    try:
        return Class(**attrs)
    except Exception as exc:
        raise FlexParserError(f"{Class.__name__} - " + str(exc))


def parse_element_attr(
    Class: Types.FlexElement, name: str, value: str
) -> Tuple[str, Any]:
    """Convert an XML element attribute into its corresponding Python type,
    based on the FlexElement subclass attribute type hint.

    Args:
        Class: FlexElement subclass
        name: XML attribute name
        value: XML attribute value
    """
    #  Validate currency of any field named something like "currency".
    if "currency" in name.lower() and value not in CURRENCY_CODES:
        raise FlexParserError(f"{name}: Unknown currency {value!r}")

    #  FIXME
    #  This "dot reference" gets hit a lot by parse_data_element(), and `Class`
    #  is always the same in the list comprehension that calls this function.
    #  Consider moving `Class.__annotations__` up out of the list comprehension
    #  in parse_data_element(), instead accepting it as a function arg here.
    Type = Class.__annotations__[name]

    try:
        converted = ATTRIB_CONVERTERS[Type](value=value)
        return name, converted
    except KeyError as exc:
        msg = f"{Class.__name__}.{name} - Don't know how to convert "  # type: ignore
        raise FlexParserError(msg + str(exc))
    except Exception as exc:
        msg = f"{Class.__name__}.{name} - " + str(exc)  # type: ignore
        raise FlexParserError(msg)


###############################################################################
#  INPUT VALUE PREP FUNCTIONS FOR DATA CONVERTERS
#  These are just implementation details for converters and don't need testing.
###############################################################################
def prep_date(value: str) -> Tuple[int, int, int]:
    """Returns a tuple of (year, month, day).
    """
    date_format = DATE_FORMATS[len(value)][value.count('/')]
    return datetime.datetime.strptime(value, date_format).timetuple()[:3]


def prep_time(value: str) -> Tuple[int, int, int]:
    """Returns a tuple of (hour, minute, second).
    """
    time_format = TIME_FORMATS[len(value)]
    return datetime.datetime.strptime(value, time_format).timetuple()[3:6]


def prep_datetime(value: str) -> Tuple[int, ...]:
    """Returns a tuple of (year, month, day, hour, minute, second).
    """
    #  HACK - some old data has ", " separator instead of ",".
    value = value.replace(", ", ",")

    def merge_date_time(datestr: str, timestr: str) -> Tuple[int, ...]:
        """Convert presplit date/time strings into args ready for datetime().
        """
        prepped_date = prep_date(datestr)
        assert prepped_date is not None

        prepped_time = prep_time(timestr)
        assert prepped_time is not None

        return prepped_date + prepped_time

    seps = [sep for sep in DATETIME_SEPARATORS if sep in value]
    if len(seps) == 1:
        sep = seps[0]
        datestr, timestr = value.split(sep)
        # HACK - some old data has TZ offset appended.  Drop the offset.
        if "-" in timestr:
            timestr = timestr.split("-")[0]
        elif "+" in timestr:
            timestr = timestr.split("+")[0]

        return merge_date_time(datestr, timestr)
    elif len(seps) == 0:
        #  If we can't find an explicit date/time separator in input value,
        #  best case is that the value as a bare date (no time).
        try:
            return prep_date(value)
        except Exception:
            pass

        #  If that doesn't work, assume null separator.  Brute force guess
        #  index of date/time split. Shortest loop is to iterate over
        #  TIME_FORMATS (there's only 2 of them).

        def testtimelength(
            value: str, time_length: int
        ) -> Optional[Tuple[int, ...]]:
            """Assuming time substring is of given length, try to process value
            into time tuple.
            """
            datestr, timestr = value[:-time_length], value[-time_length:]
            try:
                return merge_date_time(datestr, timestr)
            except Exception:
                return None

        tested = (testtimelength(value, length) for length in TIME_FORMATS)
        prepped = [t for t in tested if t is not None]
        if len(prepped) != 1:
            raise FlexParserError(f"Bad date/time format: {value}")
        return prepped[0]

    # Multiple date/time separators appear in input value.
    raise FlexParserError(f"Bad date/time format: {value}")

    sep = seps[0]

    try:
        #  HACK - some old data has ", " separator, which shows up as
        #  seps = [",", ""].  Keep the comma, strip the space.
        datestr, timestr = value.split(sep)
        timestr = timestr.strip()
        return merge_date_time(datestr, timestr)
    except Exception:
        raise FlexParserError(f"Bad date/time format: {value}")


def prep_sequence(value: str) -> Iterable[str]:
    """Split a sequence string into its component items.

    Flex `notes` attribute is semicolon-delimited; other sequences use commas.

    Empty string input interpreted as null data; returns empty list.
    """
    sep = ";" if ";" in value else ","
    return (v for v in value.split(sep) if v) if value != "" else []


def prep_code_sequence(value: str) -> Iterable[enums.Code]:
    """Split a code sequence string into its component codes.

    Flex `notes` attribute is semicolon-delimited; other sequences use commas.

    Empty string input interpreted as null data; returns empty list.
    """
    sep = ";" if ";" in value else ","
    return (
        enums.Code(v)
        for v in value.split(sep)
        if v
    ) if value != "" else []


###############################################################################
#  DATA CONVERTER FUNCTIONS
###############################################################################
def make_converter(
    Type: type, *, prep: Callable[[str], Any]
) -> Callable[[str], DataType]:
    """Factory producing converter function for type.

    Args:
        Type: type constructor e.g. str, Decimal, datetime
        prep: function that accepts string input and returns value(s) that can
              can be passed to the type constructor to create a Type instance.

    Returns: a function that accepts string input and returns a Type instance.
    """
    def convert(value: str) -> DataType:
        try:
            prepped_value = prep(value)
            if prepped_value is None:
                # Preserve "null data" indicated by prep function.
                return None
            elif isinstance(prepped_value, tuple):
                # date/time values are prepped into time tuples;
                # unpack before passing to type constructor.
                return Type(*prepped_value)
            else:
                return Type(prepped_value)
        except Exception:
            raise FlexParserError(
                f"Can't convert {value!r} to {Type}"
            )

    return convert


def make_optional(func):

    def optional_convert(value):
        return None if value in ("", "-", "--", "N/A") else func(value)

    return optional_convert


convert_string = make_optional(make_converter(str, prep=utils.identity_func))
convert_int = make_converter(int, prep=utils.identity_func)
# IB sends "Y"/"N" for True/False
convert_bool = make_converter(bool, prep=lambda x: {"Y": True, "N": False}[x])
# IB sends numeric data with place delimiters (commas)
convert_decimal = make_converter(
    decimal.Decimal,
    prep=lambda x: x.replace(",", "")
)
convert_date = make_converter(datetime.date, prep=prep_date)
convert_time = make_converter(datetime.time, prep=prep_time)
convert_datetime = make_converter(datetime.datetime, prep=prep_datetime)
convert_sequence = make_converter(tuple, prep=prep_sequence)
convert_code_sequence = make_converter(tuple, prep=prep_code_sequence)


def convert_enum(Type, value):
    #  Work around old versions of values; convert to the new format
    if Type is enums.CashAction and value == "Deposits/Withdrawals":
        value = "Deposits & Withdrawals"
    elif Type is enums.TransferType and value == "ACAT":
        value = "ACATS"

    #  Enums bind custom names to the IB-supplied values.
    #  To convert, just do a by-value lookup on the incoming string.
    #  https://docs.python.org/3/library/enum.html#programmatic-access-to-enumeration-members-and-their-attributes
    return Type(value) if value != "" else None


ATTRIB_CONVERTERS = {
    str: convert_string,
    Optional[str]: convert_string,
    int: convert_int,
    Optional[int]: make_optional(convert_int),
    bool: convert_bool,
    Optional[bool]: make_optional(convert_bool),
    decimal.Decimal: convert_decimal,
    Optional[decimal.Decimal]: make_optional(convert_decimal),
    datetime.date: convert_date,
    Optional[datetime.date]: make_optional(convert_date),
    datetime.time: convert_time,
    Optional[datetime.time]: make_optional(convert_time),
    datetime.datetime: convert_datetime,
    Optional[datetime.datetime]: make_optional(convert_datetime),
    Tuple[str, ...]: convert_sequence,
    Tuple[enums.Code, ...]: convert_code_sequence,
}
"""Map of FlexElement attribute type hint to corresponding converter function.
"""

ATTRIB_CONVERTERS.update(
    {
        Optional[Enum]: functools.partial(convert_enum, Type=Enum)
        for Enum in enums.ENUMS
    }
)
"""Map all Enum subclasses as Optional.
"""


###############################################################################
#  IB DATE FORMATS
#  https://www.interactivebrokers.com/en/software/am/am/reports/activityflexqueries.htm
###############################################################################
DATE_FORMATS = {8: {0: "%Y%m%d", 2: "%m/%d/%y"},
                9: {0: "%d-%b-%y"},
                10: {0: "%Y-%m-%d", 2: "%m/%d/%Y"}}
"""Keyed first by string length, then by "/" count within string.

We can't distinguish in-band between US MM/dd/yyyy and Euro dd/MM/yyyy.
Given an ambiguous date format, we assume US format.

ALWAYS CONFIGURE YOUR REPORTS TO USE ISO-8601 DATE FORMAT (yyyy-MM-dd).

Available date formats are:
    yyyyMMdd (default)
    yyyy-MM-dd
    MM/dd/yyyy
    MM/dd/yy
    dd/MM/yyyy [not implemented in ibflex]
    dd/MM/yy [not implemented in ibflex]
    dd-MMM-yy
"""

TIME_FORMATS = {6: "%H%M%S", 8: "%H:%M:%S"}
"""Keyed by string length.

Available time formats are:
    HHmmss (default)
    HH:mm:ss
"""

DATETIME_SEPARATORS = [";", ",", " ", "T"]
"""We omit the null separator (empty string) because it screws up our logic.

DO NOT CONFIGURE YOUR REPORTS TO USE NULL-SEPARATED DATE/TIME FIELDS.

Available date/time separators are:
    ;   (semi-colon, the default)
    ,   (comma)
    ' ' (single-spaced)
    No separator

Additionally, some old values have 'T' as a date/time separator with TZ offset.
"""


###############################################################################
#  CURRENCIES
###############################################################################
ISO4217 = (
    "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN",
    "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BOV",
    "BRL", "BSD", "BTN", "BWP", "BYR", "BZD", "CAD", "CDF", "CHE", "CHF",
    "CHW", "CLF", "CLP", "CNY", "COP", "COU", "CRC", "CUC", "CUP", "CVE",
    "CZK", "DJF", "DKK", "DOP", "DZD", "EEK", "EGP", "ERN", "ETB", "EUR",
    "FJD", "FKP", "GBP", "GEL", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD",
    "HKD", "HNL", "HRK", "HTG", "HUF", "IDR", "ILS", "INR", "IQD", "IRR",
    "ISK", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "KPW", "KRW",
    "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LTL", "LVL",
    "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRO", "MUR",
    "MVR", "MWK", "MXN", "MXV", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK",
    "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG",
    "QAR", "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK",
    "SGD", "SHP", "SLL", "SOS", "SRD", "STD", "SVC", "SYP", "SZL", "THB",
    "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TWD", "TZS", "UAH", "UGX",
    "USD", "USN", "USS", "UYI", "UYU", "UZS", "VEF", "VND", "VUV", "WST",
    "XAF", "XAG", "XAU", "XBA", "XBB", "XBC", "XBD", "XCD", "XDR", "XOF",
    "XPD", "XPF", "XPT", "XTS", "XXX", "YER", "ZAR", "ZMK", "ZWL",
)
CURRENCY_CODES = ISO4217 + (
    "CNH",           # RMB traded in HK
    "BASE_SUMMARY",  # Fake currency code used in IB NAV/Performance reports
    "",              # Lot element allows blank currency ?!
)


###############################################################################
#  CLI SCRIPT
###############################################################################
def main():
    from argparse import ArgumentParser

    argparser = ArgumentParser(
        description="Quick test of Interactive Brokers Flex XML data parser"
    )
    argparser.add_argument("file", nargs="+", help="XML data file(s)")
    args = argparser.parse_args()

    for file in args.file:
        parse(file)
        print(f"Successfully parsed {file}")


if __name__ == "__main__":
    main()
