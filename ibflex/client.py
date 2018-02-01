# coding: utf-8
"""
Download Flex queries without logging into Account Management web page.

https://www.interactivebrokers.com/en/software/am/am/reports/flex_web_service_version_3.htm
"""
# stdlib imports
import xml.etree.ElementTree as ET
from datetime import datetime
import time


# 3rd party imports
import requests
from ibflex import fields, schemata


FLEX_URL = 'https://gdcdyn.interactivebrokers.com/Universal/servlet/'
REQUEST_URL = FLEX_URL + 'FlexStatementService.SendRequest'
STMT_URL = FLEX_URL + 'FlexStatementService.GetStatement'

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


def send_request(token, query_id, url=None):
    url = url or REQUEST_URL
    response = requests.get(url,
                            params={'v': '3', 't': token, 'q': query_id},
                            headers={'user-agent': 'Java'},
                           )
    response = ET.fromstring(response.content)
    assert response.tag == 'FlexStatementResponse'
    timestamp = response.attrib['timestamp']
    # Convert "EST"/"EDT" to UTC offset so datetime.strptime can understand
    tz = {'EST': '-0500', 'EDT': '-0400'}[timestamp[-3:]]
    timestamp = timestamp[:-3] + tz

    timestamp = datetime.strptime(timestamp, '%d %B, %Y %I:%M %p %z')

    status = response.find('Status')
    schema = ResponseSchemata.get(status.text, None)
    if status is None:
        raise ValueError  # FIXME
    output = schema.convert(response)
    output['timestamp'] = timestamp
    return output


def get_statement(token, reference_code, url=None):
    url = url or STMT_URL
    statement = requests.get(url,
                             params={'v': '3', 't': token, 'q': reference_code},
                             headers={'user-agent': 'Java'},
                            )
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
            if 'FlexQueryResponse' in resp_str:
                ready = True
            elif 'FlexStatementResponse' in resp_str:
                output = ResponseFailureSchema.convert(ET.fromstring(response))
                if output['ErrorCode'] in ('1019',):
                    time.sleep(5)
                elif output['ErrorCode'] in ('1018',):
                    time.sleep(10)
                else:
                    raise ValueError  # FIXME
            else:
                print(response)
                raise ValueError  # FIXME
        return response
    elif status == 'Fail':
        error_code = response['ErrorCode']
        error_msg = response['ErrorMessage']
        raise ValueError  # FIXME
    else:
        raise ValueError  # FIXME


##############################################################################
# CLI SCRIPT
###############################################################################
def main():
    from argparse import ArgumentParser
    description = 'Download Flex brokerage statement from Interactive Brokers'
    argparser = ArgumentParser(description=description)
    argparser.add_argument('--token', '-t',
                           help='Current Flex Web Service token')
    argparser.add_argument('--query', '-q', help='Flex Query ID#')
    args = argparser.parse_args()

    statement = download(args.token, args.query)
    print(statement)


if __name__ == '__main__':
    main()
