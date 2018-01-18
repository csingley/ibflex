# coding: utf-8
""" Unit tests for ibflex.schemata module """
# stdlib imports
import unittest
import xml.etree.ElementTree as ET
import datetime
import decimal


# local imports
from ibflex import schemata, fields


class SchemaTestCase(unittest.TestCase):
    def setUp(self):
        class TestMixin(object):
            boolean = fields.Boolean()

        class TestSchema(schemata.Schema, TestMixin):
            string = fields.String(required=True)
            integer = fields.Integer()

        self.schema = TestSchema

    def testMetaclass(self):
        self.assertTrue(hasattr(self.schema, 'fields'))
        fields_ = self.schema.fields
        self.assertIsInstance(fields_, dict)
        self.assertEqual(len(fields_), 3)

        self.assertIn('string', fields_)
        string = fields_['string']
        self.assertIsInstance(string, fields.String)
        self.assertTrue(string.required)

        self.assertIn('integer', fields_)
        integer = fields_['integer']
        self.assertIsInstance(integer, fields.Integer)
        self.assertFalse(integer.required)

        self.assertIn('boolean', fields_)
        boolean = fields_['boolean']
        self.assertIsInstance(boolean, fields.Boolean)
        self.assertFalse(boolean.required)

    def testConvert(self):
        data = ET.fromstring("<Test string='foo' integer='23' boolean='Y' />")
        output = self.schema.convert(data)
        self.assertIsInstance(output, dict)
        self.assertEqual(len(output), 3)
        self.assertIn('string', output)
        string = output['string']
        self.assertIsInstance(string, str)
        self.assertEqual(string, 'foo')
        self.assertIn('integer', output)
        integer = output['integer']
        self.assertIsInstance(integer, int)
        self.assertEqual(integer, 23)
        self.assertIn('boolean', output)
        boolean = output['boolean']
        self.assertIsInstance(boolean, bool)
        self.assertEqual(boolean, True)

    def testRequired(self):
        data = ET.fromstring("<Test string='' integer='23' boolean='Y' />")
        with self.assertRaises(fields.FlexFieldError):
            self.schema.convert(data)

    def testNotRequired(self):
        data = ET.fromstring("<Test string='foo' integer='' boolean='' />")
        output = self.schema.convert(data)
        self.assertIsInstance(output, dict)
        self.assertEqual(len(output), 3)
        self.assertIn('string', output)
        string = output['string']
        self.assertIsInstance(string, str)
        self.assertEqual(string, 'foo')
        self.assertIn('integer', output)
        integer = output['integer']
        self.assertIs(integer, None)
        self.assertIn('boolean', output)
        boolean = output['boolean']
        self.assertIs(boolean, None)

    def testExtraDataNotInSchema(self):
        data = ET.fromstring(
            "<Test string='foo' integer='23' boolean='Y' bar='baz' />"
        )
        with self.assertRaises(schemata.FlexSchemaError):
            self.schema.convert(data)


class FlexQueryResponseTestCase(unittest.TestCase):
    schema = schemata.FlexQueryResponse
    data = ET.fromstring(
        """<FlexQueryResponse queryName="ibflex test" type="AF" />"""
    )

    def testConvert(self):
        output = self.schema.convert(self.data)
        self.assertIsInstance(output, dict)
        self.assertEqual(len(output), 2)
        self.assertIn('queryName', output)
        queryName = output['queryName']
        self.assertIsInstance(queryName, str)
        self.assertEqual(queryName, 'ibflex test')
        self.assertIn('type', output)
        type_ = output['type']
        self.assertIsInstance(type_, str)
        self.assertEqual(type_, 'AF')


class FlexStatementsTestCase(unittest.TestCase):
    schema = schemata.FlexStatements
    data = ET.fromstring("""<FlexStatements count="1" />""")

    def testConvert(self):
        output = self.schema.convert(self.data)
        self.assertIsInstance(output, dict)
        self.assertEqual(len(output), 1)
        self.assertIn('count', output)
        count = output['count']
        self.assertIsInstance(count, int)
        self.assertEqual(count, 1)


class FlexStatementTestCase(unittest.TestCase):
    schema = schemata.FlexStatement
    data = ET.fromstring(
        """<FlexStatement accountId="U123456" fromDate="2011-01-03" toDate="2011-12-30" period="" whenGenerated="2017-05-10;164137" />"""
    )

    def testConvert(self):
        output = self.schema.convert(self.data)
        self.assertIsInstance(output, dict)
        self.assertEqual(len(output), 5)
        self.assertIn('accountId', output)
        acctid = output['accountId']
        self.assertIsInstance(acctid, str)
        self.assertEqual(acctid, 'U123456')
        self.assertIn('fromDate', output)
        fromdate = output['fromDate']
        self.assertIsInstance(fromdate, datetime.date)
        self.assertEqual(fromdate, datetime.date(2011, 1, 3))
        self.assertIn('toDate', output)
        todate = output['toDate']
        self.assertIsInstance(todate, datetime.date)
        self.assertEqual(todate, datetime.date(2011, 12, 30))
        self.assertIn('period', output)
        period = output['period']
        self.assertIs(period, None)
        self.assertIn('whenGenerated', output)
        when = output['whenGenerated']
        self.assertIsInstance(when, datetime.datetime)
        self.assertEqual(when, datetime.datetime(2017, 5, 10, 16, 41, 37))


class EquitySummaryByReportDateInBaseTestCase(unittest.TestCase):
    schema = schemata.EquitySummaryByReportDateInBase
    data = ET.fromstring(
        """<EquitySummaryByReportDateInBase accountId="U123456" acctAlias="ibflex test" model="" reportDate="2011-12-30" cash="51.730909701" cashLong="51.730909701" cashShort="0" slbCashCollateral="0" slbCashCollateralLong="0" slbCashCollateralShort="0" stock="39.68" stockLong="44.68" stockShort="-46" slbDirectSecuritiesBorrowed="0" slbDirectSecuritiesBorrowedLong="0" slbDirectSecuritiesBorrowedShort="0" slbDirectSecuritiesLent="0" slbDirectSecuritiesLentLong="0" slbDirectSecuritiesLentShort="0" options="0" optionsLong="0" optionsShort="0" commodities="0" commoditiesLong="0" commoditiesShort="0" bonds="0" bondsLong="0" bondsShort="0" notes="0" notesLong="0" notesShort="0" funds="0" fundsLong="0" fundsShort="0" interestAccruals="-1111.05" interestAccrualsLong="0" interestAccrualsShort="-1111.05" softDollars="0" softDollarsLong="0" softDollarsShort="0" forexCfdUnrealizedPl="0" forexCfdUnrealizedPlLong="0" forexCfdUnrealizedPlShort="0" dividendAccruals="3299.79" dividendAccrualsLong="3299.79" dividendAccrualsShort="0" fdicInsuredBankSweepAccount="0" fdicInsuredBankSweepAccountLong="0" fdicInsuredBankSweepAccountShort="0" fdicInsuredAccountInterestAccruals="0" fdicInsuredAccountInterestAccrualsLong="0" fdicInsuredAccountInterestAccrualsShort="0" total="40.1509097" totalLong="44.2009097" totalShort="-46.05" />"""
    )

    def testConvert(self):
        output = self.schema.convert(self.data)
        self.assertIsInstance(output, dict)
        self.assertEqual(len(output), 55)

        self.assertEqual(output['accountId'], 'U123456')
        self.assertEqual(output['acctAlias'], "ibflex test")
        self.assertEqual(output['model'], None)
        self.assertEqual(output['reportDate'], datetime.date(2011, 12, 30))
        self.assertEqual(output['cash'], decimal.Decimal("51.730909701"))
        self.assertEqual(output['cashLong'], decimal.Decimal("51.730909701"))
        self.assertEqual(output['cashShort'], decimal.Decimal("0"))
        self.assertEqual(output['slbCashCollateral'], decimal.Decimal("0"))
        self.assertEqual(output['slbCashCollateralLong'], decimal.Decimal("0"))
        self.assertEqual(output['slbCashCollateralShort'], decimal.Decimal("0"))
        self.assertEqual(output['stock'], decimal.Decimal("39.68"))
        self.assertEqual(output['stockLong'], decimal.Decimal("44.68"))
        self.assertEqual(output['stockShort'], decimal.Decimal("-46"))
        self.assertEqual(output['slbDirectSecuritiesBorrowed'], decimal.Decimal("0"))
        self.assertEqual(output['slbDirectSecuritiesBorrowedLong'], decimal.Decimal("0"))
        self.assertEqual(output['slbDirectSecuritiesBorrowedShort'], decimal.Decimal("0"))
        self.assertEqual(output['slbDirectSecuritiesLent'], decimal.Decimal("0"))
        self.assertEqual(output['slbDirectSecuritiesLentLong'], decimal.Decimal("0"))
        self.assertEqual(output['slbDirectSecuritiesLentShort'], decimal.Decimal("0"))
        self.assertEqual(output['options'], decimal.Decimal("0"))
        self.assertEqual(output['optionsLong'], decimal.Decimal("0"))
        self.assertEqual(output['optionsShort'], decimal.Decimal("0"))
        self.assertEqual(output['commodities'], decimal.Decimal("0"))
        self.assertEqual(output['commoditiesLong'], decimal.Decimal("0"))
        self.assertEqual(output['commoditiesShort'], decimal.Decimal("0"))
        self.assertEqual(output['bonds'], decimal.Decimal("0"))
        self.assertEqual(output['bondsLong'], decimal.Decimal("0"))
        self.assertEqual(output['bondsShort'], decimal.Decimal("0"))
        self.assertEqual(output['notes'], decimal.Decimal("0"))
        self.assertEqual(output['notesLong'], decimal.Decimal("0"))
        self.assertEqual(output['notesShort'], decimal.Decimal("0"))
        self.assertEqual(output['funds'], decimal.Decimal("0"))
        self.assertEqual(output['fundsLong'], decimal.Decimal("0"))
        self.assertEqual(output['fundsShort'], decimal.Decimal("0"))
        self.assertEqual(output['interestAccruals'], decimal.Decimal("-1111.05"))
        self.assertEqual(output['interestAccrualsLong'], decimal.Decimal("0"))
        self.assertEqual(output['interestAccrualsShort'], decimal.Decimal("-1111.05"))
        self.assertEqual(output['softDollars'], decimal.Decimal("0"))
        self.assertEqual(output['softDollarsLong'], decimal.Decimal("0"))
        self.assertEqual(output['softDollarsShort'], decimal.Decimal("0"))
        self.assertEqual(output['forexCfdUnrealizedPl'], decimal.Decimal("0"))
        self.assertEqual(output['forexCfdUnrealizedPlLong'], decimal.Decimal("0"))
        self.assertEqual(output['forexCfdUnrealizedPlShort'], decimal.Decimal("0"))
        self.assertEqual(output['dividendAccruals'], decimal.Decimal("3299.79"))
        self.assertEqual(output['dividendAccrualsLong'], decimal.Decimal("3299.79"))
        self.assertEqual(output['dividendAccrualsShort'], decimal.Decimal("0"))
        self.assertEqual(output['fdicInsuredBankSweepAccount'], decimal.Decimal("0"))
        self.assertEqual(output['fdicInsuredBankSweepAccountLong'], decimal.Decimal("0"))
        self.assertEqual(output['fdicInsuredBankSweepAccountShort'], decimal.Decimal("0"))
        self.assertEqual(output['fdicInsuredAccountInterestAccruals'], decimal.Decimal("0"))
        self.assertEqual(output['fdicInsuredAccountInterestAccrualsLong'], decimal.Decimal("0"))
        self.assertEqual(output['fdicInsuredAccountInterestAccrualsShort'], decimal.Decimal("0"))
        self.assertEqual(output['total'], decimal.Decimal("40.1509097"))
        self.assertEqual(output['totalLong'], decimal.Decimal("44.2009097"))
        self.assertEqual(output['totalShort'], decimal.Decimal("-46.05"))


