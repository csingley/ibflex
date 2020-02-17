=========================================================
Python parser for Interactive Brokers Flex XML statements
=========================================================

``ibflex`` is a Python library for converting brokerage statement data in
Interactive Brokers' Flex XML format into standard Python data structures,
so it can be conveniently processed and analyzed with Python scripts.

*N.B. This module has nothing to do with programmatic trading.
It's about reading brokerage reports.*

``ibflex`` is compatible with Python version 3.7+.  The parser has no
dependencies beyond the Python standard library (although the optional client
for fetching Flex Statements from Interactive Brokers' server does depend
on `requests`_ ).

**This module is alpha software!**  It works and it's useful, but the
API, data structures, etc. are likely to see major changes.  Several XML
schemata are missing, and a few of the more newly-introduced attributes
for the existing schemata.  There are probably bugs.

`Pull requests`_ are welcome.  If you're submitting a pull request for an updated
type, please do me a favor and include a test case based on your real-world data
(censored to remove any personal information) in `tests.test_types.py`.  You should
easily be able to cut&paste one of the existing `unittest.TestCase` subclasses in
that file and adapt it to your own data.  Thanks very much; my own datastream does
not have full coverage of the object model!


Installation
============
::

    pip install ibflex


Flex Parser
===========
The primary facility provided is the ``ibflex.parser`` module, which parses
Flex-format XML data into a hierarchy of Python objects whose structure
corresponds to that of the original Flex statements, with the data converted
into appropriate Python types (datetime.datetime, decimal.Decimal, etc.)

Usage example:

