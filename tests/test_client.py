# coding: utf-8
""" Unit tests for ibflex.parser module """

import unittest
from unittest.mock import Mock, patch, call
import datetime
from io import BytesIO

import requests
from ibflex import client, parser, Types


RESPONSE_SUCCESS = (
    '<FlexStatementResponse timestamp="28 August, 2012 10:37 AM EDT">'
    '<Status>Success</Status>'
    '<ReferenceCode>1234567890</ReferenceCode>'
    '<Url>https://gdcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService.GetStatement</Url>'
    '</FlexStatementResponse>'
)


RESPONSE_FAIL = (
    '<FlexStatementResponse timestamp="28 August, 2012 10:37 AM EDT">'
    '<Status>Fail</Status>'
    '<ErrorCode>1012</ErrorCode>'
    '<ErrorMessage>Token has expired.</ErrorMessage>'
    '</FlexStatementResponse>'
)


FLEX_QUERY_RESPONSE = (
    '<FlexQueryResponse queryName="Test" type="AZ">'
    '<FlexStatements count="1">'
    '<FlexStatement accountId="U666777" fromDate="20070101" toDate="20071231" period="Foo" whenGenerated="20100505 12:30:45" />'
    '</FlexStatements>'
    '</FlexQueryResponse>'
)


def mock_response(*args, **kwargs) -> object:
    class MockResponse:
        def __init__(self, content: str):
            self._content = content

        @property
        def content(self) -> bytes:
            return bytes(self._content, encoding="utf8")

    params = kwargs["params"]
    token = params["t"]
    query = params["q"]

    if token == "DEADBEEF" and query == "0987654321":
        return MockResponse(RESPONSE_SUCCESS)
    elif token == "DEADBEEF" and query == "1234567890":
        return MockResponse(FLEX_QUERY_RESPONSE)

    return MockResponse(RESPONSE_FAIL)


@patch("requests.get", side_effect=requests.exceptions.Timeout)
class SubmitRequestTestCase(unittest.TestCase):
    def test_submit_request_retry(self, mock_requests_get):
        with self.assertRaises(requests.exceptions.Timeout):
            client.submit_request(
                url=client.REQUEST_URL,
                token="DEADBEEF",
                query="0987654321",
            )

        self.assertEqual(
            mock_requests_get.call_args_list,
            [
                call(
                    client.REQUEST_URL,
                    params={"v": "3", "t": "DEADBEEF", "q": "0987654321"},
                    headers={"user-agent": "Java"},
                    timeout=5,
                ),
                call(
                    client.REQUEST_URL,
                    params={"v": "3", "t": "DEADBEEF", "q": "0987654321"},
                    headers={"user-agent": "Java"},
                    timeout=10,
                ),
                call(
                    client.REQUEST_URL,
                    params={"v": "3", "t": "DEADBEEF", "q": "0987654321"},
                    headers={"user-agent": "Java"},
                    timeout=15,
                ),
            ],
        )


@patch("requests.get", side_effect=mock_response)
class RequestStatementTestCase(unittest.TestCase):
    def test_request_statement(self, mock_requests_get):
        #  `url` arg defaults to client.REQUEST_URL
        output = client.request_statement(
            token="DEADBEEF",
            query_id="0987654321",
        )

        mock_requests_get.assert_called_once_with(
            client.REQUEST_URL,
            params={"v": "3", "t": "DEADBEEF", "q": "0987654321"},
            headers={"user-agent": "Java"},
            timeout=5,
        )

        self.assertIsInstance(output, client.StatementAccess)
        self.assertEqual(
            output.timestamp,
            datetime.datetime(2012, 8, 28, 10, 37, tzinfo=datetime.timezone(
                datetime.timedelta(hours=-4)))
        )
        self.assertEqual(output.ReferenceCode, "1234567890")
        self.assertEqual(output.Url, client.STMT_URL)


@patch("requests.get", side_effect=mock_response)
class DownloadTestCase(unittest.TestCase):
    def test_request_statement(self, mock_requests_get: Mock):
        output = client.download(
            token="DEADBEEF",
            query_id="0987654321",
        )
        self.assertIsInstance(output, bytes)

        self.assertEqual(
            mock_requests_get.call_args_list,
            [
                call(
                    client.REQUEST_URL,
                    params={"v": "3", "t": "DEADBEEF", "q": "0987654321"},
                    headers={"user-agent": "Java"},
                    timeout=5,
                ),
                call(
                    client.STMT_URL,
                    params={"v": "3", "t": "DEADBEEF", "q": "1234567890"},
                    headers={"user-agent": "Java"},
                    timeout=5,
                ),
            ],
        )

        response = parser.parse(BytesIO(output))
        self.assertIsInstance(response, Types.FlexQueryResponse)


if __name__ == '__main__':
    unittest.main(verbosity=3)