class CashReportCurrencyTestCase(unittest.TestCase):
    schema = schemata.CashReportCurrency
    data = ET.fromstring(
        """<CashReportCurrency accountId="U123456" acctAlias="ibflex test" model="" currency="USD" fromDate="2011-01-03" toDate="2011-12-30" startingCash="30.702569078" startingCashSec="30.702569078" startingCashCom="0" clientFees="0" clientFeesSec="0" clientFeesCom="0" commissions="-45.445684" commissionsSec="-45.445684" commissionsCom="0" billableCommissions="0" billableCommissionsSec="0" billableCommissionsCom="0" depositWithdrawals="10.62" depositWithdrawalsSec="10.62" depositWithdrawalsCom="0" deposits="13.62" depositsSec="13.62" depositsCom="0" withdrawals="-24" withdrawalsSec="-24" withdrawalsCom="0" accountTransfers="0" accountTransfersSec="0" accountTransfersCom="0" linkingAdjustments="0" linkingAdjustmentsSec="0" linkingAdjustmentsCom="0" internalTransfers="0" internalTransfersSec="0" internalTransfersCom="0" dividends="34.74" dividendsSec="34.74" dividendsCom="0" insuredDepositInterest="0" insuredDepositInterestSec="0" insuredDepositInterestCom="0" brokerInterest="-64.57" brokerInterestSec="-64.57" brokerInterestCom="0" bondInterest="0" bondInterestSec="0" bondInterestCom="0" cashSettlingMtm="0" cashSettlingMtmSec="0" cashSettlingMtmCom="0" realizedVm="0" realizedVmSec="0" realizedVmCom="0" cfdCharges="0" cfdChargesSec="0" cfdChargesCom="0" netTradesSales="19.608813" netTradesSalesSec="19.608813" netTradesSalesCom="0" netTradesPurchases="-33.164799999" netTradesPurchasesSec="-33.164799999" netTradesPurchasesCom="0" advisorFees="0" advisorFeesSec="0" advisorFeesCom="0" feesReceivables="0" feesReceivablesSec="0" feesReceivablesCom="0" paymentInLieu="-44.47" paymentInLieuSec="-44.47" paymentInLieuCom="0" transactionTax="0" transactionTaxSec="0" transactionTaxCom="0" taxReceivables="0" taxReceivablesSec="0" taxReceivablesCom="0" withholdingTax="-27.07" withholdingTaxSec="-27.07" withholdingTaxCom="0" withholding871m="0" withholding871mSec="0" withholding871mCom="0" withholdingCollectedTax="0" withholdingCollectedTaxSec="0" withholdingCollectedTaxCom="0" salesTax="0" salesTaxSec="0" salesTaxCom="0" fxTranslationGainLoss="0" fxTranslationGainLossSec="0" fxTranslationGainLossCom="0" otherFees="-521.22" otherFeesSec="-521.22" otherFeesCom="0" other="0" otherSec="0" otherCom="0" endingCash="51.730897778" endingCashSec="51.730897778" endingCashCom="0" endingSettledCash="51.730897778" endingSettledCashSec="51.730897778" endingSettledCashCom="0" />"""
    )

    def testConvert(self):
        output = self.schema.convert(self.data)
        self.assertIsInstance(output, dict)
        self.assertEqual(len(output), 159)

        self.assertEqual(output['accountId'], "U123456")
        self.assertEqual(output['acctAlias'], "ibflex test")
        self.assertEqual(output['model'], None)
        self.assertEqual(output['currency'], "USD")
        self.assertEqual(output['fromDate'], datetime.date(2011, 1, 3))
        self.assertEqual(output['toDate'], datetime.date(2011, 12, 30))
        self.assertEqual(output['startingCash'], decimal.Decimal("30.702569078"))
        self.assertEqual(output['startingCashSec'], decimal.Decimal("30.702569078"))
        self.assertEqual(output['startingCashCom'], decimal.Decimal("0"))
        self.assertEqual(output['clientFees'], decimal.Decimal("0"))
        self.assertEqual(output['clientFeesSec'], decimal.Decimal("0"))
        self.assertEqual(output['clientFeesCom'], decimal.Decimal("0"))
        self.assertEqual(output['commissions'], decimal.Decimal("-45.445684"))
        self.assertEqual(output['commissionsSec'], decimal.Decimal("-45.445684"))
        self.assertEqual(output['commissionsCom'], decimal.Decimal("0"))
        self.assertEqual(output['billableCommissions'], decimal.Decimal("0"))
        self.assertEqual(output['billableCommissionsSec'], decimal.Decimal("0"))
        self.assertEqual(output['billableCommissionsCom'], decimal.Decimal("0"))
        self.assertEqual(output['depositWithdrawals'], decimal.Decimal("10.62"))
        self.assertEqual(output['depositWithdrawalsSec'], decimal.Decimal("10.62"))
        self.assertEqual(output['depositWithdrawalsCom'], decimal.Decimal("0"))
        self.assertEqual(output['deposits'], decimal.Decimal("13.62"))
        self.assertEqual(output['depositsSec'], decimal.Decimal("13.62"))
        self.assertEqual(output['depositsCom'], decimal.Decimal("0"))
        self.assertEqual(output['withdrawals'], decimal.Decimal("-24"))
        self.assertEqual(output['withdrawalsSec'], decimal.Decimal("-24"))
        self.assertEqual(output['withdrawalsCom'], decimal.Decimal("0"))
        self.assertEqual(output['accountTransfers'], decimal.Decimal("0"))
        self.assertEqual(output['accountTransfersSec'], decimal.Decimal("0"))
        self.assertEqual(output['accountTransfersCom'], decimal.Decimal("0"))
        self.assertEqual(output['linkingAdjustments'], decimal.Decimal("0"))
        self.assertEqual(output['linkingAdjustmentsSec'], decimal.Decimal("0"))
        self.assertEqual(output['linkingAdjustmentsCom'], decimal.Decimal("0"))
        self.assertEqual(output['internalTransfers'], decimal.Decimal("0"))
        self.assertEqual(output['internalTransfersSec'], decimal.Decimal("0"))
        self.assertEqual(output['internalTransfersCom'], decimal.Decimal("0"))
        self.assertEqual(output['dividends'], decimal.Decimal("34.74"))
        self.assertEqual(output['dividendsSec'], decimal.Decimal("34.74"))
        self.assertEqual(output['dividendsCom'], decimal.Decimal("0"))
        self.assertEqual(output['insuredDepositInterest'], decimal.Decimal("0"))
        self.assertEqual(output['insuredDepositInterestSec'], decimal.Decimal("0"))
        self.assertEqual(output['insuredDepositInterestCom'], decimal.Decimal("0"))
        self.assertEqual(output['brokerInterest'], decimal.Decimal("-64.57"))
        self.assertEqual(output['brokerInterestSec'], decimal.Decimal("-64.57"))
        self.assertEqual(output['brokerInterestCom'], decimal.Decimal("0"))
        self.assertEqual(output['bondInterest'], decimal.Decimal("0"))
        self.assertEqual(output['bondInterestSec'], decimal.Decimal("0"))
        self.assertEqual(output['bondInterestCom'], decimal.Decimal("0"))
        self.assertEqual(output['cashSettlingMtm'], decimal.Decimal("0"))
        self.assertEqual(output['cashSettlingMtmSec'], decimal.Decimal("0"))
        self.assertEqual(output['cashSettlingMtmCom'], decimal.Decimal("0"))
        self.assertEqual(output['realizedVm'], decimal.Decimal("0"))
        self.assertEqual(output['realizedVmSec'], decimal.Decimal("0"))
        self.assertEqual(output['realizedVmCom'], decimal.Decimal("0"))
        self.assertEqual(output['cfdCharges'], decimal.Decimal("0"))
        self.assertEqual(output['cfdChargesSec'], decimal.Decimal("0"))
        self.assertEqual(output['cfdChargesCom'], decimal.Decimal("0"))
        self.assertEqual(output['netTradesSales'], decimal.Decimal("19.608813"))
        self.assertEqual(output['netTradesSalesSec'], decimal.Decimal("19.608813"))
        self.assertEqual(output['netTradesSalesCom'], decimal.Decimal("0"))
        self.assertEqual(output['netTradesPurchases'], decimal.Decimal("-33.164799999"))
        self.assertEqual(output['netTradesPurchasesSec'], decimal.Decimal("-33.164799999"))
        self.assertEqual(output['netTradesPurchasesCom'], decimal.Decimal("0"))
        self.assertEqual(output['advisorFees'], decimal.Decimal("0"))
        self.assertEqual(output['advisorFeesSec'], decimal.Decimal("0"))
        self.assertEqual(output['advisorFeesCom'], decimal.Decimal("0"))
        self.assertEqual(output['feesReceivables'], decimal.Decimal("0"))
        self.assertEqual(output['feesReceivablesSec'], decimal.Decimal("0"))
        self.assertEqual(output['feesReceivablesCom'], decimal.Decimal("0"))
        self.assertEqual(output['paymentInLieu'], decimal.Decimal("-44.47"))
        self.assertEqual(output['paymentInLieuSec'], decimal.Decimal("-44.47"))
        self.assertEqual(output['paymentInLieuCom'], decimal.Decimal("0"))
        self.assertEqual(output['transactionTax'], decimal.Decimal("0"))
        self.assertEqual(output['transactionTaxSec'], decimal.Decimal("0"))
        self.assertEqual(output['transactionTaxCom'], decimal.Decimal("0"))
        self.assertEqual(output['taxReceivables'], decimal.Decimal("0"))
        self.assertEqual(output['taxReceivablesSec'], decimal.Decimal("0"))
        self.assertEqual(output['taxReceivablesCom'], decimal.Decimal("0"))
        self.assertEqual(output['withholdingTax'], decimal.Decimal("-27.07"))
        self.assertEqual(output['withholdingTaxSec'], decimal.Decimal("-27.07"))
        self.assertEqual(output['withholdingTaxCom'], decimal.Decimal("0"))
        self.assertEqual(output['withholding871m'], decimal.Decimal("0"))
        self.assertEqual(output['withholding871mSec'], decimal.Decimal("0"))
        self.assertEqual(output['withholding871mCom'], decimal.Decimal("0"))
        self.assertEqual(output['withholdingCollectedTax'], decimal.Decimal("0"))
        self.assertEqual(output['withholdingCollectedTaxSec'], decimal.Decimal("0"))
        self.assertEqual(output['withholdingCollectedTaxCom'], decimal.Decimal("0"))
        self.assertEqual(output['salesTax'], decimal.Decimal("0"))
        self.assertEqual(output['salesTaxSec'], decimal.Decimal("0"))
        self.assertEqual(output['salesTaxCom'], decimal.Decimal("0"))
        self.assertEqual(output['fxTranslationGainLoss'], decimal.Decimal("0"))
        self.assertEqual(output['fxTranslationGainLossSec'], decimal.Decimal("0"))
        self.assertEqual(output['fxTranslationGainLossCom'], decimal.Decimal("0"))
        self.assertEqual(output['otherFees'], decimal.Decimal("-521.22"))
        self.assertEqual(output['otherFeesSec'], decimal.Decimal("-521.22"))
        self.assertEqual(output['otherFeesCom'], decimal.Decimal("0"))
        self.assertEqual(output['other'], decimal.Decimal("0"))
        self.assertEqual(output['otherSec'], decimal.Decimal("0"))
        self.assertEqual(output['otherCom'], decimal.Decimal("0"))
        self.assertEqual(output['endingCash'], decimal.Decimal("51.730897778"))
        self.assertEqual(output['endingCashSec'], decimal.Decimal("51.730897778"))
        self.assertEqual(output['endingCashCom'], decimal.Decimal("0"))
        self.assertEqual(output['endingSettledCash'], decimal.Decimal("51.730897778"))
        self.assertEqual(output['endingSettledCashSec'], decimal.Decimal("51.730897778"))
        self.assertEqual(output['endingSettledCashCom'], decimal.Decimal("0"))


