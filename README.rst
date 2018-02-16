=========================================================
Python parser for Interactive Brokers Flex XML statements
=========================================================

``ibflex`` is a Python library for converting brokerage statement data in
Interactive Brokers' Flex XML format into standard Python data structures,
so it can be conveniently processed and analyzed with Python scripts.

*N.B. This module has nothing to do with programmatic trading.
It's about accounting.*

``ibflex`` is compatible with Python version 3.4+.  The parser has no
dependencies beyond the Python standard library (although the optional client
for fetching Flex Statements from Interactive Brokers' server does depend
on `requests`_ ).

**This module is alpha software!**  It works and it's useful, but the
API, data structures, etc. are likely to see major changes.  Several XML
schemata are missing, and a few of the more newly-introduced attributes
for the existing schemata.  There are probably bugs.

`Pull requests`_ are welcome.


Installation
============
::

    pip install ibflex


Flex Parser
===========
The primary facility provided is the ``ibflex.parser`` module, which parses
Flex-format XML data,  converts the parsed data into normal Python types
(e.g. datetime.datetime, list), and exposes them as a nested dictionary whose
structure corresponds to that of the original Flex statements.

Usage example:

.. code:: python

    In [1]: from ibflex import parser

    In [2]: with open('/home/user/Downloads/2017-08_ibkr.xml', 'r') as xmlfile:
       ...:     response = parser.parse(xmlfile)
       ...:

    In [3]: stmt = response['FlexStatements'][0]

    In [4]: trades = stmt['Trades']

    In [5]: {k:v for k,v in trades[-1] if v is not None}
    Out[5]:
    {'accountId': 'U1111111',
     'acctAlias': 'Test Account',
     'assetCategory': 'STK',
     'buySell': 'BUY',
     'changeInPrice': Decimal('0'),
     'changeInQuantity': Decimal('0'),
     'closePrice': Decimal('4.66'),
     'conid': '148510778',
     'cost': Decimal('369.3162058'),
     'currency': 'USD',
     'description': 'HC2 HOLDINGS INC',
     'exchOrderId': 'N/A',
     'exchange': 'NYSE',
     'extExecID': 'L|AAA 9683/08152017|0000100001',
     'fifoPnlRealized': Decimal('0'),
     'fxPnl': Decimal('0'),
     'fxRateToBase': Decimal('1'),
     'ibCommission': Decimal('-0.5162058'),
     'ibCommissionCurrency': 'USD',
     'ibExecID': '0000e352.5992e388.01.01',
     'ibOrderID': '931273568',
     'isAPIOrder': False,
     'levelOfDetail': 'EXECUTION',
     'mtmPnl': Decimal('4'),
     'multiplier': Decimal('1'),
     'netCash': Decimal('-369.3162058'),
     'notes': ['P'],
     'openCloseIndicator': 'O',
     'orderTime': datetime.datetime(2017, 8, 15, 11, 53, 18),
     'orderType': 'LMT',
     'origOrderID': '0',
     'origTradePrice': Decimal('0'),
     'proceeds': Decimal('-368.8'),
     'quantity': Decimal('80'),
     'reportDate': datetime.date(2017, 8, 15),
     'settleDateTarget': datetime.date(2017, 8, 18),
     'symbol': 'HCHC',
     'taxes': Decimal('0'),
     'tradeDate': datetime.date(2017, 8, 15),
     'tradeID': '1885957768',
     'tradeMoney': Decimal('368.8'),
     'tradePrice': Decimal('4.61'),
     'tradeTime': datetime.time(11, 53, 18),
     'transactionID': '7933669307',
     'transactionType': 'ExchTrade'}
    

Flex Data Format
================
Generate Flex statements through `Interactive Brokers account management`_ .
Reports > Activities > Flex Queries

``ibflex`` is designed to parse whatever you throw at it without additional
configuration, with one major shortcoming: without providing additional
information out of band, it is difficult to distinguish US-style date
formats (mm/dd) from European-style date formats (dd/mm).

** DO YOURSELF A FAVOR: CONFIGURE FLEX QUERIES TO USE ISO8601 EXTENDED FORMATS
FOR DATE (YYYY-mm-dd) AND TIME (HH:MM:SS) **


Flex Client
===========
Once you've defined various Flex queries, you can generate an access token
that will allow you to generate statements and download them through the web
API, instead of logging in to get them.

Reports > Settings > FlexWeb Service

Once you've got that set up - armed with the token, and the ID# of the desired
Flex query - ``ibflex.client`` contains the facilities necessary to retrieve
them:

.. code:: python

    In [1]: from ibflex import client

    In [2]: token = '111111111111111111111111'

    In [3]: query_id = '111111'

    In [4]: response = client.download(token, query_id)

    In [5]: response[:215]
    Out[5]: b'<FlexQueryResponse queryName="Get Everything" type="AF">\n<FlexStatements count="1">\n<FlexStatement accountId="U111111" fromDate="2018-01-01" toDate="2018-01-31" period="LastMonth" whenGenerated="2018-02-01;211353">\n'


You can also just execute client.main() as a script:

.. code:: bash

    $ python client.py -t 111111111111111111111111 -q 111111 > 2018-01_ibkr.xml


Finally, setup.py installs a script at ``~/.local/bin/flexget``... cron-tastic!

.. code:: bash

    $ flexget -t 111111111111111111111111 -q 111111 > 2018-01_ibkr.xml


Resources
=========
* Interactive Brokers `Activity Flex Query Reference`_
* Interactive Brokers `FlexWeb Service Reference`_
* `capgains`_ - package that uses ibflex (inter alia) to calculate realized gains
* `ib-flex-analyzer`_ - Analyze your Interactive Brokers Flex XML reports with pandas

.. _Pull requests: https://github.com/csingley/ibflex/pull/new/master
.. _requests: https://github.com/requests/requests
.. _Interactive Brokers account management: https://gdcdyn.interactivebrokers.com/sso/Login 
.. _Activity Flex Query Reference: https://www.interactivebrokers.com/en/software/reportguide/reportguide.htm#reportguide/activity_flex_query_reference.htm
.. _FlexWeb Service Reference: https://www.interactivebrokers.com/en/software/am/am/reports/flex_web_service_version_3.htm
.. _capgains: https://github.com/csingley/capgains
.. _ib-flex-analyzer: https://github.com/wesm/ib-flex-analyzer
