# coding: utf-8
"""
Download Flex queries without logging into Account Management web page.

https://www.interactivebrokers.com/en/software/am/am/reports/flex_web_service_version_3.htm
"""
# stdlib imports
import xml.etree.ElementTree as ET
from datetime import datetime
import time
import sys


# 3rd party imports
import requests
from ibflex import fields, schemata


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
    ('1003', 'Statement is not available.'),
    ('1004', 'Statement is incomplete at this time. Please try again shortly.'),
    ('1005', 'Settlement data is not ready at this time. Please try again shortly.'),
    ('1006', 'IFO P/L data is not ready at this time. Please try again shortly.'),
    ('1007', 'MTM P/L data is not ready at this time. Please try again shortly.'),
    ('1008', 'MTM and FIFO P/L data is not ready at this time. Please try again shortly.'),
    ('1009', 'The server is under heavy load. Statement could not be generated at this time. Please try again shortly.'),
    ('1010', 'Legacy Flex Queries are no longer supported. Please convert over to Activity Flex.'),
    ('1011', 'Service account is inactive.'),
    ('1012', 'Token has expired.'),
    ('1013', 'IP restriction.'),
    ('1014', 'Query is invalid.'),
    ('1015', 'Token is invalid.'),
    ('1016', 'Account in invalid.'),
    ('1017', 'Reference code is invalid.'),
    ('1018', 'Too many requests have been made from this token. Please try again shortly.'),
    ('1019', 'Statement generation in progress. Please try again shortly.'),
    ('1020', 'Invalid request or unable to validate request.'),
    ('1021', 'Statement could not be retrieved at this time. Please try again shortly.'),
]
ERROR_CODES, ERROR_MSGS = zip(*ERRORS)


class IbflexClientError(Exception):
    """ Base class for Exceptions defined in this module """
    pass


class BadResponseError(IbflexClientError):
    """
    Exception raised for malformed Flex response.
    """
    def __init__(self, status, response):
        self.status = status
        self.response = response
        display = "Bad response, status='{}':\n\n {}".format(status, response)
        super(BadResponseError, self).__init__(display)


class ResponseCodeError(IbflexClientError):
    """
    Exception raised when Flex server returns a response with an error code.
    """
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg
        display = "Code={}: {}".format(code, msg)
        super(ResponseCodeError, self).__init__(display)


###############################################################################
# SCHEMATA
###############################################################################
class TextSchema(metaclass=schemata.SchemaMetaclass):
    """
    Base schema class where data is in text not attributes.
    """
    @classmethod
    def convert(cls, elem):
        output = {field.tag: cls.fields[field.tag].convert(field.text)
                  for field in elem}
        return output


class ResponseSuccessSchema(TextSchema):
    Status = fields.OneOf('Success', 'Fail', 'Warn', required=True)
    ReferenceCode = fields.String(required=True)
    Url = fields.String(required=True)


class ResponseFailureSchema(TextSchema):
    Status = fields.OneOf('Success', 'Fail', 'Warn', required=True)
    ErrorCode = fields.OneOf(*ERROR_CODES, required=True)
    ErrorMessage = fields.OneOf(*ERROR_MSGS, required=True)


ResponseSchemata = {'Success': ResponseSuccessSchema,
                    'Fail': ResponseFailureSchema}


###############################################################################
# FUNCTIONS
###############################################################################
def requests_get_timeout(url, token, query_id):
    response = None
    req_count = 1
    while(not response):
        try:
            response = requests.get(url,
                                    params={'v': '3', 't': token, 'q': query_id},
                                    headers={'user-agent': 'Java'},
                                    timeout=5*req_count)
        except requests.exceptions.Timeout:
            if(req_count<3):
                req_count += 1
                print('Request Timeout, re-sending...')
            else:
                sys.exit('Request Timeout, exiting.')

    return response


def send_request(token, query_id, url=None):
    url = url or REQUEST_URL
    response = requests_get_timeout(url, token, query_id)
    response = ET.fromstring(response.content)
    assert response.tag == 'FlexStatementResponse'
    timestamp = response.attrib['timestamp']
    # Convert "EST"/"EDT" to UTC offset so datetime.strptime can understand
    tz = {'EST': '-0500', 'EDT': '-0400'}[timestamp[-3:]]
    timestamp = timestamp[:-3] + tz

    timestamp = datetime.strptime(timestamp, '%d %B, %Y %I:%M %p %z')

    status = response.find('Status')
    if status is None:
        raise BadResponseError(status=status, response=response)
    schema = ResponseSchemata.get(status.text, None)
    if schema is None:
        raise BadResponseError(status=status, response=response)
    output = schema.convert(response)
    output['timestamp'] = timestamp
    return output


def get_statement(token, reference_code, url=None):
    url = url or STMT_URL
    statement = requests_get_timeout(url, token, reference_code)
    return statement.content


def download(token, query_id):
    response = send_request(token, query_id)
    status = response['Status']
    if status == 'Success':
        reference_code = response['ReferenceCode']
        url = response['Url']
        ready = False
        while not ready:
            response = get_statement(token, reference_code, url)
            resp_str = str(response)
            try:
                if 'FlexQueryResponse' in resp_str:
                    ready = True
                elif 'FlexStatementResponse' in resp_str:
                    output = ResponseFailureSchema.convert(ET.fromstring(response))
                    raise ResponseCodeError(code=output['ErrorCode'],
                                            msg=output['ErrorMessage'])
                else:
                    raise BadResponseError(status=status, response=response)
            except ResponseCodeError as err:
                if err.code in ('1019',):
                    time.sleep(5)
                elif err.code in ('1018',):
                    time.sleep(10)
                else:
                    raise
        return response
    elif status == 'Fail':
        raise ResponseCodeError(code=response['ErrorCode'],
                                msg=response['ErrorMessage'])
    else:
        raise BadResponseError(status=status, response=response)


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