class StatementOfFundsLineTestCase(unittest.TestCase):
    schema = schemata.StatementOfFundsLine
    data = ET.fromstring(
        """<StatementOfFundsLine accountId="U123456" acctAlias="ibflex test" model="" currency="USD" assetCategory="STK" symbol="ECRO" description="ECC CAPITAL CORP" conid="33205002" securityID="" securityIDType="" cusip="" isin="" underlyingConid="" underlyingSymbol="" issuer="" multiplier="1" strike="" expiry="" putCall="" principalAdjustFactor="" reportDate="2011-12-27" date="2011-12-27" activityDescription="Buy 38,900 ECC CAPITAL CORP " tradeID="657898717" debit="-3185.60925" credit="" amount="-3185.60925" balance="53409.186538632" buySell="BUY" />"""
    )

    def testConvert(self):
        output = self.schema.convert(self.data)
        self.assertIsInstance(output, dict)
        self.assertEqual(len(output), 29)

        self.assertEqual(output['accountId'], "U123456")
        self.assertEqual(output['acctAlias'], "ibflex test")
        self.assertEqual(output['model'], None)
        self.assertEqual(output['currency'], "USD")
        self.assertEqual(output['assetCategory'], "STK")
        self.assertEqual(output['symbol'], "ECRO")
        self.assertEqual(output['description'], "ECC CAPITAL CORP")
        self.assertEqual(output['conid'], "33205002")
        self.assertEqual(output['securityID'], None)
        self.assertEqual(output['securityIDType'], None)
        self.assertEqual(output['cusip'], None)
        self.assertEqual(output['isin'], None)
        self.assertEqual(output['underlyingConid'], None)
        self.assertEqual(output['underlyingSymbol'], None)
        self.assertEqual(output['issuer'], None)
        self.assertEqual(output['multiplier'], 1)
        self.assertEqual(output['strike'], None)
        self.assertEqual(output['expiry'], None)
        self.assertEqual(output['putCall'], None)
        self.assertEqual(output['principalAdjustFactor'], None)
        self.assertEqual(output['reportDate'], datetime.date(2011, 12, 27))
        self.assertEqual(output['date'], datetime.date(2011, 12, 27))
        self.assertEqual(output['activityDescription'], "Buy 38,900 ECC CAPITAL CORP ")
        self.assertEqual(output['tradeID'], "657898717")
        self.assertEqual(output['debit'], decimal.Decimal("-3185.60925"))
        self.assertEqual(output['credit'], None)
        self.assertEqual(output['amount'], decimal.Decimal("-3185.60925"))
        self.assertEqual(output['balance'], decimal.Decimal("53409.186538632"))
        self.assertEqual(output['buySell'], "BUY")