.. code:: python

    In [1]: from ibflex import parser

    In [2]: response = parser.parse("2017-01_ibkr.xml")

    In [3]: response
    Out[3]: FlexQueryResponse(queryName='SCP Everything', type='AF', len(FlexStatements)=1)

    In [4]: stmt = response.FlexStatements[0]

    In [5]: stmt
    Out[5]: FlexStatement(accountId='U770993', fromDate=datetime.date(2017, 1, 2), toDate=datetime.date(2017, 1, 31), period=None, whenGenerated=datetime.datetime(2017, 5, 10, 11, 41, 38), len(CashReport)=3, len(EquitySummaryInBase)=23, len(StmtFunds)=344, len(ChangeInPositionValues)=2, len(OpenPositions)=2140, len(FxPositions)=1, len(Trades)=339, len(CorporateActions)=1, len(CashTransactions)=4, len(InterestAccruals)=1, len(ChangeInDividendAccruals)=5, len(OpenDividendAccruals)=2, len(SecuritiesInfo)=30, len(ConversionRates)=550)

    In [6]: trade = stmt.Trades[-1]

    In [7]: trade
    Out[7]: Trade(transactionType=<TradeType.EXCHTRADE: 'ExchTrade'>, openCloseIndicator=<OpenClose.CLOSE: 'C'>, buySell=<BuySell.SELL: 'SELL'>, orderType=<OrderType.LIMIT: 'LMT'>, assetCategory=<AssetClass.STOCK: 'STK'>, accountId='U770993', currency='USD', fxRateToBase=Decimal('1'), symbol='WMIH', description='WMIH CORP', conid='105068604', cusip=None, isin=None, listingExchange=None, multiplier=Decimal('1'), strike=None, expiry=None, putCall=None, tradeID='1742757182', reportDate=datetime.date(2017, 1, 30), tradeDate=datetime.date(2017, 1, 30), tradeTime=datetime.time(15, 39, 36), settleDateTarget=datetime.date(2017, 2, 2), exchange='BYX', quantity=Decimal('-8'), tradePrice=Decimal('1.4'), tradeMoney=Decimal('-11.2'), taxes=Decimal('0'), ibCommission=Decimal('-0.00680792'), ibCommissionCurrency='USD', netCash=Decimal('11.19319208'), netCashInBase=None, closePrice=Decimal('1.4'), notes=(<Code.PARTIAL: 'P'>,), cost=Decimal('-10.853621'), mtmPnl=Decimal('0'), origTradePrice=Decimal('0'), origTradeDate=None, origTradeID=None, origOrderID='0', openDateTime=None, fifoPnlRealized=Decimal('0.339571'), capitalGainsPnl=None, levelOfDetail='EXECUTION', ibOrderID='865480117', orderTime=datetime.datetime(2017, 1, 30, 15, 39, 36), changeInPrice=Decimal('0'), changeInQuantity=Decimal('0'), proceeds=Decimal('11.2'), fxPnl=Decimal('0'), clearingFirmID=None, transactionID='7248583136', holdingPeriodDateTime=None, ibExecID='0001090f.588f449a.01.01', brokerageOrderID=None, orderReference=None, volatilityOrderLink=None, exchOrderId=None, extExecID='S2367553204796', traderID=None, isAPIOrder=False, acctAlias='SCP 0-0', model=None, securityID=None, securityIDType=None, principalAdjustFactor=None, dateTime=None, underlyingConid=None, underlyingSecurityID=None, underlyingSymbol=None, underlyingListingExchange=None, issuer=None, sedol=None, whenRealized=None, whenReopened=None)

    In [8]: print(f"{trade.tradeDate} {trade.buySell.name} {abs(trade.quantity)} {trade.symbol} @ {trade.tradePrice} {trade.currency}")
    2017-01-30 SELL 8 WMIH @ 1.4 USD

    In [9]: pos = stmt.OpenPositions[-1]

    In [10]: pos
    Out[10]: OpenPosition(side=<LongShort.SHORT: 'Short'>, assetCategory=<AssetClass.STOCK: 'STK'>, accountId='U770993', currency='USD', fxRateToBase=Decimal('1'), reportDate=datetime.date(2017, 1, 31), symbol='VXX', description='IPATH S&P 500 VIX S/T FU ETN', conid='242500577', securityID=None, cusip=None, isin=None, multiplier=Decimal('1'), position=Decimal('-75'), markPrice=Decimal('19.42'), positionValue=Decimal('-1456.5'), openPrice=Decimal('109.210703693'), costBasisPrice=Decimal('109.210703693'), costBasisMoney=Decimal('-8190.802777'), fifoPnlUnrealized=Decimal('6734.302777'), levelOfDetail='LOT', openDateTime=datetime.datetime(2015, 8, 24, 9, 28, 9), holdingPeriodDateTime=datetime.datetime(2015, 8, 24, 9, 28, 9), securityIDType=None, issuer=None, underlyingConid=None, underlyingSymbol=None, code=(), originatingOrderID='699501861', originatingTransactionID='5634129129', accruedInt=None, acctAlias='SCP 0-0', model=None, sedol=None, percentOfNAV=None, strike=None, expiry=None, putCall=None, principalAdjustFactor=None, listingExchange=None, underlyingSecurityID=None, underlyingListingExchange=None, positionValueInBase=None, unrealizedCapitalGainsPnl=None, unrealizedlFxPnl=None)

    In [11]: print(f"{trade.tradeDate} {trade.buySell.name} {abs(trade.quantity)} {trade.symbol} @ {trade.tradePrice} {trade.currency}")
    2017-01-30 SELL 8 WMIH @ 1.4 USD

    In [12]: [sec for sec in stmt.SecuritiesInfo if sec.conid == trade.conid][0]
    Out[12]: SecurityInfo(assetCategory=<AssetClass.STOCK: 'STK'>, symbol='WMIH', description='WMIH CORP', conid='105068604', securityID=None, cusip=None, isin=None, listingExchange=None, underlyingSecurityID=None, underlyingListingExchange=None, underlyingConid=None, underlyingCategory=None, subCategory=None, multiplier=Decimal('1'), strike=None, expiry=None, maturity=None, issueDate=None, type=None, sedol=None, securityIDType=None, underlyingSymbol=None, issuer=None, putCall=None, principalAdjustFactor=Decimal('1'), code=())


Flex Query Report Configuration
===============================
Configure Flex statements through `Interactive Brokers account management`_ .
Reports > Flex Queries > Custom Flex Queries > Configure

You can configure whatever you like and ibflex should parse it, with these exceptions:

    * You can't use European-style date formats (dd/MM/yy or dd/MM/yyyy).
      Just accept the default (yyyyMMdd) or get with the program and use ISO-8601 (yyyy-MM-dd).

    * You should use some delimiter between dates & times. The default delimiter
      (semicolon) is fastest to process.

    * For the Trades section of the statement, you can't select the options at the
      top for "Symbol Summary", "Asset Class", or "Orders".  These will blow up
      the parser.  It's fine to check the box for "Asset Class" down below, along
      with the other selections for XML attributes.


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
