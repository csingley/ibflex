# coding: utf-8
"""
Parser/type converter for data in Interactive Brokers' Flex XML format.

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
""" Possible type annotations for a class attributes from Types module. """


def parse(source) -> Types.FlexQueryResponse:
    """Parse Flex XML data into hierarchy of ibflex.Types instances.
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
    """Distinguish XML data elements from list wrappers; dispatch accordingly.
    """
    tag = elem.tag

    if not hasattr(Types, tag):
        #  If ibflex.Types doesn't contain a class definition for this element,
        #  then it's a list wrapper, not a data element.
        return parse_list(elem)
    elif tag == "OptionEAE" and not elem.attrib:
        #  IB uses the same tag name for OptionEAE wrapper and data element.
        #  Force ignore the class definition for the OptionEAE wrapper
        #  (which has no element attributes, unlike the data element).
        return parse_list(elem)

    return parse_data_element(elem)


def parse_data_element(
    elem: ET.Element
) -> Types.FlexElement:
    """Parse an XML data element into a class instance from the Types module.
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

    # Parse XML element attributes
    def parse_attribute(
        attr_name: str, attr_type: AttributeType, value: str
    ) -> Tuple[str, Any]:
        if isinstance(attr_type, enum.EnumMeta):
            #  Enum classes have IB text as values; convert from value to name
            #  https://docs.python.org/3/library/enum.html#programmatic-access-to-enumeration-members-and-their-attributes
            return attr_name, attr_type(value)

        if "currency" in attr_name.lower():
            if value not in CURRENCY_CODES:
                raise FlexParserError(f"Unknown currency {value!r}")

        return attr_name, ATTRIB_CONVERTERS[attr_type](value)

    attrs = dict(
        parse_attribute(k, schema[k], v) for k, v in elem.attrib.items()
    )

    # Parse XML element children
    attrs.update({child.tag: parse_element(child) for child in elem})
    instance = Class(**attrs)
    return instance


def parse_list(elem: ET.Element) -> List[Types.FlexElement]:
    """Parse an XML wrapper into a list of Types class instances.
    """
    tag = elem.tag

    if tag == "FxPositions":
        #   <FxLot> is double-wrapped (???).  Element structure here is:
        #       <FxPositions><FxLots><FxLot /></FxLots></FxPositions>
        #   Look through <FxLots> to create FlexStatement.FxPositions
        #   as a list of FxLot instances.
        if len(elem) != 1:
            msg = "Bad XML structure: <FXPositions> contains multiple <FxLots>"
            raise FlexParserError(msg)
        elem = elem[0]
    elif tag == "FlexStatements":
        # Verify that # of contained <FlexStatement> elements matches
        # what's reported in <FlexStatements count> attribute
        count = int(elem.attrib["count"])
        if len(elem) != count:
            msg = f"FlexStatement count={len(elem)}; expected count={count}"
            raise FlexParserError(msg)

    instances = [parse_data_element(child) for child in elem]
    # Sanity check - list contents should all be same type
    assert utils.all_equal(type(instance) for instance in instances)
    return instances


###############################################################################
#  INPUT VALUE PREP FUNCTIONS FOR DATA CONVERTERS
###############################################################################
def prep_string(value: str) -> Optional[str]:
    """ Empty string is interpreted as null data. """
    return value or None


def prep_int(value: str) -> Optional[str]:
    """ Empty string is interpreted as null data. """
    return value or None


def prep_date(value: str) -> Optional[Tuple[int, int, int]]:
    """Returns a tuple of (year, month, day).
    Empty string is interpreted as null data.
    """
    if not value:
        return None
    date_format = DATE_FORMATS[len(value)][value.count('/')]
    return datetime.datetime.strptime(value, date_format).timetuple()[:3]


def prep_time(value: str) -> Optional[Tuple[int, int, int]]:
    """Returns a tuple of (hour, minute, second).
    Empty string is interpreted as null data.
    """
    if not value:
        return None
    time_format = TIME_FORMATS[len(value)]
    return datetime.datetime.strptime(value, time_format).timetuple()[3:6]


def prep_datetime(value: str) -> Optional[Tuple[int, ...]]:
    """Returns a tuple of (year, month, day, hour, minute, second).

    Empty string is interpreted as null data.
    """
    if not value:
        return None

    def merge_date_time(datestr: str, timestr: str) -> Tuple[int, ...]:
        """Convert presplit date/time strings into args ready for datetime().

        Args:
            datestr - string representing date, in any recognized format.
            timestr - string representing time, in any recognized format.

        Returns:
            tuple of (year, month, day, hour, minute, second).
        """
        prepped_date = prep_date(datestr)
        prepped_time = prep_time(timestr)
        assert prepped_date is not None
        assert prepped_time is not None

        return prepped_date + prepped_time

    seps = [sep for sep in DATETIME_SEPARATORS if sep in value]
    if len(seps) == 1:
        sep = seps[0]
        datestr, timestr = value.split(sep)
        return merge_date_time(datestr, timestr)
    elif len(seps) == 0:
        #  If we can't find an explicit date/time separator in input value,
        #  assume null separator.  Brute force guess index of date/time split.
        #
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


def prep_bool(value: str) -> Optional[bool]:
    """Convert 'Y'/'N' into True/False.
    Empty string is interpreted as null data.
    """
    if not value:
        return None
    return {"Y": True, "N": False}[value]


def prep_decimal(value: str) -> Optional[str]:
    """Strip place separators (commas) from string holding numeric value.
    Empty string is interpreted as null data.
    """
    return value.replace(",", "") or None


def prep_list(value: str) -> Iterable[str]:
    """Split a sequence string into its elements.
    Flex `notes` attribute is semicolon-separated; other sequences use commas.

    Empty string is interpreted as empty list.
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
                # date/time values are prepped into time_struct() slices;
                # unpack before passing to type constructor.
                return Type(*prepped_value)
            else:
                return Type(prepped_value)
        except Exception:
            raise FlexParserError(
                f"{value!r} can't be converted to {type}"
            )

    return convert


convert_decimal = make_converter(decimal.Decimal, prep=prep_decimal)


ATTRIB_CONVERTERS = {
    str: make_converter(str, prep=prep_string),
    int: make_converter(int, prep=prep_int),
    bool: make_converter(bool, prep=prep_bool),
    decimal.Decimal: convert_decimal,
    Union[decimal.Decimal, None]: convert_decimal,
    datetime.date: make_converter(datetime.date, prep=prep_date),
    datetime.time: make_converter(datetime.time, prep=prep_time),
    datetime.datetime: make_converter(datetime.datetime, prep=prep_datetime),
    List[str]: make_converter(list, prep=prep_list),
}
"""Map of Types class attribute type hint to corresponding converter function.
"""


###############################################################################
#  IB DATE FORMATS
#
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
                print(trade.buySell)


if __name__ == "__main__":
    main()