class ChangeInPositionValueTestCase(unittest.TestCase):
    schema = schemata.ChangeInPositionValue
    data = ET.fromstring(
        """<ChangeInPositionValue accountId="U123456" acctAlias="ibflex test" model="" currency="USD" assetCategory="STK" priorPeriodValue="18.57" transactions="14.931399999" mtmPriorPeriodPositions="-16.1077" mtmTransactions="-22.2354" corporateActions="-11.425" other="0" accountTransfers="94.18" linkingAdjustments="0" fxTranslationPnl="0" futurePriceAdjustments="0" settledCash="0" endOfPeriodValue="39.68" />"""
    )

    def testConvert(self):
        output = self.schema.convert(self.data)
        self.assertIsInstance(output, dict)
        self.assertEqual(len(output), 17)

        self.assertEqual(output['accountId'], "U123456")
        self.assertEqual(output['acctAlias'], "ibflex test")
        self.assertEqual(output['model'], None)
        self.assertEqual(output['currency'], "USD")
        self.assertEqual(output['assetCategory'], "STK")
        self.assertEqual(output['priorPeriodValue'], decimal.Decimal("18.57"))
        self.assertEqual(output['transactions'], decimal.Decimal("14.931399999"))
        self.assertEqual(output['mtmPriorPeriodPositions'], decimal.Decimal("-16.1077"))
        self.assertEqual(output['mtmTransactions'], decimal.Decimal("-22.2354"))
        self.assertEqual(output['corporateActions'], decimal.Decimal("-11.425"))
        self.assertEqual(output['other'], decimal.Decimal("0"))
        self.assertEqual(output['accountTransfers'], decimal.Decimal("94.18"))
        self.assertEqual(output['linkingAdjustments'], decimal.Decimal("0"))
        self.assertEqual(output['fxTranslationPnl'], decimal.Decimal("0"))
        self.assertEqual(output['futurePriceAdjustments'], decimal.Decimal("0"))
        self.assertEqual(output['settledCash'], decimal.Decimal("0"))
        self.assertEqual(output['endOfPeriodValue'], decimal.Decimal("39.68"))


class OpenPositionTestCase(unittest.TestCase):
    schema = schemata.OpenPosition
    data = ET.fromstring(
        """<OpenPosition accountId="U123456" acctAlias="ibflex test" model="" currency="USD" fxRateToBase="1" assetCategory="STK" symbol="VXX" description="IPATH S&amp;P 500 VIX S/T FU ETN" conid="80789235" securityID="" securityIDType="" cusip="" isin="" underlyingConid="" underlyingSymbol="" issuer="" multiplier="1" strike="" expiry="" putCall="" principalAdjustFactor="" reportDate="2011-12-30" position="-100" markPrice="35.53" positionValue="-3553" openPrice="34.405" costBasisPrice="34.405" costBasisMoney="-3440.5" percentOfNAV="" fifoPnlUnrealized="-112.5" side="Short" levelOfDetail="LOT" openDateTime="2011-08-08;134413" holdingPeriodDateTime="2011-08-08;134413" code="" originatingOrderID="308163094" originatingTransactionID="2368917073" accruedInt="" />"""
    )

    def testConvert(self):
        output = self.schema.convert(self.data)
        self.assertIsInstance(output, dict)
        self.assertEqual(len(output), 38)

        self.assertEqual(output['accountId'], "U123456")
        self.assertEqual(output['acctAlias'], "ibflex test")
        self.assertEqual(output['model'], None)
        self.assertEqual(output['currency'], "USD")
        self.assertEqual(output['fxRateToBase'], 1)
        self.assertEqual(output['assetCategory'], "STK")
        self.assertEqual(output['symbol'], "VXX")
        self.assertEqual(output['description'], "IPATH S&P 500 VIX S/T FU ETN")
        self.assertEqual(output['conid'], "80789235")
        self.assertEqual(output['securityID'], None)
        self.assertEqual(output['securityIDType'], None)
        self.assertEqual(output['cusip'], None)
        self.assertEqual(output['isin'], None)
        self.assertEqual(output['underlyingConid'], None)
        self.assertEqual(output['underlyingSymbol'], None)
        self.assertEqual(output['issuer'], None)
        self.assertEqual(output['multiplier'], 1)
        self.assertEqual(output['strike'], None)
        self.assertEqual(output['expiry'], None)
        self.assertEqual(output['putCall'], None)
        self.assertEqual(output['principalAdjustFactor'], None)
        self.assertEqual(output['reportDate'], datetime.date(2011, 12, 30))
        self.assertEqual(output['position'], decimal.Decimal("-100"))
        self.assertEqual(output['markPrice'], decimal.Decimal("35.53"))
        self.assertEqual(output['positionValue'], decimal.Decimal("-3553"))
        self.assertEqual(output['openPrice'], decimal.Decimal("34.405"))
        self.assertEqual(output['costBasisPrice'], decimal.Decimal("34.405"))
        self.assertEqual(output['costBasisMoney'], decimal.Decimal("-3440.5"))
        self.assertEqual(output['percentOfNAV'], None)
        self.assertEqual(output['fifoPnlUnrealized'], decimal.Decimal("-112.5"))
        self.assertEqual(output['side'], "Short")
        self.assertEqual(output['levelOfDetail'], "LOT")
        self.assertEqual(output['openDateTime'], datetime.datetime(2011, 8, 8, 13, 44, 13))
        self.assertEqual(output['holdingPeriodDateTime'],  datetime.datetime(2011, 8, 8, 13, 44, 13))
        self.assertEqual(output['code'], [])
        self.assertEqual(output['originatingOrderID'], "308163094")
        self.assertEqual(output['originatingTransactionID'], "2368917073")
        self.assertEqual(output['accruedInt'], None)


class FxLotTestCase(unittest.TestCase):
    schema = schemata.FxLot
    data = ET.fromstring(
        """<FxLot accountId="U123456" acctAlias="ibflex test" model="" assetCategory="CASH" reportDate="2013-12-31" functionalCurrency="USD" fxCurrency="CAD" quantity="0.000012" costPrice="1" costBasis="-0.000012" closePrice="0.94148" value="0.000011" unrealizedPL="-0.000001" code="" lotDescription="CASH: -0.0786 USD.CAD" lotOpenDateTime="2011-01-25;180427" levelOfDetail="LOT" />"""
    )

    def testConvert(self):
        output = self.schema.convert(self.data)
        self.assertIsInstance(output, dict)
        self.assertEqual(len(output), 17)

        self.assertEqual(output['accountId'], "U123456")
        self.assertEqual(output['acctAlias'], "ibflex test")
        self.assertEqual(output['model'], None)
        self.assertEqual(output['assetCategory'], "CASH")
        self.assertEqual(output['reportDate'], datetime.date(2013, 12, 31))
        self.assertEqual(output['functionalCurrency'], "USD")
        self.assertEqual(output['fxCurrency'], "CAD")
        self.assertEqual(output['quantity'], decimal.Decimal("0.000012"))
        self.assertEqual(output['costPrice'], decimal.Decimal("1"))
        self.assertEqual(output['costBasis'], decimal.Decimal("-0.000012"))
        self.assertEqual(output['closePrice'], decimal.Decimal("0.94148"))
        self.assertEqual(output['value'], decimal.Decimal("0.000011"))
        self.assertEqual(output['unrealizedPL'], decimal.Decimal("-0.000001"))
        self.assertEqual(output['code'], [])
        self.assertEqual(output['lotDescription'], "CASH: -0.0786 USD.CAD")
        self.assertEqual(output['lotOpenDateTime'], datetime.datetime(2011, 1, 25, 18, 4, 27))
        self.assertEqual(output['levelOfDetail'], "LOT")


