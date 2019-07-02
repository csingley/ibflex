# coding: utf-8
"""
Download Flex queries without logging into Account Management web page.

https://www.interactivebrokers.com/en/software/am/am/reports/flex_web_service_version_3.htm
"""
# stdlib imports
from dataclasses import dataclass
import xml.etree.ElementTree as ET
from datetime import datetime
import time
from typing import Union, Optional


# 3rd party imports
import requests


###############################################################################
# SERVICE LOCATIONS
###############################################################################
FLEX_URL = 'https://gdcdyn.interactivebrokers.com/Universal/servlet/'
REQUEST_URL = FLEX_URL + 'FlexStatementService.SendRequest'
STMT_URL = FLEX_URL + 'FlexStatementService.GetStatement'


###############################################################################
# ERRORS
###############################################################################
ERRORS = [
    ("1003", "Statement is not available."),
    ("1004", "Statement is incomplete at this time. Please try again shortly."),
    ("1005", "Settlement data is not ready at this time. Please try again shortly."),
    ("1006", "FIFO P/L data is not ready at this time. Please try again shortly."),
    ("1007", "MTM P/L data is not ready at this time. Please try again shortly."),
    ("1008", "MTM and FIFO P/L data is not ready at this time. Please try again shortly."),
    ("1009", "The server is under heavy load. Statement could not be generated at this time. Please try again shortly."),
    ("1010", "Legacy Flex Queries are no longer supported. Please convert over to Activity Flex."),
    ("1011", "Service account is inactive."),
    ("1012", "Token has expired."),
    ("1013", "IP restriction."),
    ("1014", "Query is invalid."),
    ("1015", "Token is invalid."),
    ("1016", "Account in invalid."),
    ("1017", "Reference code is invalid."),
    ("1018", "Too many requests have been made from this token. Please try again shortly."),
    ("1019", "Statement generation in progress. Please try again shortly."),
    ("1020", "Invalid request or unable to validate request."),
    ("1021", "Statement could not be retrieved at this time. Please try again shortly."),
]
ERROR_CODES, ERROR_MSGS = zip(*ERRORS)

SERVER_BUSY = ("1009", "1019", )
CLIENT_THROTTLED = ("1018", )


class IbflexClientError(Exception):
    """ Base class for Exceptions defined in this module """


class BadResponseError(IbflexClientError):
    """
    Exception raised for malformed Flex response.
    """
    def __init__(self, response: requests.Response):
        self.response = response
        super(BadResponseError, self).__init__(response.content)


class ResponseCodeError(IbflexClientError):
    """
    Exception raised when Flex server returns a response with an error code.
    """
    def __init__(self, code: str, msg: str):
        self.code = code
        self.msg = msg
        super(ResponseCodeError, self).__init__(f"Code={code}: {msg}")


###############################################################################
#  FlexStatementResponse TYPES
###############################################################################
@dataclass(frozen=True)
class StatementAccess:
    timestamp: datetime
    ReferenceCode: str
    Url: str


@dataclass(frozen=True)
class StatementError:
    timestamp: datetime
    ErrorCode: str
    ErrorMessage: str


###############################################################################
# FUNCTIONS
###############################################################################
def download(token: str, query_id: str) -> bytes:
    """2-step FlexQueryReport download process.

    Args:
        token: Current access token from Reports > Settings > FlexWeb Service.
        query_id: Flex Query ID from
                  Reports > Flex Queries > Custom Flex Queries > Configure.
    """
    stmt_access = request_statement(token, query_id)
    status = 0
    while status is not True:
        time.sleep(status)
        response = submit_request(
            url=stmt_access.Url or STMT_URL,
            token=token,
            query=stmt_access.ReferenceCode,
        )
        status = check_statement_response(response)
    return response.content


def request_statement(
    token: str, query_id: str, url: Optional[str] = None
) -> StatementAccess:
    """First part of the 2-step download process.
    """
    url = url or REQUEST_URL
    response = submit_request(url, token, query=query_id)
    stmt_access = parse_stmt_response(response)
    if isinstance(stmt_access, StatementError):
        raise ResponseCodeError(
            stmt_access.ErrorCode,
            stmt_access.ErrorMessage,
        )
    return stmt_access


def submit_request(url: str, token: str, query: str) -> requests.Response:
    """Post a query to an API access point, along with an authentication token.

    Retry with a progressive timeout window.
    """
    MAX_REQUESTS = 3
    TIMEOUT_INCREMENT = 5

    response = None
    req_count = 1
    while (not response):
        try:
            response = requests.get(
                url,
                params={"v": "3", "t": token, "q": query},
                headers={"user-agent": "Java"},
                timeout=req_count * TIMEOUT_INCREMENT,
            )
        except requests.exceptions.Timeout:
            if req_count >= MAX_REQUESTS:
                raise
            else:
                print("Request Timeout, re-sending...")
                req_count += 1

    return response


def parse_stmt_response(
    response: requests.Response
) -> Union[StatementAccess, StatementError]:
    """Read 1st step response; parse into StatementAccess or StatementError.
    """
    try:
        elem = ET.fromstring(response.content)
        assert elem.tag == 'FlexStatementResponse'

        timestamp = elem.attrib['timestamp']
        # Convert "EST"/"EDT" to UTC offset so datetime.strptime can understand
        tz = {'EST': '-0500', 'EDT': '-0400'}[timestamp[-3:]]
        timestamp = timestamp[:-3] + tz
        datetime_ = datetime.strptime(timestamp, '%d %B, %Y %I:%M %p %z')

        data = {child.tag: child.text for child in elem}
        status = data.pop("Status")
        assert status in {"Success", "Fail", "Warn"}
        Type = {
            "Success": StatementAccess,
            "Fail": StatementError,
            "Warn": StatementError,
        }[status]
        return Type(timestamp=datetime_, **data)  # type: ignore
    except Exception:
        raise BadResponseError(response=response)


def check_statement_response(response: requests.Response) -> Union[bool, int]:
    """Validate response received from 2nd step of download.

    Returns:
        True if `response` contains a FlexQueryResponse.
        Retry delay (seconds) if `response` is an error indicating that
            'please try again shortly' means 'within several seconds'.

    Raises:
        ResponseCodeError if `response` is any other kind of error.
        BadResponseError if we can't parse `response`.
    """
    #  FlexQueryResponses can be massive; avoid parsing them.
    resp_str = str(response.content)
    if 'FlexQueryResponse' in resp_str:
        return True
    elif 'FlexStatementResponse' in resp_str:
        try:
            error = parse_stmt_response(response)
            assert isinstance(error, StatementError)
        except Exception:
            raise BadResponseError(response)
        if error.ErrorCode in SERVER_BUSY:
            #  Statement generation in progress. Please try again shortly.
            return 5
        elif error.ErrorCode in CLIENT_THROTTLED:
            #  Too many requests have been made from this token. Please try again shortly.
            return 10
        else:
            raise ResponseCodeError(error.ErrorCode, error.ErrorMessage)
    else:
        raise BadResponseError(response)


##############################################################################
# CLI SCRIPT
###############################################################################
def main():
    from argparse import ArgumentParser
    description = 'Download Flex brokerage statement from Interactive Brokers'
    argparser = ArgumentParser(description=description)
    argparser.add_argument('--token', '-t', required=True,
                           help='Current Flex Web Service token')
    argparser.add_argument('--query', '-q', required=True,
                           help='Flex Query ID#')
    args = argparser.parse_args()

    statement = download(args.token, args.query)
    print(statement.decode())


if __name__ == '__main__':
    main()
