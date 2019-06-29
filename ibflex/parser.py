# coding: utf-8
"""Parser/type converter for data in Interactive Brokers' Flex XML format.

https://www.interactivebrokers.com/en/software/reportguide/reportguide.htm
"""
import xml.etree.ElementTree as ET
import enum
import collections
import datetime
import decimal
from typing import List, Tuple, Union, Optional, Any, Callable, Iterable

from ibflex import Types, utils


class FlexParserError(Exception):
    """ Error experienced while parsing Flex XML data. """


AttributeType = Union[
    str, int, bool, decimal.Decimal, datetime.date, datetime.time,
    datetime.datetime, enum.Enum, List[str], None,
]
""" Possible type annotations for a class attribute from Types module. """


###############################################################################
#  PARSE FUNCTIONS
###############################################################################
def parse(source) -> Types.FlexQueryResponse:
    """Parse Flex XML data into a hierarchy of ibflex.Types class instances.

    Args:
        source: file name or file object.
    """
    tree = ET.ElementTree()
    tree.parse(source)
    root = tree.getroot()
    if root.tag != "FlexQueryResponse":
        raise FlexParserError("Not a FlexQueryResponse")
    parsed = parse_element(root)
    assert isinstance(parsed, Types.FlexQueryResponse)
    return parsed


def parse_element(
    elem: ET.Element
) -> Union[Types.FlexElement, List[Types.FlexElement]]:
    """Distinguish XML data element from container element; dispatch accordingly.

    Flex format stores data as XML element attributes, while container elements
    have no attributes.  The only exception is <FlexStatements>, which has a
    `count` attribute as a check on its contents.
    """
    if not elem.attrib or elem.tag == "FlexStatements":
        return parse_element_container(elem)

    return parse_data_element(elem)


def parse_element_container(elem: ET.Element) -> List[Types.FlexElement]:
    """Parse XML element container into list of FlexElement subclass instances.
    """
    tag = elem.tag

    if tag == "FxPositions":
        #   <FxLot> is double-wrapped (???).  Element structure here is:
        #       <FxPositions><FxLots><FxLot /></FxLots></FxPositions>
        #   Look through <FxLots> to create FlexStatement.FxPositions
        #   as a list of FxLot instances.
        if len(elem) > 1:
            msg = "Bad XML structure: <FXPositions> contains multiple <FxLots>"
            raise FlexParserError(msg)
        elem = elem[0] if len(elem) == 1 else elem
    elif tag == "FlexStatements":
        # Verify that # of contained <FlexStatement> elements matches
        # what's reported in <FlexStatements count> attribute
        count = int(elem.attrib["count"])
        if len(elem) != count:
            msg = f"FlexStatement count={len(elem)}; expected count={count}"
            raise FlexParserError(msg)

    instances = [parse_data_element(child) for child in elem]

    # Sanity check - list contents should all be same type
    if not utils.all_equal(type(instance) for instance in instances):
        types = {type(instance) for instance in instances}
        raise FlexParserError(f"{tag} contains multiple element types {types}")

    return instances


def parse_data_element(
    elem: ET.Element
) -> Types.FlexElement:
    """Parse an XML data element into a Types.FlexElement subclass instance.
    """
    Class = getattr(Types, elem.tag)

    #  Map of Class attribute name to type hint.
    #  Need to collect annotations from traversing entire Class MRO
    #  (method resolution order) to support mixin inheritance.
    schema = collections.ChainMap(
        *[
            cls.__annotations__
            for cls in Class.__mro__
            if hasattr(cls, "__annotations__")
        ]
    )

    def parse_element_attr(
        name: str, value: str, Type: AttributeType
    ) -> Tuple[str, Any]:
        """Convert an XML element attribute into its corresponding Python type,
        based on the FlexElement subclass attribute type hint.

        Note:
            Empty string (null data) returns empty list (for list Types) or None

        Args:
            name: XML attribute name
            value: XML attribute value
            Type: type hint for FlexElement subclass attribute of `name`
        """
        if not value:
            return name, [] if getattr(Type, "_name", "") == "List" else None

        if isinstance(Type, enum.EnumMeta):
            #  Dispatch Enums by metaclass, not class; they're all handled the same way.
            #  Enums defined in Types bind custom names to the IB-supplied values.
            #  To convert, just do a reverse lookup on the incoming string.
            #  https://docs.python.org/3/library/enum.html#programmatic-access-to-enumeration-members-and-their-attributes
            return name, Type(value)

        # Validate currency
        if "currency" in name.lower() and value not in CURRENCY_CODES:
            raise FlexParserError(f"Unknown currency {value!r}")

        try:
            return name, ATTRIB_CONVERTERS[Type](value)
        except Exception as exc:
            msg = f"{Class.__name__}.{name}" + str(exc)
            raise FlexParserError(msg)

    # Parse element attributes
    attrs = dict(
        parse_element_attr(k, v, schema[k]) for k, v in elem.attrib.items()
    )

    # FlexQueryResponse & FlexStatement are the only data elements
    # that contain other data elements.
    contained_elements = {child.tag: parse_element(child) for child in elem}
    if contained_elements:
        assert elem.tag in ("FlexQueryResponse", "FlexStatement")
        attrs.update(contained_elements)

    instance = Class(**attrs)
    return instance


###############################################################################
#  INPUT VALUE PREP FUNCTIONS FOR DATA CONVERTERS
###############################################################################
def prep_date(value: str) -> Tuple[int, int, int]:
    """Returns a tuple of (year, month, day).
    """
    date_format = DATE_FORMATS[len(value)][value.count('/')]
    return datetime.datetime.strptime(value, date_format).timetuple()[:3]