class TradeTestCase(unittest.TestCase):
    schema = schemata.Trade
    data = ET.fromstring(
        """<Trade accountId="U123456" acctAlias="ibflex test" model="" currency="USD" fxRateToBase="1" assetCategory="OPT" symbol="VXX   110917C00005000" description="VXX 17SEP11 5.0 C" conid="83615386" securityID="" securityIDType="" cusip="" isin="" underlyingConid="80789235" underlyingSymbol="VXX" issuer="" multiplier="100" strike="5" expiry="2011-09-17" putCall="C" principalAdjustFactor="" tradeID="594763148" reportDate="2011-08-12" tradeDate="2011-08-11" tradeTime="162000" settleDateTarget="2011-08-12" transactionType="BookTrade" exchange="--" quantity="3" tradePrice="0" tradeMoney="0" proceeds="-0" taxes="0" ibCommission="0" ibCommissionCurrency="USD" netCash="0" closePrice="29.130974" openCloseIndicator="C" notes="A" cost="8398.81122" fifoPnlRealized="0" fxPnl="0" mtmPnl="8739.2922" origTradePrice="0" origTradeDate="" origTradeID="" origOrderID="0" clearingFirmID="" transactionID="2381339439" buySell="BUY" ibOrderID="2381339439" ibExecID="" brokerageOrderID="" orderReference="" volatilityOrderLink="" exchOrderId="N/A" extExecID="N/A" orderTime="" openDateTime="" holdingPeriodDateTime="" whenRealized="" whenReopened="" levelOfDetail="EXECUTION" changeInPrice="0" changeInQuantity="0" orderType="" traderID="" isAPIOrder="N" />"""
    )

    def testConvert(self):
        output = self.schema.convert(self.data)
        self.assertIsInstance(output, dict)
        self.assertEqual(len(output), 68)

        self.assertEqual(output['accountId'], "U123456")
        self.assertEqual(output['acctAlias'], "ibflex test")
        self.assertEqual(output['model'], None)
        self.assertEqual(output['currency'], "USD")
        self.assertEqual(output['fxRateToBase'], decimal.Decimal('1'))
        self.assertEqual(output['assetCategory'], "OPT")
        self.assertEqual(output['symbol'], "VXX   110917C00005000")
        self.assertEqual(output['description'], "VXX 17SEP11 5.0 C")
        self.assertEqual(output['conid'], "83615386")
        self.assertEqual(output['securityID'], None)
        self.assertEqual(output['securityIDType'], None)
        self.assertEqual(output['cusip'], None)
        self.assertEqual(output['isin'], None)
        self.assertEqual(output['underlyingConid'], "80789235")
        self.assertEqual(output['underlyingSymbol'], "VXX")
        self.assertEqual(output['issuer'], None)
        self.assertEqual(output['multiplier'], decimal.Decimal('100'))
        self.assertEqual(output['strike'], decimal.Decimal('5'))
        self.assertEqual(output['expiry'], datetime.date(2011, 9, 17))
        self.assertEqual(output['putCall'], "C")
        self.assertEqual(output['principalAdjustFactor'], None)
        self.assertEqual(output['tradeID'], "594763148")
        self.assertEqual(output['reportDate'], datetime.date(2011, 8, 12))
        self.assertEqual(output['tradeDate'],  datetime.date(2011, 8, 11))
        self.assertEqual(output['tradeTime'], datetime.time(16, 20, 0))
        self.assertEqual(output['settleDateTarget'],  datetime.date(2011, 8, 12))
        self.assertEqual(output['transactionType'], "BookTrade")
        self.assertEqual(output['exchange'], "--")
        self.assertEqual(output['quantity'], decimal.Decimal("3"))
        self.assertEqual(output['tradePrice'], decimal.Decimal("0"))
        self.assertEqual(output['tradeMoney'], decimal.Decimal("0"))
        self.assertEqual(output['proceeds'], decimal.Decimal("-0"))
        self.assertEqual(output['taxes'], decimal.Decimal("0"))
        self.assertEqual(output['ibCommission'], decimal.Decimal("0"))
        self.assertEqual(output['ibCommissionCurrency'], "USD")
        self.assertEqual(output['netCash'], decimal.Decimal("0"))
        self.assertEqual(output['closePrice'], decimal.Decimal("29.130974"))
        self.assertEqual(output['openCloseIndicator'], "C")
        self.assertEqual(output['notes'], ["A", ])
        self.assertEqual(output['cost'], decimal.Decimal("8398.81122"))
        self.assertEqual(output['fifoPnlRealized'], decimal.Decimal("0"))
        self.assertEqual(output['fxPnl'], decimal.Decimal("0"))
        self.assertEqual(output['mtmPnl'], decimal.Decimal("8739.2922"))
        self.assertEqual(output['origTradePrice'], decimal.Decimal("0"))
        self.assertEqual(output['origTradeDate'], None)
        self.assertEqual(output['origTradeID'], None)
        self.assertEqual(output['origOrderID'], "0")
        self.assertEqual(output['clearingFirmID'], None)
        self.assertEqual(output['transactionID'], "2381339439")
        self.assertEqual(output['buySell'], "BUY")
        self.assertEqual(output['ibOrderID'], "2381339439")
        self.assertEqual(output['ibExecID'], None)
        self.assertEqual(output['brokerageOrderID'], None)
        self.assertEqual(output['orderReference'], None)
        self.assertEqual(output['volatilityOrderLink'], None)
        self.assertEqual(output['exchOrderId'], "N/A")
        self.assertEqual(output['extExecID'], "N/A")
        self.assertEqual(output['orderTime'], None)
        self.assertEqual(output['openDateTime'], None)
        self.assertEqual(output['holdingPeriodDateTime'], None)
        self.assertEqual(output['whenRealized'], None)
        self.assertEqual(output['whenReopened'], None)
        self.assertEqual(output['levelOfDetail'], "EXECUTION")
        self.assertEqual(output['changeInPrice'], decimal.Decimal("0"))
        self.assertEqual(output['changeInQuantity'], decimal.Decimal("0"))
        self.assertEqual(output['orderType'], None)
        self.assertEqual(output['traderID'], None)
        self.assertEqual(output['isAPIOrder'], False)


class OptionEAETestCase(unittest.TestCase):
    schema = schemata.OptionEAE
    data = ET.fromstring(
        """<OptionEAE accountId="U123456" acctAlias="ibflex test" model="" currency="USD" fxRateToBase="1" assetCategory="OPT" symbol="VXX   110805C00020000" description="VXX 05AUG11 20.0 C" conid="91900358" securityID="" securityIDType="" cusip="" isin="" underlyingConid="80789235" underlyingSymbol="VXX" issuer="" multiplier="100" strike="20" expiry="2011-08-05" putCall="C" principalAdjustFactor="" date="2011-08-05" transactionType="Assignment" quantity="20" tradePrice="0.0000" markPrice="0.0000" proceeds="0.00" commisionsAndTax="0.00" costBasis="21,792.73" realizedPnl="0.00" fxPnl="0.00" mtmPnl="20,620.00" tradeID="" />"""
    )

    def testConvert(self):
        output = self.schema.convert(self.data)
        self.assertIsInstance(output, dict)
        self.assertEqual(len(output), 33)

        self.assertEqual(output['accountId'], "U123456")
        self.assertEqual(output['acctAlias'], "ibflex test")
        self.assertEqual(output['model'], None)
        self.assertEqual(output['currency'], "USD")
        self.assertEqual(output['fxRateToBase'], decimal.Decimal("1"))
        self.assertEqual(output['assetCategory'], "OPT")
        self.assertEqual(output['symbol'], "VXX   110805C00020000")
        self.assertEqual(output['description'], "VXX 05AUG11 20.0 C")
        self.assertEqual(output['conid'], "91900358")
        self.assertEqual(output['securityID'], None)
        self.assertEqual(output['securityIDType'], None)
        self.assertEqual(output['cusip'], None)
        self.assertEqual(output['isin'], None)
        self.assertEqual(output['underlyingConid'], "80789235")
        self.assertEqual(output['underlyingSymbol'], "VXX")
        self.assertEqual(output['issuer'], None)
        self.assertEqual(output['multiplier'], decimal.Decimal("100"))
        self.assertEqual(output['strike'], decimal.Decimal("20"))
        self.assertEqual(output['expiry'], datetime.date(2011, 8, 5))
        self.assertEqual(output['putCall'], "C")
        self.assertEqual(output['principalAdjustFactor'], None)
        self.assertEqual(output['date'], datetime.date(2011, 8, 5))
        self.assertEqual(output['transactionType'], "Assignment")
        self.assertEqual(output['quantity'], decimal.Decimal("20"))
        self.assertEqual(output['tradePrice'], decimal.Decimal("0.0000"))
        self.assertEqual(output['markPrice'], decimal.Decimal("0.0000"))
        self.assertEqual(output['proceeds'], decimal.Decimal("0.00"))
        self.assertEqual(output['commisionsAndTax'], decimal.Decimal("0.00"))
        self.assertEqual(output['costBasis'], decimal.Decimal("21792.73"))
        self.assertEqual(output['realizedPnl'], decimal.Decimal("0.00"))
        self.assertEqual(output['fxPnl'], decimal.Decimal("0.00"))
        self.assertEqual(output['mtmPnl'], decimal.Decimal("20620.00"))
        self.assertEqual(output['tradeID'], None)


class TradeTransferTestCase(unittest.TestCase):
    schema = schemata.TradeTransfer
    data = ET.fromstring(
        """<TradeTransfer accountId="U123456" acctAlias="ibflex test" model="" currency="USD" fxRateToBase="1" assetCategory="STK" symbol="ADGI" description="ALLIED DEFENSE GROUP INC/THE" conid="764451" securityID="" securityIDType="" cusip="" isin="" underlyingConid="" underlyingSymbol="" issuer="" multiplier="1" strike="" expiry="" putCall="" principalAdjustFactor="" tradeID="599063639" reportDate="2011-08-22" tradeDate="2011-08-19" tradeTime="202000" settleDateTarget="2011-08-24" transactionType="DvpTrade" exchange="--" quantity="10000" tradePrice="3.1" tradeMoney="31000" proceeds="-31010" taxes="0" ibCommission="-1" ibCommissionCurrency="USD" netCash="-31011" closePrice="3.02" openCloseIndicator="O" notes="" cost="31011" fifoPnlRealized="0" fxPnl="0" mtmPnl="-810" origTradePrice="0" origTradeDate="" origTradeID="" origOrderID="0" clearingFirmID="94378" transactionID="" brokerName="E*Trade Clearing LLC" brokerAccount="1234-5678" awayBrokerCommission="10" regulatoryFee="0" direction="From" deliveredReceived="Received" netTradeMoney="31010" netTradeMoneyInBase="31010" netTradePrice="3.101" openDateTime="" holdingPeriodDateTime="" whenRealized="" whenReopened="" levelOfDetail="TRADE_TRANSFERS" />"""
    )

    def testConvert(self):
        output = self.schema.convert(self.data)
        self.assertIsInstance(output, dict)
        self.assertEqual(len(output), 63)

        self.assertEqual(output['accountId'], "U123456")
        self.assertEqual(output['acctAlias'], "ibflex test")
        self.assertEqual(output['model'], None)
        self.assertEqual(output['currency'], "USD")
        self.assertEqual(output['fxRateToBase'], decimal.Decimal('1'))
        self.assertEqual(output['assetCategory'], "STK")
        self.assertEqual(output['symbol'], "ADGI")
        self.assertEqual(output['description'], "ALLIED DEFENSE GROUP INC/THE")
        self.assertEqual(output['conid'], "764451")
        self.assertEqual(output['securityID'], None)
        self.assertEqual(output['securityIDType'], None)
        self.assertEqual(output['cusip'], None)
        self.assertEqual(output['isin'], None)
        self.assertEqual(output['underlyingConid'], None)
        self.assertEqual(output['underlyingSymbol'], None)
        self.assertEqual(output['issuer'], None)
        self.assertEqual(output['multiplier'], decimal.Decimal('1'))
        self.assertEqual(output['strike'], None)
        self.assertEqual(output['expiry'], None)
        self.assertEqual(output['putCall'], None)
        self.assertEqual(output['principalAdjustFactor'], None)
        self.assertEqual(output['tradeID'], "599063639")
        self.assertEqual(output['reportDate'], datetime.date(2011, 8, 22))
        self.assertEqual(output['tradeDate'], datetime.date(2011, 8, 19))
        self.assertEqual(output['tradeTime'], datetime.time(20,20, 0))
        self.assertEqual(output['settleDateTarget'], datetime.date(2011, 8, 24))
        self.assertEqual(output['transactionType'], "DvpTrade")
        self.assertEqual(output['exchange'], "--")
        self.assertEqual(output['quantity'], decimal.Decimal("10000"))
        self.assertEqual(output['tradePrice'], decimal.Decimal("3.1"))
        self.assertEqual(output['tradeMoney'], decimal.Decimal("31000"))
        self.assertEqual(output['proceeds'], decimal.Decimal("-31010"))
        self.assertEqual(output['taxes'], decimal.Decimal("0"))
        self.assertEqual(output['ibCommission'], decimal.Decimal("-1"))
        self.assertEqual(output['ibCommissionCurrency'], "USD")
        self.assertEqual(output['netCash'], decimal.Decimal("-31011"))
        self.assertEqual(output['closePrice'], decimal.Decimal("3.02"))
        self.assertEqual(output['openCloseIndicator'], "O")
        self.assertEqual(output['notes'], [])
        self.assertEqual(output['cost'], decimal.Decimal("31011"))
        self.assertEqual(output['fifoPnlRealized'], decimal.Decimal("0"))
        self.assertEqual(output['fxPnl'], decimal.Decimal("0"))
        self.assertEqual(output['mtmPnl'], decimal.Decimal("-810"))
        self.assertEqual(output['origTradePrice'], decimal.Decimal("0"))
        self.assertEqual(output['origTradeDate'], None)
        self.assertEqual(output['origTradeID'], None)
        self.assertEqual(output['origOrderID'], "0")
        self.assertEqual(output['clearingFirmID'], "94378")
        self.assertEqual(output['transactionID'], None)
        self.assertEqual(output['brokerName'], "E*Trade Clearing LLC")
        self.assertEqual(output['brokerAccount'], "1234-5678")
        self.assertEqual(output['awayBrokerCommission'], decimal.Decimal("10"))
        self.assertEqual(output['regulatoryFee'], decimal.Decimal("0"))
        self.assertEqual(output['direction'], "From")
        self.assertEqual(output['deliveredReceived'], "Received")
        self.assertEqual(output['netTradeMoney'], decimal.Decimal("31010"))
        self.assertEqual(output['netTradeMoneyInBase'], decimal.Decimal("31010"))
        self.assertEqual(output['netTradePrice'], decimal.Decimal("3.101"))
        self.assertEqual(output['openDateTime'], None)
        self.assertEqual(output['holdingPeriodDateTime'], None)
        self.assertEqual(output['whenRealized'], None)
        self.assertEqual(output['whenReopened'], None)
        self.assertEqual(output['levelOfDetail'], "TRADE_TRANSFERS")


class CashTransactionTestCase(unittest.TestCase):
    schema = schemata.CashTransaction
    data = ET.fromstring(
        """<CashTransaction accountId="U123456" acctAlias="ibflex test" model="" currency="USD" fxRateToBase="1" assetCategory="STK" symbol="RHDGF" description="RHDGF(ANN741081064) CASH DIVIDEND 1.00000000 USD PER SHARE (Return of Capital)" conid="62049667" securityID="ANN741081064" securityIDType="ISIN" cusip="" isin="ANN741081064" underlyingConid="" underlyingSymbol="" issuer="" multiplier="1" strike="" expiry="" putCall="" principalAdjustFactor="" dateTime="2015-10-06" amount="27800" type="Dividends" tradeID="" code="" transactionID="5767420360" reportDate="2015-10-06" clientReference="" />"""
    )

    def testConvert(self):
        output = self.schema.convert(self.data)
        self.assertIsInstance(output, dict)
        self.assertEqual(len(output), 29)

        self.assertEqual(output['accountId'], "U123456")
        self.assertEqual(output['acctAlias'], "ibflex test")
        self.assertEqual(output['model'], None)
        self.assertEqual(output['currency'], "USD")
        self.assertEqual(output['fxRateToBase'], decimal.Decimal("1"))
        self.assertEqual(output['assetCategory'], "STK")
        self.assertEqual(output['symbol'], "RHDGF")
        self.assertEqual(output['description'], "RHDGF(ANN741081064) CASH DIVIDEND 1.00000000 USD PER SHARE (Return of Capital)")
        self.assertEqual(output['conid'], "62049667")
        self.assertEqual(output['securityID'], "ANN741081064")
        self.assertEqual(output['securityIDType'], "ISIN")
        self.assertEqual(output['cusip'], None)
        self.assertEqual(output['isin'], "ANN741081064")
        self.assertEqual(output['underlyingConid'], None)
        self.assertEqual(output['underlyingSymbol'], None)
        self.assertEqual(output['issuer'], None)
        self.assertEqual(output['multiplier'], decimal.Decimal("1"))
        self.assertEqual(output['strike'], None)
        self.assertEqual(output['expiry'], None)
        self.assertEqual(output['putCall'], None)
        self.assertEqual(output['principalAdjustFactor'], None)
        self.assertEqual(output['dateTime'], datetime.date(2015, 10, 6))
        self.assertEqual(output['amount'], decimal.Decimal("27800"))
        self.assertEqual(output['type'], "Dividends")
        self.assertEqual(output['tradeID'], None)
        self.assertEqual(output['code'], [])
        self.assertEqual(output['transactionID'], "5767420360")
        self.assertEqual(output['reportDate'], datetime.date(2015,10, 6))
        self.assertEqual(output['clientReference'], None)


class InterestAccrualsCurrencyTestCase(unittest.TestCase):
    schema = schemata.InterestAccrualsCurrency
    data = ET.fromstring(
        """<InterestAccrualsCurrency accountId="U123456" acctAlias="ibflex test" model="" currency="BASE_SUMMARY" fromDate="2011-01-03" toDate="2011-12-30" startingAccrualBalance="-11.558825" interestAccrued="-7516.101776" accrualReversal="6416.624437" fxTranslation="-0.013836" endingAccrualBalance="-1111.05" />"""
    )

    def testConvert(self):
        output = self.schema.convert(self.data)
        self.assertIsInstance(output, dict)
        self.assertEqual(len(output), 11)

        self.assertEqual(output['accountId'], "U123456")
        self.assertEqual(output['acctAlias'], "ibflex test")
        self.assertEqual(output['model'], None)
        self.assertEqual(output['currency'], "BASE_SUMMARY")
        self.assertEqual(output['fromDate'], datetime.date(2011, 1, 3))
        self.assertEqual(output['toDate'], datetime.date(2011, 12, 30))
        self.assertEqual(output['startingAccrualBalance'], decimal.Decimal("-11.558825"))
        self.assertEqual(output['interestAccrued'], decimal.Decimal("-7516.101776"))
        self.assertEqual(output['accrualReversal'], decimal.Decimal("6416.624437"))
        self.assertEqual(output['fxTranslation'], decimal.Decimal("-0.013836"))
        self.assertEqual(output['endingAccrualBalance'], decimal.Decimal("-1111.05"))