def prep_time(value: str) -> Optional[Tuple[int, int, int]]:
    """Returns a tuple of (hour, minute, second).
    """
    time_format = TIME_FORMATS[len(value)]
    return datetime.datetime.strptime(value, time_format).timetuple()[3:6]


def prep_datetime(value: str) -> Tuple[int, ...]:
    """Returns a tuple of (year, month, day, hour, minute, second).
    """

    def merge_date_time(datestr: str, timestr: str) -> Tuple[int, ...]:
        """Convert presplit date/time strings into args ready for datetime().

        Args:
            datestr - string representing date, in any recognized format.
            timestr - string representing time, in any recognized format.

        Returns:
            tuple of (year, month, day, hour, minute, second).
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
        return merge_date_time(datestr, timestr)
    elif len(seps) == 0:
        #  If we can't find an explicit date/time separator in input value,
        #  first try the value as a bare date (no time).
        try:
            prepped_date = prep_date(value)
        except Exception:
            pass
        else:
            return prepped_date

        #  If that doesn't work, assume null separator.
        #  Brute force guess index of date/time split.
        #  Shortest loop is to iterate over TIME_FORMATS, slicing value from
        #  the rear and taking that as the time string, with the date string
        #  comprising the remainder.

        def testlength(
            value: str, time_length: int
        ) -> Optional[Tuple[int, ...]]:
            """Assuming time substring is of given length, try to process value
            into time tuple.

            Args:
                value: input string data.
                time_length: candidate length of time substring.

            Returns:
                If valid, return (year, month, day, hour, minute, second).
                If invalid, return None.
            """
            try:
                datestr, timestr = value[:-time_length], value[-time_length:]
                return merge_date_time(datestr, timestr)
            except Exception:
                return None

        tested = (testlength(value, length) for length in TIME_FORMATS)
        prepped = [t for t in tested if t is not None]
        if len(prepped) != 1:
            raise FlexParserError(f"Bad date/time format: {prepped}")
        return prepped[0]

    # Multiple date/time separators appear in input value.
    raise FlexParserError(f"Bad date/time format: {prepped}")


def prep_sequence(value: str) -> Iterable[str]:
    """Split a sequence string into its component items.

    Flex `notes` attribute is semicolon-delimited; other sequences use commas.
    """
    sep = ";" if ";" in value else ","
    return (v for v in value.split(sep) if v)


###############################################################################
#  DATA CONVERTER FUNCTIONS
###############################################################################
def make_converter(
    Type: type, *, prep: Callable[[str], Any]
) -> Callable[[str], AttributeType]:
    """Factory producing converter function for type.

    Args:
        Type: type constructor e.g. str, Decimal, datetime
        prep: function that accepts string input and returns value(s) that can
              can be passed to the type constructor to create a Type instance.

    Returns: a function that accepts string input and returns a Type instance.
    """
    def convert(value: str) -> AttributeType:
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
                f"{value!r} can't be converted to {Type}"
            )

    return convert


convert_string = make_converter(str, prep=utils.identity_func)
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
convert_sequence = make_converter(list, prep=prep_sequence)

ATTRIB_CONVERTERS = {
    str: convert_string,
    Optional[str]: convert_string,
    int: convert_int,
    Optional[int]: convert_int,
    bool: convert_bool,
    Optional[bool]: convert_bool,
    decimal.Decimal: convert_decimal,
    Optional[decimal.Decimal]: convert_decimal,
    datetime.date: convert_date,
    Optional[datetime.date]: convert_date,
    datetime.time: convert_time,
    datetime.datetime: convert_datetime,
    Optional[datetime.datetime]: convert_datetime,
    List[str]: convert_sequence,
}
"""Map of Types class attribute type hint to corresponding converter function.
"""


###############################################################################
#  IB DATE FORMATS
#  https://www.interactivebrokers.com/en/software/am/am/reports/activityflexqueries.htm
###############################################################################
DATE_FORMATS = {8: {0: "%Y%m%d", 2: "%m/%d/%y"},
                9: {0: "%d-%b-%y"},
                10: {0: "%Y-%m-%d", 2: "%m/%d/%y"}}
"""Keyed first by string length, then by "/" count within string.

We can't distinguish in-band between US MM/dd/yyyy and Euro dd/MM/yyyy.
Given an ambiguous date format, we assume US format.

ALWAYS CONFIGURE YOUR REPORTS TO USE ISO-8601 DATE FORMAT (yyyy-MM-dd).

Available date formats are:
    yyyyMMdd (default)
    yyyy-MM-dd
    MM/dd/yyyy
    MM/dd/yy
    dd/MM/yyyy
    dd/MM/yy
    dd-MMM-yy
"""

TIME_FORMATS = {6: "%H%M%S", 8: "%H:%M:%S"}
"""Keyed by string length.

Available time formats are:
    HHmmss (default)
    HH:mm:ss
"""

DATETIME_SEPARATORS = {";", ",", " "}
"""We omit the null separator (empty string) because it screws up our logic.

DO NOT CONFIGURE YOUR REPORTS TO USE NULL-SEPARATED DATE/TIME FIELDS.

Available date/time separators are:
    ;   (semi-colon, the default)
    ,   (comma)
    ' ' (single-spaced)
    No separator
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
        print(file)
        response = parse(file)
        for stmt in response.FlexStatements:
            for trade in stmt.Trades:
                print(trade)


if __name__ == "__main__":
    main()