class SLBActivityTestCase(unittest.TestCase):
    schema = schemata.SLBActivity
    data = ET.fromstring(
        """<SLBActivity accountId="U123456" acctAlias="ibflex test" model="" currency="USD" fxRateToBase="1" assetCategory="STK" symbol="CHTP.CVR" description="CHELSEA THERAPEUTICS INTERNA - ESCROW" conid="158060456" securityID="" securityIDType="" cusip="" isin="" underlyingConid="" underlyingSymbol="" issuer="" multiplier="1" strike="" expiry="" putCall="" principalAdjustFactor="" date="2015-06-01" slbTransactionId="SLB.32117554" activityDescription="New Loan Allocation" type="ManagedLoan" exchange="" quantity="-48330" feeRate="0.44" collateralAmount="48330" markQuantity="0" markPriorPrice="0" markCurrentPrice="0" />"""
    )

    def testConvert(self):
        output = self.schema.convert(self.data)
        self.assertIsInstance(output, dict)
        self.assertEqual(len(output), 32)

        self.assertEqual(output['accountId'], "U123456")
        self.assertEqual(output['acctAlias'], "ibflex test")
        self.assertEqual(output['model'], None)
        self.assertEqual(output['currency'], "USD")
        self.assertEqual(output['fxRateToBase'], decimal.Decimal("1"))
        self.assertEqual(output['assetCategory'], "STK")
        self.assertEqual(output['symbol'], "CHTP.CVR")
        self.assertEqual(output['description'], "CHELSEA THERAPEUTICS INTERNA - ESCROW")
        self.assertEqual(output['conid'], "158060456")
        self.assertEqual(output['securityID'], None)
        self.assertEqual(output['securityIDType'], None)
        self.assertEqual(output['cusip'], None)
        self.assertEqual(output['isin'], None)
        self.assertEqual(output['underlyingConid'], None)
        self.assertEqual(output['underlyingSymbol'], None)
        self.assertEqual(output['issuer'], None)
        self.assertEqual(output['multiplier'], decimal.Decimal("1"))
        self.assertEqual(output['strike'], None)
        self.assertEqual(output['expiry'], None)
        self.assertEqual(output['putCall'], None)
        self.assertEqual(output['principalAdjustFactor'], None)
        self.assertEqual(output['date'], datetime.date(2015, 6, 1))
        self.assertEqual(output['slbTransactionId'], "SLB.32117554")
        self.assertEqual(output['activityDescription'], "New Loan Allocation")
        self.assertEqual(output['type'], "ManagedLoan")
        self.assertEqual(output['exchange'], None)
        self.assertEqual(output['quantity'], decimal.Decimal("-48330"))
        self.assertEqual(output['feeRate'], decimal.Decimal("0.44"))
        self.assertEqual(output['collateralAmount'], decimal.Decimal("48330"))
        self.assertEqual(output['markQuantity'], decimal.Decimal("0"))
        self.assertEqual(output['markPriorPrice'], decimal.Decimal("0"))
        self.assertEqual(output['markCurrentPrice'], decimal.Decimal("0"))


class TransferTestCase(unittest.TestCase):
    schema = schemata.Transfer
    data = ET.fromstring(
        """<Transfer accountId="U123456" acctAlias="ibflex test" model="" currency="USD" fxRateToBase="1" assetCategory="STK" symbol="FMTIF" description="FMI HOLDINGS LTD" conid="86544467" securityID="" securityIDType="" cusip="" isin="" underlyingConid="" underlyingSymbol="" issuer="" multiplier="1" strike="" expiry="" putCall="" principalAdjustFactor="" date="2011-07-18" type="ACATS" direction="IN" company="--" account="12345678" accountName="" quantity="226702" transferPrice="0" positionAmount="11.51" positionAmountInBase="11.51" pnlAmount="0" pnlAmountInBase="0" fxPnl="0" cashTransfer="0" code="" clientReference="" />"""
    )

    def testConvert(self):
        output = self.schema.convert(self.data)
        self.assertIsInstance(output, dict)
        self.assertEqual(len(output), 37)

        self.assertEqual(output['accountId'], "U123456")
        self.assertEqual(output['acctAlias'], "ibflex test")
        self.assertEqual(output['model'], None)
        self.assertEqual(output['currency'], "USD")
        self.assertEqual(output['fxRateToBase'], decimal.Decimal("1"))
        self.assertEqual(output['assetCategory'], "STK")
        self.assertEqual(output['symbol'], "FMTIF")
        self.assertEqual(output['description'], "FMI HOLDINGS LTD")
        self.assertEqual(output['conid'], "86544467")
        self.assertEqual(output['securityID'], None)
        self.assertEqual(output['securityIDType'], None)
        self.assertEqual(output['cusip'], None)
        self.assertEqual(output['isin'], None)
        self.assertEqual(output['underlyingConid'], None)
        self.assertEqual(output['underlyingSymbol'], None)
        self.assertEqual(output['issuer'], None)
        self.assertEqual(output['multiplier'], decimal.Decimal("1"))
        self.assertEqual(output['strike'], None)
        self.assertEqual(output['expiry'], None)
        self.assertEqual(output['putCall'], None)
        self.assertEqual(output['principalAdjustFactor'], None)
        self.assertEqual(output['date'], datetime.date(2011, 7, 18))
        self.assertEqual(output['type'], "ACATS")
        self.assertEqual(output['direction'], "IN")
        self.assertEqual(output['company'], "--")
        self.assertEqual(output['account'], "12345678")
        self.assertEqual(output['accountName'], None)
        self.assertEqual(output['quantity'], decimal.Decimal("226702"))
        self.assertEqual(output['transferPrice'], decimal.Decimal("0"))
        self.assertEqual(output['positionAmount'], decimal.Decimal("11.51"))
        self.assertEqual(output['positionAmountInBase'], decimal.Decimal("11.51"))
        self.assertEqual(output['pnlAmount'], decimal.Decimal("0"))
        self.assertEqual(output['pnlAmountInBase'], decimal.Decimal("0"))
        self.assertEqual(output['fxPnl'], decimal.Decimal("0"))
        self.assertEqual(output['cashTransfer'], decimal.Decimal("0"))
        self.assertEqual(output['code'], [])
        self.assertEqual(output['clientReference'], None)


class CorporateActionTestCase(unittest.TestCase):
    schema = schemata.CorporateAction
    data = ET.fromstring(
        """<CorporateAction accountId="U123456" acctAlias="ibflex test" model="" currency="USD" fxRateToBase="1" assetCategory="STK" symbol="NILSY.TEN" description="NILSY.TEN(466992534) MERGED(Voluntary Offer Allocation)  FOR USD 30.60000000 PER SHARE (NILSY.TEN, MMC NORILSK NICKEL JSC-ADR - TENDER, 466992534)" conid="96835898" securityID="" securityIDType="" cusip="" isin="" underlyingConid="" underlyingSymbol="" issuer="" multiplier="1" strike="" expiry="" putCall="" principalAdjustFactor="" reportDate="2011-11-03" dateTime="2011-11-02;202500" amount="-30600" proceeds="30600" value="-18110" quantity="-1000" fifoPnlRealized="10315" mtmPnl="12490" code="" type="TC" />"""
    )

    def testConvert(self):
        output = self.schema.convert(self.data)
        self.assertIsInstance(output, dict)
        self.assertEqual(len(output), 31)

        self.assertEqual(output['accountId'], "U123456")
        self.assertEqual(output['acctAlias'], "ibflex test")
        self.assertEqual(output['model'], None)
        self.assertEqual(output['currency'], "USD")
        self.assertEqual(output['fxRateToBase'], decimal.Decimal("1"))
        self.assertEqual(output['assetCategory'], "STK")
        self.assertEqual(output['symbol'], "NILSY.TEN")
        self.assertEqual(output['description'], "NILSY.TEN(466992534) MERGED(Voluntary Offer Allocation)  FOR USD 30.60000000 PER SHARE (NILSY.TEN, MMC NORILSK NICKEL JSC-ADR - TENDER, 466992534)")
        self.assertEqual(output['conid'], "96835898")
        self.assertEqual(output['securityID'], None)
        self.assertEqual(output['securityIDType'], None)
        self.assertEqual(output['cusip'], None)
        self.assertEqual(output['isin'], None)
        self.assertEqual(output['underlyingConid'], None)
        self.assertEqual(output['underlyingSymbol'], None)
        self.assertEqual(output['issuer'], None)
        self.assertEqual(output['multiplier'], decimal.Decimal("1"))
        self.assertEqual(output['strike'], None)
        self.assertEqual(output['expiry'], None)
        self.assertEqual(output['putCall'], None)
        self.assertEqual(output['principalAdjustFactor'], None)
        self.assertEqual(output['reportDate'], datetime.date(2011, 11, 3))
        self.assertEqual(output['dateTime'], datetime.datetime(2011, 11, 2, 20, 25, 0))
        self.assertEqual(output['amount'], decimal.Decimal("-30600"))
        self.assertEqual(output['proceeds'], decimal.Decimal("30600"))
        self.assertEqual(output['value'], decimal.Decimal("-18110"))
        self.assertEqual(output['quantity'], decimal.Decimal("-1000"))
        self.assertEqual(output['fifoPnlRealized'], decimal.Decimal("10315"))
        self.assertEqual(output['mtmPnl'], decimal.Decimal("12490"))
        self.assertEqual(output['code'], [])
        self.assertEqual(output['type'], "TC")


class ChangeInDividendAccrualTestCase(unittest.TestCase):
    schema = schemata.ChangeInDividendAccrual
    data = ET.fromstring(
        """<ChangeInDividendAccrual accountId="U123456" acctAlias="ibflex test" model="" currency="USD" fxRateToBase="1" assetCategory="STK" symbol="RHDGF" description="RETAIL HOLDINGS NV" conid="62049667" securityID="ANN741081064" securityIDType="ISIN" cusip="" isin="ANN741081064" underlyingConid="" underlyingSymbol="" issuer="" multiplier="1" strike="" expiry="" putCall="" principalAdjustFactor="" date="2011-09-21" exDate="2011-09-22" payDate="2011-10-11" quantity="13592" tax="0" fee="0" grossRate="2.5" grossAmount="33980" netAmount="33980" code="Po" fromAcct="" toAcct="" />"""
    )

    def testConvert(self):
        output = self.schema.convert(self.data)
        self.assertIsInstance(output, dict)
        self.assertEqual(len(output), 33)

        self.assertEqual(output['accountId'], "U123456")
        self.assertEqual(output['acctAlias'], "ibflex test")
        self.assertEqual(output['model'], None)
        self.assertEqual(output['currency'], "USD")
        self.assertEqual(output['fxRateToBase'], decimal.Decimal("1"))
        self.assertEqual(output['assetCategory'], "STK")
        self.assertEqual(output['symbol'], "RHDGF")
        self.assertEqual(output['description'], "RETAIL HOLDINGS NV")
        self.assertEqual(output['conid'], "62049667")
        self.assertEqual(output['securityID'], "ANN741081064")
        self.assertEqual(output['securityIDType'], "ISIN")
        self.assertEqual(output['cusip'], None)
        self.assertEqual(output['isin'], "ANN741081064")
        self.assertEqual(output['underlyingConid'], None)
        self.assertEqual(output['underlyingSymbol'], None)
        self.assertEqual(output['issuer'], None)
        self.assertEqual(output['multiplier'], decimal.Decimal("1"))
        self.assertEqual(output['strike'], None)
        self.assertEqual(output['expiry'], None)
        self.assertEqual(output['putCall'], None)
        self.assertEqual(output['principalAdjustFactor'], None)
        self.assertEqual(output['date'], datetime.date(2011, 9, 21))
        self.assertEqual(output['exDate'], datetime.date(2011, 9, 22))
        self.assertEqual(output['payDate'], datetime.date(2011, 10, 11))
        self.assertEqual(output['quantity'], decimal.Decimal("13592"))
        self.assertEqual(output['tax'], decimal.Decimal("0"))
        self.assertEqual(output['fee'], decimal.Decimal("0"))
        self.assertEqual(output['grossRate'], decimal.Decimal("2.5"))
        self.assertEqual(output['grossAmount'], decimal.Decimal("33980"))
        self.assertEqual(output['netAmount'], decimal.Decimal("33980"))
        self.assertEqual(output['code'], ["Po"])
        self.assertEqual(output['fromAcct'], None)
        self.assertEqual(output['toAcct'], None)


class OpenDividendAccrualTestCase(unittest.TestCase):
    schema = schemata.OpenDividendAccrual
    data = ET.fromstring(
        """<OpenDividendAccrual accountId="U123456" acctAlias="ibflex test" model="" currency="USD" fxRateToBase="1" assetCategory="STK" symbol="CASH" description="META FINANCIAL GROUP INC" conid="3655441" securityID="" securityIDType="" cusip="" isin="" underlyingConid="" underlyingSymbol="" issuer="" multiplier="1" strike="" expiry="" putCall="" principalAdjustFactor="" exDate="2011-12-08" payDate="2012-01-01" quantity="25383" tax="0" fee="0" grossRate="0.13" grossAmount="3299.79" netAmount="3299.79" code="" fromAcct="" toAcct="" />"""
    )

    def testConvert(self):
        output = self.schema.convert(self.data)
        self.assertIsInstance(output, dict)
        self.assertEqual(len(output), 32)

        self.assertEqual(output['accountId'], "U123456")
        self.assertEqual(output['acctAlias'], "ibflex test")
        self.assertEqual(output['model'], None)
        self.assertEqual(output['currency'], "USD")
        self.assertEqual(output['fxRateToBase'], decimal.Decimal("1"))
        self.assertEqual(output['assetCategory'], "STK")
        self.assertEqual(output['symbol'], "CASH")
        self.assertEqual(output['description'], "META FINANCIAL GROUP INC")
        self.assertEqual(output['conid'], "3655441")
        self.assertEqual(output['securityID'], None)
        self.assertEqual(output['securityIDType'], None)
        self.assertEqual(output['cusip'], None)
        self.assertEqual(output['isin'], None)
        self.assertEqual(output['underlyingConid'], None)
        self.assertEqual(output['underlyingSymbol'], None)
        self.assertEqual(output['issuer'], None)
        self.assertEqual(output['multiplier'], decimal.Decimal("1"))
        self.assertEqual(output['strike'], None)
        self.assertEqual(output['expiry'], None)
        self.assertEqual(output['putCall'], None)
        self.assertEqual(output['principalAdjustFactor'], None)
        self.assertEqual(output['exDate'], datetime.date(2011, 12, 8))
        self.assertEqual(output['payDate'], datetime.date(2012, 1, 1))
        self.assertEqual(output['quantity'], decimal.Decimal("25383"))
        self.assertEqual(output['tax'], decimal.Decimal("0"))
        self.assertEqual(output['fee'], decimal.Decimal("0"))
        self.assertEqual(output['grossRate'], decimal.Decimal("0.13"))
        self.assertEqual(output['grossAmount'], decimal.Decimal("3299.79"))
        self.assertEqual(output['netAmount'], decimal.Decimal("3299.79"))
        self.assertEqual(output['code'], [])
        self.assertEqual(output['fromAcct'], None)
        self.assertEqual(output['toAcct'], None)


class SecurityInfoTestCase(unittest.TestCase):
    schema = schemata.SecurityInfo
    data = ET.fromstring(
        """<SecurityInfo assetCategory="STK" symbol="VXX" description="IPATH S&amp;P 500 VIX S/T FU ETN" conid="80789235" securityID="" securityIDType="" cusip="" isin="" underlyingConid="" underlyingSymbol="" issuer="" multiplier="1" strike="" expiry="" putCall="" principalAdjustFactor="1" maturity="" issueDate="" code="" />"""
    )

    def testConvert(self):
        output = self.schema.convert(self.data)
        self.assertIsInstance(output, dict)
        self.assertEqual(len(output), 19)

        self.assertEqual(output['assetCategory'], "STK")
        self.assertEqual(output['symbol'], "VXX")
        self.assertEqual(output['description'], "IPATH S&P 500 VIX S/T FU ETN")
        self.assertEqual(output['conid'], "80789235")
        self.assertEqual(output['securityID'], None)
        self.assertEqual(output['securityIDType'], None)
        self.assertEqual(output['cusip'], None)
        self.assertEqual(output['isin'], None)
        self.assertEqual(output['underlyingConid'], None)
        self.assertEqual(output['underlyingSymbol'], None)
        self.assertEqual(output['issuer'], None)
        self.assertEqual(output['multiplier'], decimal.Decimal("1"))
        self.assertEqual(output['strike'], None)
        self.assertEqual(output['expiry'], None)
        self.assertEqual(output['putCall'], None)
        self.assertEqual(output['principalAdjustFactor'], decimal.Decimal("1"))
        self.assertEqual(output['maturity'], None)
        self.assertEqual(output['issueDate'], None)
        self.assertEqual(output['code'], [])


class ConversionRateTestCase(unittest.TestCase):
    schema = schemata.ConversionRate
    data = ET.fromstring(
        """<ConversionRate reportDate="2011-12-30" fromCurrency="HKD" toCurrency="USD" rate="0.12876" />"""
    )

    def testConvert(self):
        output = self.schema.convert(self.data)
        self.assertIsInstance(output, dict)
        self.assertEqual(len(output), 4)

        self.assertEqual(output['reportDate'], datetime.date(2011, 12, 30))
        self.assertEqual(output['fromCurrency'], "HKD")
        self.assertEqual(output['toCurrency'], "USD")
        self.assertEqual(output['rate'], decimal.Decimal("0.12876"))


if __name__ == '__main__':
    unittest.main(verbosity=3)
