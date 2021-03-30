# coding: utf-8
""" Unit tests for ibflex.Types module """

# stdlib imports
import unittest
import xml.etree.ElementTree as ET
import datetime
import decimal


# local imports
from ibflex import Types, enums, parser


class AccountInformationTestCase(unittest.TestCase):
    data = ET.fromstring(
        ('<AccountInformation accountId="U123456" acctAlias="ibflex test" '
         'currency="USD" name="Porky Pig" accountType="Advisor Client" '
         'customerType="Partnership" '
         'accountCapabilities="Portfolio Margin,IBPrime" '
         'tradingPermissions="Stocks,Options,Warrants,Bonds,Forex,Stock Borrow" '
         'dateOpened="2009-06-25" dateFunded="2009-07-13" dateClosed="" '
         'masterName="Dewey Cheatham &amp; Howe" ibEntity="IBLLC-US" />')
    )

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.AccountInformation)
        self.assertEqual(instance.accountId, "U123456")
        self.assertEqual(instance.acctAlias, "ibflex test")
        self.assertEqual(instance.currency, "USD")
        self.assertEqual(instance.name, "Porky Pig")
        self.assertEqual(instance.accountType, "Advisor Client")
        self.assertEqual(instance.customerType, "Partnership")
        self.assertEqual(
            instance.accountCapabilities,
            ("Portfolio Margin", "IBPrime")
        )
        self.assertEqual(
            instance.tradingPermissions,
            ("Stocks", "Options", "Warrants", "Bonds", "Forex", "Stock Borrow")
        )
        self.assertEqual(instance.dateOpened, datetime.date(2009, 6, 25))
        self.assertEqual(instance.dateFunded, datetime.date(2009, 7, 13))
        self.assertEqual(instance.dateClosed, None)
        self.assertEqual(instance.masterName, "Dewey Cheatham & Howe")
        self.assertEqual(instance.ibEntity, "IBLLC-US")


class FlexStatementTestCase(unittest.TestCase):
    data = ET.fromstring(
        ('<FlexStatement accountId="U123456" fromDate="2011-01-03" toDate="2011-12-30" '
         'period="" whenGenerated="2017-05-10;164137" />')
    )
    data.append(AccountInformationTestCase.data)

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.FlexStatement)
        self.assertEqual(instance.accountId , 'U123456')
        self.assertEqual(instance.fromDate, datetime.date(2011, 1, 3))
        self.assertEqual(instance.toDate, datetime.date(2011, 12, 30))
        self.assertIs(instance.period, None)
        self.assertEqual(instance.whenGenerated, datetime.datetime(2017, 5, 10, 16, 41, 37))
        self.assertIsInstance(instance.AccountInformation, Types.AccountInformation)


class FlexQueryResponseTestCase(unittest.TestCase):
    data = ET.fromstring(
        """<FlexQueryResponse queryName="ibflex test" type="AF" />"""
    )
    data.append(ET.fromstring("""<FlexStatements count="1" />"""))

    def testParse(self):
        self.data[0].append(FlexStatementTestCase.data)
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.FlexQueryResponse)
        self.assertEqual(instance.queryName, 'ibflex test')
        self.assertEqual(instance.type, 'AF')

        self.assertIsInstance(instance.FlexStatements, tuple)
        self.assertEqual(len(instance.FlexStatements), 1)
        self.assertIsInstance(instance.FlexStatements[0], Types.FlexStatement)

    def testParseWrongStatementCount(self):
        """Error if <FlexStatements> `count` attr doesn't match # FlexStatement
        """
        # `count` == 1; no FlexStatement
        with self.assertRaises(parser.FlexParserError):
            parser.parse_data_element(self.data)

        # `count` == 1; 2 FlexStatements
        self.data[0].append(FlexStatementTestCase.data)
        self.data[0].append(FlexStatementTestCase.data)
        with self.assertRaises(parser.FlexParserError):
            parser.parse_data_element(self.data)

    def testParseNoStatements(self):
        # Error if FlexStatements `count` attribute doesn't match # FlexStatement
        self.data[0].append(FlexStatementTestCase.data)
        self.data[0].append(FlexStatementTestCase.data)
        with self.assertRaises(parser.FlexParserError):
            parser.parse_data_element(self.data)


class EquitySummaryByReportDateInBaseTestCase(unittest.TestCase):
    data = ET.fromstring(
        ('<EquitySummaryByReportDateInBase accountId="U123456" acctAlias="ibflex test" '
         'model="" reportDate="2011-12-30" cash="51.730909701" cashLong="51.730909701" '
         'cashShort="0" slbCashCollateral="0" slbCashCollateralLong="0" '
         'slbCashCollateralShort="0" stock="39.68" stockLong="44.68" stockShort="-46" '
         'slbDirectSecuritiesBorrowed="0" slbDirectSecuritiesBorrowedLong="0" '
         'slbDirectSecuritiesBorrowedShort="0" slbDirectSecuritiesLent="0" '
         'slbDirectSecuritiesLentLong="0" slbDirectSecuritiesLentShort="0" options="0" '
         'optionsLong="0" optionsShort="0" commodities="0" commoditiesLong="0" '
         'commoditiesShort="0" bonds="0" bondsLong="0" bondsShort="0" notes="0" '
         'notesLong="0" notesShort="0" funds="0" fundsLong="0" fundsShort="0" '
         'interestAccruals="-1111.05" interestAccrualsLong="0" '
         'interestAccrualsShort="-1111.05" softDollars="0" softDollarsLong="0" '
         'softDollarsShort="0" forexCfdUnrealizedPl="0" forexCfdUnrealizedPlLong="0" '
         'forexCfdUnrealizedPlShort="0" dividendAccruals="3299.79" '
         'dividendAccrualsLong="3299.79" dividendAccrualsShort="0" '
         'fdicInsuredBankSweepAccount="0" fdicInsuredBankSweepAccountLong="0" '
         'fdicInsuredBankSweepAccountShort="0" fdicInsuredAccountInterestAccruals="0" '
         'fdicInsuredAccountInterestAccrualsLong="0" '
         'fdicInsuredAccountInterestAccrualsShort="0" '
         'total="40.1509097" totalLong="44.2009097" totalShort="-46.05" />')
    )

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.EquitySummaryByReportDateInBase)

        self.assertEqual(instance.accountId, 'U123456')
        self.assertEqual(instance.acctAlias, "ibflex test")
        self.assertEqual(instance.model, None)
        self.assertEqual(instance.reportDate, datetime.date(2011, 12, 30))
        self.assertEqual(instance.cash, decimal.Decimal("51.730909701"))
        self.assertEqual(instance.cashLong, decimal.Decimal("51.730909701"))
        self.assertEqual(instance.cashShort, decimal.Decimal("0"))
        self.assertEqual(instance.slbCashCollateral, decimal.Decimal("0"))
        self.assertEqual(instance.slbCashCollateralLong, decimal.Decimal("0"))
        self.assertEqual(instance.slbCashCollateralShort, decimal.Decimal("0"))
        self.assertEqual(instance.stock, decimal.Decimal("39.68"))
        self.assertEqual(instance.stockLong, decimal.Decimal("44.68"))
        self.assertEqual(instance.stockShort, decimal.Decimal("-46"))
        self.assertEqual(instance.slbDirectSecuritiesBorrowed, decimal.Decimal("0"))
        self.assertEqual(instance.slbDirectSecuritiesBorrowedLong, decimal.Decimal("0"))
        self.assertEqual(instance.slbDirectSecuritiesBorrowedShort, decimal.Decimal("0"))
        self.assertEqual(instance.slbDirectSecuritiesLent, decimal.Decimal("0"))
        self.assertEqual(instance.slbDirectSecuritiesLentLong, decimal.Decimal("0"))
        self.assertEqual(instance.slbDirectSecuritiesLentShort, decimal.Decimal("0"))
        self.assertEqual(instance.options, decimal.Decimal("0"))
        self.assertEqual(instance.optionsLong, decimal.Decimal("0"))
        self.assertEqual(instance.optionsShort, decimal.Decimal("0"))
        self.assertEqual(instance.commodities, decimal.Decimal("0"))
        self.assertEqual(instance.commoditiesLong, decimal.Decimal("0"))
        self.assertEqual(instance.commoditiesShort, decimal.Decimal("0"))
        self.assertEqual(instance.bonds, decimal.Decimal("0"))
        self.assertEqual(instance.bondsLong, decimal.Decimal("0"))
        self.assertEqual(instance.bondsShort, decimal.Decimal("0"))
        self.assertEqual(instance.notes, decimal.Decimal("0"))
        self.assertEqual(instance.notesLong, decimal.Decimal("0"))
        self.assertEqual(instance.notesShort, decimal.Decimal("0"))
        self.assertEqual(instance.funds, decimal.Decimal("0"))
        self.assertEqual(instance.fundsLong, decimal.Decimal("0"))
        self.assertEqual(instance.fundsShort, decimal.Decimal("0"))
        self.assertEqual(instance.interestAccruals, decimal.Decimal("-1111.05"))
        self.assertEqual(instance.interestAccrualsLong, decimal.Decimal("0"))
        self.assertEqual(instance.interestAccrualsShort, decimal.Decimal("-1111.05"))
        self.assertEqual(instance.softDollars, decimal.Decimal("0"))
        self.assertEqual(instance.softDollarsLong, decimal.Decimal("0"))
        self.assertEqual(instance.softDollarsShort, decimal.Decimal("0"))
        self.assertEqual(instance.forexCfdUnrealizedPl, decimal.Decimal("0"))
        self.assertEqual(instance.forexCfdUnrealizedPlLong, decimal.Decimal("0"))
        self.assertEqual(instance.forexCfdUnrealizedPlShort, decimal.Decimal("0"))
        self.assertEqual(instance.dividendAccruals, decimal.Decimal("3299.79"))
        self.assertEqual(instance.dividendAccrualsLong, decimal.Decimal("3299.79"))
        self.assertEqual(instance.dividendAccrualsShort, decimal.Decimal("0"))
        self.assertEqual(instance.fdicInsuredBankSweepAccount, decimal.Decimal("0"))
        self.assertEqual(instance.fdicInsuredBankSweepAccountLong, decimal.Decimal("0"))
        self.assertEqual(instance.fdicInsuredBankSweepAccountShort, decimal.Decimal("0"))
        self.assertEqual(instance.fdicInsuredBankSweepAccountCashComponent, None)
        self.assertEqual(instance.fdicInsuredBankSweepAccountCashComponentLong, None)
        self.assertEqual(instance.fdicInsuredBankSweepAccountCashComponentShort, None)
        self.assertEqual(instance.fdicInsuredAccountInterestAccruals, decimal.Decimal("0"))
        self.assertEqual(instance.fdicInsuredAccountInterestAccrualsLong, decimal.Decimal("0"))
        self.assertEqual(instance.fdicInsuredAccountInterestAccrualsShort, decimal.Decimal("0"))
        self.assertEqual(instance.fdicInsuredAccountInterestAccrualsComponent, None)
        self.assertEqual(instance.fdicInsuredAccountInterestAccrualsComponentLong, None)
        self.assertEqual(instance.fdicInsuredAccountInterestAccrualsComponentShort, None)
        self.assertEqual(instance.total, decimal.Decimal("40.1509097"))
        self.assertEqual(instance.totalLong, decimal.Decimal("44.2009097"))
        self.assertEqual(instance.totalShort, decimal.Decimal("-46.05"))
        self.assertEqual(instance.brokerInterestAccrualsComponent, None)
        self.assertEqual(instance.brokerCashComponent, None)
        self.assertEqual(instance.cfdUnrealizedPl, None)


class CashReportCurrencyTestCase(unittest.TestCase):
    data = ET.fromstring(
        ('<CashReportCurrency accountId="U123456" acctAlias="ibflex test" model="" '
         'currency="USD" fromDate="2011-01-03" toDate="2011-12-30" '
         'startingCash="30.702569078" startingCashSec="30.702569078" '
         'startingCashCom="0" clientFees="0" clientFeesSec="0" clientFeesCom="0" '
         'commissions="-45.445684" commissionsSec="-45.445684" commissionsCom="0" '
         'billableCommissions="0" billableCommissionsSec="0" '
         'billableCommissionsCom="0" depositWithdrawals="10.62" '
         'depositWithdrawalsSec="10.62" depositWithdrawalsCom="0" deposits="13.62" '
         'depositsSec="13.62" depositsCom="0" withdrawals="-24" withdrawalsSec="-24" '
         'withdrawalsCom="0" accountTransfers="0" accountTransfersSec="0" '
         'accountTransfersCom="0" linkingAdjustments="0" linkingAdjustmentsSec="0" '
         'linkingAdjustmentsCom="0" internalTransfers="0" internalTransfersSec="0" '
         'internalTransfersCom="0" excessFundSweep="0" excessFundSweepSec="0" '
         'excessFundSweepCom="0" excessFundSweepMTD="0" excessFundSweepYTD="0" '
         'dividends="34.74" dividendsSec="34.74" dividendsCom="0" insuredDepositInterest="0" '
         'insuredDepositInterestSec="0" insuredDepositInterestCom="0" brokerInterest="-64.57" '
         'brokerInterestSec="-64.57" brokerInterestCom="0" bondInterest="0" '
         'bondInterestSec="0" bondInterestCom="0" cashSettlingMtm="0" '
         'cashSettlingMtmSec="0" cashSettlingMtmCom="0" realizedVm="0" '
         'realizedVmSec="0" realizedVmCom="0" cfdCharges="0" cfdChargesSec="0" '
         'cfdChargesCom="0" netTradesSales="19.608813" netTradesSalesSec="19.608813" '
         'netTradesSalesCom="0" netTradesPurchases="-33.164799999" '
         'netTradesPurchasesSec="-33.164799999" netTradesPurchasesCom="0" '
         'advisorFees="0" advisorFeesSec="0" advisorFeesCom="0" feesReceivables="0" '
         'feesReceivablesSec="0" feesReceivablesCom="0" paymentInLieu="-44.47" '
         'paymentInLieuSec="-44.47" paymentInLieuCom="0" transactionTax="0" '
         'transactionTaxSec="0" transactionTaxCom="0" taxReceivables="0" '
         'taxReceivablesSec="0" taxReceivablesCom="0" withholdingTax="-27.07" '
         'withholdingTaxSec="-27.07" withholdingTaxCom="0" withholding871m="0" '
         'withholding871mSec="0" withholding871mCom="0" withholdingCollectedTax="0" '
         'withholdingCollectedTaxSec="0" withholdingCollectedTaxCom="0" salesTax="0" '
         'salesTaxSec="0" salesTaxCom="0" billableSalesTax="0" billableSalesTaxSec="0" '
         'billableSalesTaxCom="0" billableSalesTaxMTD="0" billableSalesTaxYTD="0" fxTranslationGainLoss="0" '
         'fxTranslationGainLossSec="0" fxTranslationGainLossCom="0" '
         'otherFees="-521.22" otherFeesSec="-521.22" otherFeesCom="0" other="0" '
         'otherSec="0" otherCom="0" endingCash="51.730897778" '
         'endingCashSec="51.730897778" endingCashCom="0" '
         'endingSettledCash="51.730897778" endingSettledCashSec="51.730897778" '
         'endingSettledCashCom="0" />')
    )

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.CashReportCurrency)
        self.assertEqual(instance.accountId, "U123456")
        self.assertEqual(instance.acctAlias, "ibflex test")
        self.assertEqual(instance.model, None)
        self.assertEqual(instance.currency, "USD")
        self.assertEqual(instance.fromDate, datetime.date(2011, 1, 3))
        self.assertEqual(instance.toDate, datetime.date(2011, 12, 30))
        self.assertEqual(instance.startingCash, decimal.Decimal("30.702569078"))
        self.assertEqual(instance.startingCashSec, decimal.Decimal("30.702569078"))
        self.assertEqual(instance.startingCashCom, decimal.Decimal("0"))
        self.assertEqual(instance.clientFees, decimal.Decimal("0"))
        self.assertEqual(instance.clientFeesSec, decimal.Decimal("0"))
        self.assertEqual(instance.clientFeesCom, decimal.Decimal("0"))
        self.assertEqual(instance.commissions, decimal.Decimal("-45.445684"))
        self.assertEqual(instance.commissionsSec, decimal.Decimal("-45.445684"))
        self.assertEqual(instance.commissionsCom, decimal.Decimal("0"))
        self.assertEqual(instance.billableCommissions, decimal.Decimal("0"))
        self.assertEqual(instance.billableCommissionsSec, decimal.Decimal("0"))
        self.assertEqual(instance.billableCommissionsCom, decimal.Decimal("0"))
        self.assertEqual(instance.depositWithdrawals, decimal.Decimal("10.62"))
        self.assertEqual(instance.depositWithdrawalsSec, decimal.Decimal("10.62"))
        self.assertEqual(instance.depositWithdrawalsCom, decimal.Decimal("0"))
        self.assertEqual(instance.deposits, decimal.Decimal("13.62"))
        self.assertEqual(instance.depositsSec, decimal.Decimal("13.62"))
        self.assertEqual(instance.depositsCom, decimal.Decimal("0"))
        self.assertEqual(instance.withdrawals, decimal.Decimal("-24"))
        self.assertEqual(instance.withdrawalsSec, decimal.Decimal("-24"))
        self.assertEqual(instance.withdrawalsCom, decimal.Decimal("0"))
        self.assertEqual(instance.accountTransfers, decimal.Decimal("0"))
        self.assertEqual(instance.accountTransfersSec, decimal.Decimal("0"))
        self.assertEqual(instance.accountTransfersCom, decimal.Decimal("0"))
        self.assertEqual(instance.linkingAdjustments, decimal.Decimal("0"))
        self.assertEqual(instance.linkingAdjustmentsSec, decimal.Decimal("0"))
        self.assertEqual(instance.linkingAdjustmentsCom, decimal.Decimal("0"))
        self.assertEqual(instance.internalTransfers, decimal.Decimal("0"))
        self.assertEqual(instance.internalTransfersSec, decimal.Decimal("0"))
        self.assertEqual(instance.internalTransfersCom, decimal.Decimal("0"))
        self.assertEqual(instance.dividends, decimal.Decimal("34.74"))
        self.assertEqual(instance.dividendsSec, decimal.Decimal("34.74"))
        self.assertEqual(instance.dividendsCom, decimal.Decimal("0"))
        self.assertEqual(instance.insuredDepositInterest, decimal.Decimal("0"))
        self.assertEqual(instance.insuredDepositInterestSec, decimal.Decimal("0"))
        self.assertEqual(instance.insuredDepositInterestCom, decimal.Decimal("0"))
        self.assertEqual(instance.brokerInterest, decimal.Decimal("-64.57"))
        self.assertEqual(instance.brokerInterestSec, decimal.Decimal("-64.57"))
        self.assertEqual(instance.brokerInterestCom, decimal.Decimal("0"))
        self.assertEqual(instance.bondInterest, decimal.Decimal("0"))
        self.assertEqual(instance.bondInterestSec, decimal.Decimal("0"))
        self.assertEqual(instance.bondInterestCom, decimal.Decimal("0"))
        self.assertEqual(instance.cashSettlingMtm, decimal.Decimal("0"))
        self.assertEqual(instance.cashSettlingMtmSec, decimal.Decimal("0"))
        self.assertEqual(instance.cashSettlingMtmCom, decimal.Decimal("0"))
        self.assertEqual(instance.realizedVm, decimal.Decimal("0"))
        self.assertEqual(instance.realizedVmSec, decimal.Decimal("0"))
        self.assertEqual(instance.realizedVmCom, decimal.Decimal("0"))
        self.assertEqual(instance.cfdCharges, decimal.Decimal("0"))
        self.assertEqual(instance.cfdChargesSec, decimal.Decimal("0"))
        self.assertEqual(instance.cfdChargesCom, decimal.Decimal("0"))
        self.assertEqual(instance.netTradesSales, decimal.Decimal("19.608813"))
        self.assertEqual(instance.netTradesSalesSec, decimal.Decimal("19.608813"))
        self.assertEqual(instance.netTradesSalesCom, decimal.Decimal("0"))
        self.assertEqual(instance.netTradesPurchases, decimal.Decimal("-33.164799999"))
        self.assertEqual(instance.netTradesPurchasesSec, decimal.Decimal("-33.164799999"))
        self.assertEqual(instance.netTradesPurchasesCom, decimal.Decimal("0"))
        self.assertEqual(instance.advisorFees, decimal.Decimal("0"))
        self.assertEqual(instance.advisorFeesSec, decimal.Decimal("0"))
        self.assertEqual(instance.advisorFeesCom, decimal.Decimal("0"))
        self.assertEqual(instance.feesReceivables, decimal.Decimal("0"))
        self.assertEqual(instance.feesReceivablesSec, decimal.Decimal("0"))
        self.assertEqual(instance.feesReceivablesCom, decimal.Decimal("0"))
        self.assertEqual(instance.paymentInLieu, decimal.Decimal("-44.47"))
        self.assertEqual(instance.paymentInLieuSec, decimal.Decimal("-44.47"))
        self.assertEqual(instance.paymentInLieuCom, decimal.Decimal("0"))
        self.assertEqual(instance.transactionTax, decimal.Decimal("0"))
        self.assertEqual(instance.transactionTaxSec, decimal.Decimal("0"))
        self.assertEqual(instance.transactionTaxCom, decimal.Decimal("0"))
        self.assertEqual(instance.taxReceivables, decimal.Decimal("0"))
        self.assertEqual(instance.taxReceivablesSec, decimal.Decimal("0"))
        self.assertEqual(instance.taxReceivablesCom, decimal.Decimal("0"))
        self.assertEqual(instance.withholdingTax, decimal.Decimal("-27.07"))
        self.assertEqual(instance.withholdingTaxSec, decimal.Decimal("-27.07"))
        self.assertEqual(instance.withholdingTaxCom, decimal.Decimal("0"))
        self.assertEqual(instance.withholding871m, decimal.Decimal("0"))
        self.assertEqual(instance.withholding871mSec, decimal.Decimal("0"))
        self.assertEqual(instance.withholding871mCom, decimal.Decimal("0"))
        self.assertEqual(instance.withholdingCollectedTax, decimal.Decimal("0"))
        self.assertEqual(instance.withholdingCollectedTaxSec, decimal.Decimal("0"))
        self.assertEqual(instance.withholdingCollectedTaxCom, decimal.Decimal("0"))
        self.assertEqual(instance.salesTax, decimal.Decimal("0"))
        self.assertEqual(instance.salesTaxSec, decimal.Decimal("0"))
        self.assertEqual(instance.salesTaxCom, decimal.Decimal("0"))
        self.assertEqual(instance.fxTranslationGainLoss, decimal.Decimal("0"))
        self.assertEqual(instance.fxTranslationGainLossSec, decimal.Decimal("0"))
        self.assertEqual(instance.fxTranslationGainLossCom, decimal.Decimal("0"))
        self.assertEqual(instance.otherFees, decimal.Decimal("-521.22"))
        self.assertEqual(instance.otherFeesSec, decimal.Decimal("-521.22"))
        self.assertEqual(instance.otherFeesCom, decimal.Decimal("0"))
        self.assertEqual(instance.other, decimal.Decimal("0"))
        self.assertEqual(instance.otherSec, decimal.Decimal("0"))
        self.assertEqual(instance.otherCom, decimal.Decimal("0"))
        self.assertEqual(instance.endingCash, decimal.Decimal("51.730897778"))
        self.assertEqual(instance.endingCashSec, decimal.Decimal("51.730897778"))
        self.assertEqual(instance.endingCashCom, decimal.Decimal("0"))
        self.assertEqual(instance.endingSettledCash, decimal.Decimal("51.730897778"))
        self.assertEqual(instance.endingSettledCashSec, decimal.Decimal("51.730897778"))
        self.assertEqual(instance.endingSettledCashCom, decimal.Decimal("0"))


class StatementOfFundsLineTestCase(unittest.TestCase):
    data = ET.fromstring(
        ('<StatementOfFundsLine accountId="U123456" acctAlias="ibflex test" model="" '
         'currency="USD" assetCategory="STK" symbol="ECRO" '
         'description="ECC CAPITAL CORP" conid="33205002" securityID="" '
         'securityIDType="" cusip="" isin="" underlyingConid="" underlyingSymbol="" '
         'issuer="" multiplier="1" strike="" expiry="" putCall="" '
         'principalAdjustFactor="" reportDate="2011-12-27" date="2011-12-27" '
         'activityDescription="Buy 38,900 ECC CAPITAL CORP " tradeID="657898717" '
         'debit="-3185.60925" credit="" amount="-3185.60925" balance="53409.186538632" '
         'buySell="BUY" />')
    )

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.StatementOfFundsLine)
        self.assertEqual(instance.accountId, "U123456")
        self.assertEqual(instance.acctAlias, "ibflex test")
        self.assertEqual(instance.model, None)
        self.assertEqual(instance.currency, "USD")
        self.assertEqual(instance.assetCategory, enums.AssetClass.STOCK)
        self.assertEqual(instance.symbol, "ECRO")
        self.assertEqual(instance.description, "ECC CAPITAL CORP")
        self.assertEqual(instance.conid, "33205002")
        self.assertEqual(instance.securityID, None)
        self.assertEqual(instance.securityIDType, None)
        self.assertEqual(instance.cusip, None)
        self.assertEqual(instance.isin, None)
        self.assertEqual(instance.underlyingConid, None)
        self.assertEqual(instance.underlyingSymbol, None)
        self.assertEqual(instance.issuer, None)
        self.assertEqual(instance.multiplier, 1)
        self.assertEqual(instance.strike, None)
        self.assertEqual(instance.expiry, None)
        self.assertEqual(instance.putCall, None)
        self.assertEqual(instance.principalAdjustFactor, None)
        self.assertEqual(instance.reportDate, datetime.date(2011, 12, 27))
        self.assertEqual(instance.date, datetime.datetime(2011, 12, 27))
        self.assertEqual(instance.activityDescription, "Buy 38,900 ECC CAPITAL CORP ")
        self.assertEqual(instance.tradeID, "657898717")
        self.assertEqual(instance.debit, decimal.Decimal("-3185.60925"))
        self.assertEqual(instance.credit, None)
        self.assertEqual(instance.amount, decimal.Decimal("-3185.60925"))
        self.assertEqual(instance.balance, decimal.Decimal("53409.186538632"))
        self.assertEqual(instance.buySell, "BUY")


class ChangeInPositionValueTestCase(unittest.TestCase):
    data = ET.fromstring(
        ('<ChangeInPositionValue accountId="U123456" acctAlias="ibflex test" model="" '
         'currency="USD" assetCategory="STK" priorPeriodValue="18.57" '
         'transactions="14.931399999" mtmPriorPeriodPositions="-16.1077" '
         'mtmTransactions="-22.2354" corporateActions="-11.425" other="0" '
         'accountTransfers="94.18" linkingAdjustments="0" fxTranslationPnl="0" '
         'futurePriceAdjustments="0" settledCash="0" endOfPeriodValue="39.68" />')
    )

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.ChangeInPositionValue)
        self.assertEqual(instance.accountId, "U123456")
        self.assertEqual(instance.acctAlias, "ibflex test")
        self.assertEqual(instance.model, None)
        self.assertEqual(instance.currency, "USD")
        self.assertEqual(instance.assetCategory, enums.AssetClass.STOCK)
        self.assertEqual(instance.priorPeriodValue, decimal.Decimal("18.57"))
        self.assertEqual(instance.transactions, decimal.Decimal("14.931399999"))
        self.assertEqual(instance.mtmPriorPeriodPositions, decimal.Decimal("-16.1077"))
        self.assertEqual(instance.mtmTransactions, decimal.Decimal("-22.2354"))
        self.assertEqual(instance.corporateActions, decimal.Decimal("-11.425"))
        self.assertEqual(instance.other, decimal.Decimal("0"))
        self.assertEqual(instance.accountTransfers, decimal.Decimal("94.18"))
        self.assertEqual(instance.linkingAdjustments, decimal.Decimal("0"))
        self.assertEqual(instance.fxTranslationPnl, decimal.Decimal("0"))
        self.assertEqual(instance.futurePriceAdjustments, decimal.Decimal("0"))
        self.assertEqual(instance.settledCash, decimal.Decimal("0"))
        self.assertEqual(instance.endOfPeriodValue, decimal.Decimal("39.68"))


class OpenPositionTestCase(unittest.TestCase):
    data = ET.fromstring(
        ('<OpenPosition accountId="U123456" acctAlias="ibflex test" model="" '
         'currency="USD" fxRateToBase="1" assetCategory="STK" symbol="VXX" '
         'description="IPATH S&amp;P 500 VIX S/T FU ETN" conid="80789235" securityID="" '
         'securityIDType="" cusip="" isin="" underlyingConid="" underlyingSymbol="" '
         'issuer="" multiplier="1" strike="" expiry="" putCall="" '
         'principalAdjustFactor="" reportDate="2011-12-30" position="-100" '
         'markPrice="35.53" positionValue="-3553" openPrice="34.405" '
         'costBasisPrice="34.405" costBasisMoney="-3440.5" percentOfNAV="" '
         'fifoPnlUnrealized="-112.5" side="Short" levelOfDetail="LOT" '
         'openDateTime="2011-08-08;134413" holdingPeriodDateTime="2011-08-08;134413" '
         'code="" originatingOrderID="308163094" originatingTransactionID="2368917073" '
         'accruedInt="" />')
    )

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.OpenPosition)
        self.assertEqual(instance.accountId, "U123456")
        self.assertEqual(instance.acctAlias, "ibflex test")
        self.assertEqual(instance.model, None)
        self.assertEqual(instance.currency, "USD")
        self.assertEqual(instance.fxRateToBase, 1)
        self.assertEqual(instance.assetCategory, enums.AssetClass.STOCK)
        self.assertEqual(instance.symbol, "VXX")
        self.assertEqual(instance.description, "IPATH S&P 500 VIX S/T FU ETN")
        self.assertEqual(instance.conid, "80789235")
        self.assertEqual(instance.securityID, None)
        self.assertEqual(instance.securityIDType, None)
        self.assertEqual(instance.cusip, None)
        self.assertEqual(instance.isin, None)
        self.assertEqual(instance.underlyingConid, None)
        self.assertEqual(instance.underlyingSymbol, None)
        self.assertEqual(instance.issuer, None)
        self.assertEqual(instance.multiplier, 1)
        self.assertEqual(instance.strike, None)
        self.assertEqual(instance.expiry, None)
        self.assertEqual(instance.putCall, None)
        self.assertEqual(instance.principalAdjustFactor, None)
        self.assertEqual(instance.reportDate, datetime.date(2011, 12, 30))
        self.assertEqual(instance.position, decimal.Decimal("-100"))
        self.assertEqual(instance.markPrice, decimal.Decimal("35.53"))
        self.assertEqual(instance.positionValue, decimal.Decimal("-3553"))
        self.assertEqual(instance.openPrice, decimal.Decimal("34.405"))
        self.assertEqual(instance.costBasisPrice, decimal.Decimal("34.405"))
        self.assertEqual(instance.costBasisMoney, decimal.Decimal("-3440.5"))
        self.assertEqual(instance.percentOfNAV, None)
        self.assertEqual(instance.fifoPnlUnrealized, decimal.Decimal("-112.5"))
        self.assertEqual(instance.side, enums.LongShort.SHORT)
        self.assertEqual(instance.levelOfDetail, "LOT")
        self.assertEqual(instance.openDateTime, datetime.datetime(2011, 8, 8, 13, 44, 13))
        self.assertEqual(instance.holdingPeriodDateTime,  datetime.datetime(2011, 8, 8, 13, 44, 13))
        self.assertEqual(instance.code, ())
        self.assertEqual(instance.originatingOrderID, "308163094")
        self.assertEqual(instance.originatingTransactionID, "2368917073")
        self.assertEqual(instance.accruedInt, None)


class FxLotTestCase(unittest.TestCase):
    data = ET.fromstring(
        ('<FxLot accountId="U123456" acctAlias="ibflex test" model="" '
         'assetCategory="CASH" reportDate="2013-12-31" functionalCurrency="USD" '
         'fxCurrency="CAD" quantity="0.000012" costPrice="1" costBasis="-0.000012" '
         'closePrice="0.94148" value="0.000011" unrealizedPL="-0.000001" code="" '
         'lotDescription="CASH: -0.0786 USD.CAD" lotOpenDateTime="2011-01-25;180427" '
         'levelOfDetail="LOT" />')
    )

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.FxLot)
        self.assertEqual(instance.accountId, "U123456")
        self.assertEqual(instance.acctAlias, "ibflex test")
        self.assertEqual(instance.model, None)
        self.assertEqual(instance.assetCategory, enums.AssetClass.CASH)
        self.assertEqual(instance.reportDate, datetime.date(2013, 12, 31))
        self.assertEqual(instance.functionalCurrency, "USD")
        self.assertEqual(instance.fxCurrency, "CAD")
        self.assertEqual(instance.quantity, decimal.Decimal("0.000012"))
        self.assertEqual(instance.costPrice, decimal.Decimal("1"))
        self.assertEqual(instance.costBasis, decimal.Decimal("-0.000012"))
        self.assertEqual(instance.closePrice, decimal.Decimal("0.94148"))
        self.assertEqual(instance.value, decimal.Decimal("0.000011"))
        self.assertEqual(instance.unrealizedPL, decimal.Decimal("-0.000001"))
        self.assertEqual(instance.code, ())
        self.assertEqual(instance.lotDescription, "CASH: -0.0786 USD.CAD")
        self.assertEqual(instance.lotOpenDateTime, datetime.datetime(2011, 1, 25, 18, 4, 27))
        self.assertEqual(instance.levelOfDetail, "LOT")


class TradeTestCase(unittest.TestCase):
    data = ET.fromstring(
        ('<Trade accountId="U123456" acctAlias="ibflex test" model="" currency="USD" '
         'fxRateToBase="1" assetCategory="OPT" symbol="VXX   110917C00005000" '
         'description="VXX 17SEP11 5.0 C" conid="83615386" securityID="" '
         'securityIDType="" cusip="" isin="" underlyingConid="80789235" '
         'underlyingSymbol="VXX" issuer="" multiplier="100" strike="5" '
         'expiry="2011-09-17" putCall="C" principalAdjustFactor="" tradeID="594763148" '
         'reportDate="2011-08-12" tradeDate="2011-08-11" tradeTime="162000" '
         'settleDateTarget="2011-08-12" transactionType="BookTrade" exchange="--" '
         'quantity="3" tradePrice="0" tradeMoney="0" proceeds="-0" taxes="0" '
         'ibCommission="0" ibCommissionCurrency="USD" netCash="0" '
         'closePrice="29.130974" openCloseIndicator="C" notes="A" cost="8398.81122" '
         'fifoPnlRealized="0" fxPnl="0" mtmPnl="8739.2922" origTradePrice="0" '
         'origTradeDate="" origTradeID="" origOrderID="0" clearingFirmID="" '
         'transactionID="2381339439" buySell="BUY" ibOrderID="2381339439" ibExecID="" '
         'brokerageOrderID="" orderReference="" volatilityOrderLink="" '
         'exchOrderId="N/A" extExecID="N/A" orderTime="" openDateTime="" '
         'holdingPeriodDateTime="" whenRealized="" whenReopened="" '
         'levelOfDetail="EXECUTION" changeInPrice="0" changeInQuantity="0" '
         'orderType="" traderID="" isAPIOrder="N" accruedInt="0" serialNumber="" '
         'deliveryType="" commodityType="" fineness="0.0" weight="0.0 ()" />')
    )

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.Trade)
        self.assertEqual(instance.accountId, "U123456")
        self.assertEqual(instance.acctAlias, "ibflex test")
        self.assertEqual(instance.model, None)
        self.assertEqual(instance.currency, "USD")
        self.assertEqual(instance.fxRateToBase, decimal.Decimal('1'))
        self.assertEqual(instance.assetCategory, enums.AssetClass.OPTION)
        self.assertEqual(instance.symbol, "VXX   110917C00005000")
        self.assertEqual(instance.description, "VXX 17SEP11 5.0 C")
        self.assertEqual(instance.conid, "83615386")
        self.assertEqual(instance.securityID, None)
        self.assertEqual(instance.securityIDType, None)
        self.assertEqual(instance.cusip, None)
        self.assertEqual(instance.isin, None)
        self.assertEqual(instance.underlyingConid, "80789235")
        self.assertEqual(instance.underlyingSymbol, "VXX")
        self.assertEqual(instance.issuer, None)
        self.assertEqual(instance.multiplier, decimal.Decimal('100'))
        self.assertEqual(instance.strike, decimal.Decimal('5'))
        self.assertEqual(instance.expiry, datetime.date(2011, 9, 17))
        self.assertEqual(instance.putCall, enums.PutCall.CALL)
        self.assertEqual(instance.principalAdjustFactor, None)
        self.assertEqual(instance.tradeID, "594763148")
        self.assertEqual(instance.reportDate, datetime.date(2011, 8, 12))
        self.assertEqual(instance.tradeDate,  datetime.date(2011, 8, 11))
        self.assertEqual(instance.tradeTime, datetime.time(16, 20, 0))
        self.assertEqual(instance.settleDateTarget,  datetime.date(2011, 8, 12))
        self.assertEqual(instance.transactionType, enums.TradeType.BOOKTRADE)
        self.assertEqual(instance.exchange, None)
        self.assertEqual(instance.quantity, decimal.Decimal("3"))
        self.assertEqual(instance.tradePrice, decimal.Decimal("0"))
        self.assertEqual(instance.tradeMoney, decimal.Decimal("0"))
        self.assertEqual(instance.proceeds, decimal.Decimal("-0"))
        self.assertEqual(instance.taxes, decimal.Decimal("0"))
        self.assertEqual(instance.ibCommission, decimal.Decimal("0"))
        self.assertEqual(instance.ibCommissionCurrency, "USD")
        self.assertEqual(instance.netCash, decimal.Decimal("0"))
        self.assertEqual(instance.closePrice, decimal.Decimal("29.130974"))
        self.assertEqual(instance.openCloseIndicator, enums.OpenClose.CLOSE)
        self.assertEqual(instance.notes, (enums.Code.ASSIGNMENT, ))
        self.assertEqual(instance.cost, decimal.Decimal("8398.81122"))
        self.assertEqual(instance.fifoPnlRealized, decimal.Decimal("0"))
        self.assertEqual(instance.fxPnl, decimal.Decimal("0"))
        self.assertEqual(instance.mtmPnl, decimal.Decimal("8739.2922"))
        self.assertEqual(instance.origTradePrice, decimal.Decimal("0"))
        self.assertEqual(instance.origTradeDate, None)
        self.assertEqual(instance.origTradeID, None)
        self.assertEqual(instance.origOrderID, "0")
        self.assertEqual(instance.clearingFirmID, None)
        self.assertEqual(instance.transactionID, "2381339439")
        self.assertEqual(instance.buySell, enums.BuySell.BUY)
        self.assertEqual(instance.ibOrderID, "2381339439")
        self.assertEqual(instance.ibExecID, None)
        self.assertEqual(instance.brokerageOrderID, None)
        self.assertEqual(instance.orderReference, None)
        self.assertEqual(instance.volatilityOrderLink, None)
        self.assertEqual(instance.exchOrderId, None)
        self.assertEqual(instance.extExecID, None)
        self.assertEqual(instance.orderTime, None)
        self.assertEqual(instance.openDateTime, None)
        self.assertEqual(instance.holdingPeriodDateTime, None)
        self.assertEqual(instance.whenRealized, None)
        self.assertEqual(instance.whenReopened, None)
        self.assertEqual(instance.levelOfDetail, "EXECUTION")
        self.assertEqual(instance.changeInPrice, decimal.Decimal("0"))
        self.assertEqual(instance.changeInQuantity, decimal.Decimal("0"))
        self.assertEqual(instance.orderType, None)
        self.assertEqual(instance.traderID, None)
        self.assertEqual(instance.isAPIOrder, False)
        self.assertEqual(instance.accruedInt, decimal.Decimal("0"))
        self.assertEqual(instance.serialNumber, None)
        self.assertEqual(instance.deliveryType, None)
        self.assertEqual(instance.commodityType, None)
        self.assertEqual(instance.fineness, decimal.Decimal("0"))
        self.assertEqual(instance.weight, "0.0 ()")


class OptionEAETestCase(unittest.TestCase):
    data = ET.fromstring(
        ('<OptionEAE accountId="U123456" acctAlias="ibflex test" model="" '
         'currency="USD" fxRateToBase="1" assetCategory="OPT" '
         'symbol="VXX   110805C00020000" '
         'description="VXX 05AUG11 20.0 C" conid="91900358" securityID="" '
         'securityIDType="" cusip="" isin="" underlyingConid="80789235" '
         'underlyingSymbol="VXX" issuer="" multiplier="100" strike="20" '
         'expiry="2011-08-05" putCall="C" principalAdjustFactor="" date="2011-08-05" '
         'transactionType="Assignment" quantity="20" tradePrice="0.0000" '
         'markPrice="0.0000" proceeds="0.00" commisionsAndTax="0.00" '
         'costBasis="21,792.73" realizedPnl="0.00" fxPnl="0.00" mtmPnl="20,620.00" '
         'tradeID="" />')
    )

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.OptionEAE)
        self.assertEqual(instance.accountId, "U123456")
        self.assertEqual(instance.acctAlias, "ibflex test")
        self.assertEqual(instance.model, None)
        self.assertEqual(instance.currency, "USD")
        self.assertEqual(instance.fxRateToBase, decimal.Decimal("1"))
        self.assertEqual(instance.assetCategory, enums.AssetClass.OPTION)
        self.assertEqual(instance.symbol, "VXX   110805C00020000")
        self.assertEqual(instance.description, "VXX 05AUG11 20.0 C")
        self.assertEqual(instance.conid, "91900358")
        self.assertEqual(instance.securityID, None)
        self.assertEqual(instance.securityIDType, None)
        self.assertEqual(instance.cusip, None)
        self.assertEqual(instance.isin, None)
        self.assertEqual(instance.underlyingConid, "80789235")
        self.assertEqual(instance.underlyingSymbol, "VXX")
        self.assertEqual(instance.issuer, None)
        self.assertEqual(instance.multiplier, decimal.Decimal("100"))
        self.assertEqual(instance.strike, decimal.Decimal("20"))
        self.assertEqual(instance.expiry, datetime.date(2011, 8, 5))
        self.assertEqual(instance.putCall, enums.PutCall.CALL)
        self.assertEqual(instance.principalAdjustFactor, None)
        self.assertEqual(instance.date, datetime.date(2011, 8, 5))
        self.assertEqual(instance.transactionType, enums.OptionAction.ASSIGN)
        self.assertEqual(instance.quantity, decimal.Decimal("20"))
        self.assertEqual(instance.tradePrice, decimal.Decimal("0.0000"))
        self.assertEqual(instance.markPrice, decimal.Decimal("0.0000"))
        self.assertEqual(instance.proceeds, decimal.Decimal("0.00"))
        self.assertEqual(instance.commisionsAndTax, decimal.Decimal("0.00"))
        self.assertEqual(instance.costBasis, decimal.Decimal("21792.73"))
        self.assertEqual(instance.realizedPnl, decimal.Decimal("0.00"))
        self.assertEqual(instance.fxPnl, decimal.Decimal("0.00"))
        self.assertEqual(instance.mtmPnl, decimal.Decimal("20620.00"))
        self.assertEqual(instance.tradeID, None)


class TradeTransferTestCase(unittest.TestCase):
    data = ET.fromstring(
        ('<TradeTransfer accountId="U123456" acctAlias="ibflex test" model="" '
         'currency="USD" fxRateToBase="1" assetCategory="STK" symbol="ADGI" '
         'description="ALLIED DEFENSE GROUP INC/THE" conid="764451" securityID="" '
         'securityIDType="" cusip="" isin="" underlyingConid="" underlyingSymbol="" '
         'issuer="" multiplier="1" strike="" expiry="" putCall="" '
         'principalAdjustFactor="" tradeID="599063639" reportDate="2011-08-22" '
         'tradeDate="2011-08-19" tradeTime="202000" settleDateTarget="2011-08-24" '
         'transactionType="DvpTrade" exchange="--" quantity="10000" tradePrice="3.1" '
         'tradeMoney="31000" proceeds="-31010" taxes="0" ibCommission="-1" '
         'ibCommissionCurrency="USD" netCash="-31011" closePrice="3.02" '
         'openCloseIndicator="O" notes="" cost="31011" fifoPnlRealized="0" fxPnl="0" '
         'mtmPnl="-810" origTradePrice="0" origTradeDate="" origTradeID="" '
         'origOrderID="0" clearingFirmID="94378" transactionID="" '
         'brokerName="E*Trade Clearing LLC" brokerAccount="1234-5678" '
         'awayBrokerCommission="10" regulatoryFee="0" direction="From" '
         'deliveredReceived="Received" netTradeMoney="31010" '
         'netTradeMoneyInBase="31010" netTradePrice="3.101" openDateTime="" '
         'holdingPeriodDateTime="" whenRealized="" whenReopened="" '
         'levelOfDetail="TRADE_TRANSFERS" />')
    )

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.TradeTransfer)
        self.assertEqual(instance.accountId, "U123456")
        self.assertEqual(instance.acctAlias, "ibflex test")
        self.assertEqual(instance.model, None)
        self.assertEqual(instance.currency, "USD")
        self.assertEqual(instance.fxRateToBase, decimal.Decimal('1'))
        self.assertEqual(instance.assetCategory, enums.AssetClass.STOCK)
        self.assertEqual(instance.symbol, "ADGI")
        self.assertEqual(instance.description, "ALLIED DEFENSE GROUP INC/THE")
        self.assertEqual(instance.conid, "764451")
        self.assertEqual(instance.securityID, None)
        self.assertEqual(instance.securityIDType, None)
        self.assertEqual(instance.cusip, None)
        self.assertEqual(instance.isin, None)
        self.assertEqual(instance.underlyingConid, None)
        self.assertEqual(instance.underlyingSymbol, None)
        self.assertEqual(instance.issuer, None)
        self.assertEqual(instance.multiplier, decimal.Decimal('1'))
        self.assertEqual(instance.strike, None)
        self.assertEqual(instance.expiry, None)
        self.assertEqual(instance.putCall, None)
        self.assertEqual(instance.principalAdjustFactor, None)
        self.assertEqual(instance.tradeID, "599063639")
        self.assertEqual(instance.reportDate, datetime.date(2011, 8, 22))
        self.assertEqual(instance.tradeDate, datetime.date(2011, 8, 19))
        self.assertEqual(instance.tradeTime, datetime.time(20,20, 0))
        self.assertEqual(instance.settleDateTarget, datetime.date(2011, 8, 24))
        self.assertEqual(instance.transactionType, enums.TradeType.DVPTRADE)
        self.assertEqual(instance.exchange, None)
        self.assertEqual(instance.quantity, decimal.Decimal("10000"))
        self.assertEqual(instance.tradePrice, decimal.Decimal("3.1"))
        self.assertEqual(instance.tradeMoney, decimal.Decimal("31000"))
        self.assertEqual(instance.proceeds, decimal.Decimal("-31010"))
        self.assertEqual(instance.taxes, decimal.Decimal("0"))
        self.assertEqual(instance.ibCommission, decimal.Decimal("-1"))
        self.assertEqual(instance.ibCommissionCurrency, "USD")
        self.assertEqual(instance.netCash, decimal.Decimal("-31011"))
        self.assertEqual(instance.closePrice, decimal.Decimal("3.02"))
        self.assertEqual(instance.openCloseIndicator, enums.OpenClose.OPEN)
        self.assertEqual(instance.notes, ())
        self.assertEqual(instance.cost, decimal.Decimal("31011"))
        self.assertEqual(instance.fifoPnlRealized, decimal.Decimal("0"))
        self.assertEqual(instance.fxPnl, decimal.Decimal("0"))
        self.assertEqual(instance.mtmPnl, decimal.Decimal("-810"))
        self.assertEqual(instance.origTradePrice, decimal.Decimal("0"))
        self.assertEqual(instance.origTradeDate, None)
        self.assertEqual(instance.origTradeID, None)
        self.assertEqual(instance.origOrderID, "0")
        self.assertEqual(instance.clearingFirmID, "94378")
        self.assertEqual(instance.transactionID, None)
        self.assertEqual(instance.brokerName, "E*Trade Clearing LLC")
        self.assertEqual(instance.brokerAccount, "1234-5678")
        self.assertEqual(instance.awayBrokerCommission, decimal.Decimal("10"))
        self.assertEqual(instance.regulatoryFee, decimal.Decimal("0"))
        self.assertEqual(instance.direction, enums.ToFrom.FROM)
        self.assertEqual(instance.deliveredReceived, enums.DeliveredReceived.RECEIVED)
        self.assertEqual(instance.netTradeMoney, decimal.Decimal("31010"))
        self.assertEqual(instance.netTradeMoneyInBase, decimal.Decimal("31010"))
        self.assertEqual(instance.netTradePrice, decimal.Decimal("3.101"))
        self.assertEqual(instance.openDateTime, None)
        self.assertEqual(instance.holdingPeriodDateTime, None)
        self.assertEqual(instance.whenRealized, None)
        self.assertEqual(instance.whenReopened, None)
        self.assertEqual(instance.levelOfDetail, "TRADE_TRANSFERS")


class CashTransactionTestCase(unittest.TestCase):
    data = ET.fromstring(
        ('<CashTransaction accountId="U123456" acctAlias="ibflex test" model="" '
         'currency="USD" fxRateToBase="1" assetCategory="STK" symbol="RHDGF" '
         'description="RHDGF(ANN741081064) CASH DIVIDEND 1.00000000 USD PER SHARE (Return of Capital)" '
         'conid="62049667" securityID="ANN741081064" securityIDType="ISIN" cusip="" '
         'isin="ANN741081064" underlyingConid="" underlyingSymbol="" issuer="" '
         'multiplier="1" strike="" expiry="" putCall="" principalAdjustFactor="" '
         'dateTime="2015-10-06" amount="27800" type="Dividends" tradeID="" code="" '
         'transactionID="5767420360" reportDate="2015-10-06" clientReference="" />')
    )

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.CashTransaction)
        self.assertEqual(instance.accountId, "U123456")
        self.assertEqual(instance.acctAlias, "ibflex test")
        self.assertEqual(instance.model, None)
        self.assertEqual(instance.currency, "USD")
        self.assertEqual(instance.fxRateToBase, decimal.Decimal("1"))
        self.assertEqual(instance.assetCategory, enums.AssetClass.STOCK)
        self.assertEqual(instance.symbol, "RHDGF")
        self.assertEqual(instance.description, "RHDGF(ANN741081064) CASH DIVIDEND 1.00000000 USD PER SHARE (Return of Capital)")
        self.assertEqual(instance.conid, "62049667")
        self.assertEqual(instance.securityID, "ANN741081064")
        self.assertEqual(instance.securityIDType, "ISIN")
        self.assertEqual(instance.cusip, None)
        self.assertEqual(instance.isin, "ANN741081064")
        self.assertEqual(instance.underlyingConid, None)
        self.assertEqual(instance.underlyingSymbol, None)
        self.assertEqual(instance.issuer, None)
        self.assertEqual(instance.multiplier, decimal.Decimal("1"))
        self.assertEqual(instance.strike, None)
        self.assertEqual(instance.expiry, None)
        self.assertEqual(instance.putCall, None)
        self.assertEqual(instance.principalAdjustFactor, None)
        self.assertEqual(instance.dateTime, datetime.datetime(2015, 10, 6))
        self.assertEqual(instance.amount, decimal.Decimal("27800"))
        self.assertEqual(instance.type, enums.CashAction.DIVIDEND)
        self.assertEqual(instance.tradeID, None)
        self.assertEqual(instance.code, ())
        self.assertEqual(instance.transactionID, "5767420360")
        self.assertEqual(instance.reportDate, datetime.date(2015,10, 6))
        self.assertEqual(instance.clientReference, None)


class DebitCardActivityTestCase(unittest.TestCase):
    data = ET.fromstring(
        ('<DebitCardActivity accountId="U123456" acctAlias="ibflex test" model="" '
         'currency="BASE_SUMMARY" fxRateToBase="1" assetCategory="" status="Settled" '
         'reportDate="20201101" postingDate="20201102" transactionDateTime="20201110;172030" '
         'category="RETAIL" merchantNameLocation="DTN" '
         'amount="-117.00" />')
    )

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.DebitCardActivity)
        self.assertEqual(instance.accountId, "U123456")
        self.assertEqual(instance.acctAlias, "ibflex test")
        self.assertEqual(instance.model, None)
        self.assertEqual(instance.currency, "BASE_SUMMARY")
        self.assertEqual(instance.fxRateToBase, decimal.Decimal("1"))
        self.assertEqual(instance.assetCategory, None)
        self.assertEqual(instance.status, "Settled")
        self.assertEqual(instance.reportDate, datetime.date(2020, 11, 1))
        self.assertEqual(instance.postingDate, datetime.date(2020, 11, 2))
        self.assertEqual(instance.transactionDateTime, datetime.datetime(2020, 11, 10, 17, 20, 30))
        self.assertEqual(instance.category, "RETAIL")
        self.assertEqual(instance.merchantNameLocation, "DTN")
        self.assertEqual(instance.amount, decimal.Decimal("-117.00"))


class InterestAccrualsCurrencyTestCase(unittest.TestCase):
    data = ET.fromstring(
        ('<InterestAccrualsCurrency accountId="U123456" acctAlias="ibflex test" '
         'model="" currency="BASE_SUMMARY" fromDate="2011-01-03" toDate="2011-12-30" '
         'startingAccrualBalance="-11.558825" interestAccrued="-7516.101776" '
         'accrualReversal="6416.624437" fxTranslation="-0.013836" '
         'endingAccrualBalance="-1111.05" />')
    )

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.InterestAccrualsCurrency)
        self.assertEqual(instance.accountId, "U123456")
        self.assertEqual(instance.acctAlias, "ibflex test")
        self.assertEqual(instance.model, None)
        self.assertEqual(instance.currency, "BASE_SUMMARY")
        self.assertEqual(instance.fromDate, datetime.date(2011, 1, 3))
        self.assertEqual(instance.toDate, datetime.date(2011, 12, 30))
        self.assertEqual(instance.startingAccrualBalance, decimal.Decimal("-11.558825"))
        self.assertEqual(instance.interestAccrued, decimal.Decimal("-7516.101776"))
        self.assertEqual(instance.accrualReversal, decimal.Decimal("6416.624437"))
        self.assertEqual(instance.fxTranslation, decimal.Decimal("-0.013836"))
        self.assertEqual(instance.endingAccrualBalance, decimal.Decimal("-1111.05"))


class SLBActivityTestCase(unittest.TestCase):
    data = ET.fromstring(
        ('<SLBActivity accountId="U123456" acctAlias="ibflex test" model="" '
         'currency="USD" fxRateToBase="1" assetCategory="STK" symbol="CHTP.CVR" '
         'description="CHELSEA THERAPEUTICS INTERNA - ESCROW" conid="158060456" '
         'securityID="" securityIDType="" cusip="" isin="" underlyingConid="" '
         'underlyingSymbol="" issuer="" multiplier="1" strike="" expiry="" putCall="" '
         'principalAdjustFactor="" date="2015-06-01" slbTransactionId="SLB.32117554" '
         'activityDescription="New Loan Allocation" type="ManagedLoan" exchange="" '
         'quantity="-48330" feeRate="0.44" collateralAmount="48330" markQuantity="0" '
         'markPriorPrice="0" markCurrentPrice="0" />')
    )

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.SLBActivity)
        self.assertEqual(instance.accountId, "U123456")
        self.assertEqual(instance.acctAlias, "ibflex test")
        self.assertEqual(instance.model, None)
        self.assertEqual(instance.currency, "USD")
        self.assertEqual(instance.fxRateToBase, decimal.Decimal("1"))
        self.assertEqual(instance.assetCategory, enums.AssetClass.STOCK)
        self.assertEqual(instance.symbol, "CHTP.CVR")
        self.assertEqual(instance.description, "CHELSEA THERAPEUTICS INTERNA - ESCROW")
        self.assertEqual(instance.conid, "158060456")
        self.assertEqual(instance.securityID, None)
        self.assertEqual(instance.securityIDType, None)
        self.assertEqual(instance.cusip, None)
        self.assertEqual(instance.isin, None)
        self.assertEqual(instance.underlyingConid, None)
        self.assertEqual(instance.underlyingSymbol, None)
        self.assertEqual(instance.issuer, None)
        self.assertEqual(instance.multiplier, decimal.Decimal("1"))
        self.assertEqual(instance.strike, None)
        self.assertEqual(instance.expiry, None)
        self.assertEqual(instance.putCall, None)
        self.assertEqual(instance.principalAdjustFactor, None)
        self.assertEqual(instance.date, datetime.date(2015, 6, 1))
        self.assertEqual(instance.slbTransactionId, "SLB.32117554")
        self.assertEqual(instance.activityDescription, "New Loan Allocation")
        self.assertEqual(instance.type, "ManagedLoan")
        self.assertEqual(instance.exchange, None)
        self.assertEqual(instance.quantity, decimal.Decimal("-48330"))
        self.assertEqual(instance.feeRate, decimal.Decimal("0.44"))
        self.assertEqual(instance.collateralAmount, decimal.Decimal("48330"))
        self.assertEqual(instance.markQuantity, decimal.Decimal("0"))
        self.assertEqual(instance.markPriorPrice, decimal.Decimal("0"))
        self.assertEqual(instance.markCurrentPrice, decimal.Decimal("0"))


class TransferTestCase(unittest.TestCase):
    data = ET.fromstring(
        ('<Transfer accountId="U123456" acctAlias="ibflex test" model="" '
         'currency="USD" fxRateToBase="1" assetCategory="STK" symbol="FMTIF" '
         'description="FMI HOLDINGS LTD" conid="86544467" securityID="" '
         'securityIDType="" cusip="" isin="" underlyingConid="" underlyingSymbol="" '
         'issuer="" multiplier="1" strike="" expiry="" putCall="" '
         'principalAdjustFactor="" date="2011-07-18" type="ACATS" direction="IN" '
         'company="--" account="12345678" accountName="" quantity="226702" '
         'transferPrice="0" positionAmount="11.51" positionAmountInBase="11.51" '
         'pnlAmount="0" pnlAmountInBase="0" fxPnl="0" cashTransfer="0" code="" '
         'clientReference="" />')
    )

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.Transfer)
        self.assertEqual(instance.accountId, "U123456")
        self.assertEqual(instance.acctAlias, "ibflex test")
        self.assertEqual(instance.model, None)
        self.assertEqual(instance.currency, "USD")
        self.assertEqual(instance.fxRateToBase, decimal.Decimal("1"))
        self.assertEqual(instance.assetCategory, enums.AssetClass.STOCK)
        self.assertEqual(instance.symbol, "FMTIF")
        self.assertEqual(instance.description, "FMI HOLDINGS LTD")
        self.assertEqual(instance.conid, "86544467")
        self.assertEqual(instance.securityID, None)
        self.assertEqual(instance.securityIDType, None)
        self.assertEqual(instance.cusip, None)
        self.assertEqual(instance.isin, None)
        self.assertEqual(instance.underlyingConid, None)
        self.assertEqual(instance.underlyingSymbol, None)
        self.assertEqual(instance.issuer, None)
        self.assertEqual(instance.multiplier, decimal.Decimal("1"))
        self.assertEqual(instance.strike, None)
        self.assertEqual(instance.expiry, None)
        self.assertEqual(instance.putCall, None)
        self.assertEqual(instance.principalAdjustFactor, None)
        self.assertEqual(instance.date, datetime.date(2011, 7, 18))
        self.assertEqual(instance.type, enums.TransferType.ACATS)
        self.assertEqual(instance.direction, enums.InOut.IN)
        self.assertEqual(instance.company, None)
        self.assertEqual(instance.account, "12345678")
        self.assertEqual(instance.accountName, None)
        self.assertEqual(instance.quantity, decimal.Decimal("226702"))
        self.assertEqual(instance.transferPrice, decimal.Decimal("0"))
        self.assertEqual(instance.positionAmount, decimal.Decimal("11.51"))
        self.assertEqual(instance.positionAmountInBase, decimal.Decimal("11.51"))
        self.assertEqual(instance.pnlAmount, decimal.Decimal("0"))
        self.assertEqual(instance.pnlAmountInBase, decimal.Decimal("0"))
        self.assertEqual(instance.fxPnl, decimal.Decimal("0"))
        self.assertEqual(instance.cashTransfer, decimal.Decimal("0"))
        self.assertEqual(instance.code, ())
        self.assertEqual(instance.clientReference, None)


class CorporateActionTestCase(unittest.TestCase):
    data = ET.fromstring(
        ('<CorporateAction accountId="U123456" acctAlias="ibflex test" model="" '
         'currency="USD" fxRateToBase="1" assetCategory="STK" symbol="NILSY.TEN" '
         'description="NILSY.TEN(466992534) MERGED(Voluntary Offer Allocation)  FOR USD 30.60000000 PER SHARE (NILSY.TEN, MMC NORILSK NICKEL JSC-ADR - TENDER, 466992534)" '
         'conid="96835898" securityID="" securityIDType="" cusip="" isin="" '
         'underlyingConid="" underlyingSymbol="" issuer="" multiplier="1" strike="" '
         'expiry="" putCall="" principalAdjustFactor="" reportDate="2011-11-03" '
         'dateTime="2011-11-02;202500" amount="-30600" proceeds="30600" value="-18110" '
         'quantity="-1000" fifoPnlRealized="10315" mtmPnl="12490" code="" type="TC" />')
    )

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.CorporateAction)
        self.assertEqual(instance.accountId, "U123456")
        self.assertEqual(instance.acctAlias, "ibflex test")
        self.assertEqual(instance.model, None)
        self.assertEqual(instance.currency, "USD")
        self.assertEqual(instance.fxRateToBase, decimal.Decimal("1"))
        self.assertEqual(instance.assetCategory, enums.AssetClass.STOCK)
        self.assertEqual(instance.symbol, "NILSY.TEN")
        self.assertEqual(instance.description, "NILSY.TEN(466992534) MERGED(Voluntary Offer Allocation)  FOR USD 30.60000000 PER SHARE (NILSY.TEN, MMC NORILSK NICKEL JSC-ADR - TENDER, 466992534)")
        self.assertEqual(instance.conid, "96835898")
        self.assertEqual(instance.securityID, None)
        self.assertEqual(instance.securityIDType, None)
        self.assertEqual(instance.cusip, None)
        self.assertEqual(instance.isin, None)
        self.assertEqual(instance.underlyingConid, None)
        self.assertEqual(instance.underlyingSymbol, None)
        self.assertEqual(instance.issuer, None)
        self.assertEqual(instance.multiplier, decimal.Decimal("1"))
        self.assertEqual(instance.strike, None)
        self.assertEqual(instance.expiry, None)
        self.assertEqual(instance.putCall, None)
        self.assertEqual(instance.principalAdjustFactor, None)
        self.assertEqual(instance.reportDate, datetime.date(2011, 11, 3))
        self.assertEqual(instance.dateTime, datetime.datetime(2011, 11, 2, 20, 25, 0))
        self.assertEqual(instance.amount, decimal.Decimal("-30600"))
        self.assertEqual(instance.proceeds, decimal.Decimal("30600"))
        self.assertEqual(instance.value, decimal.Decimal("-18110"))
        self.assertEqual(instance.quantity, decimal.Decimal("-1000"))
        self.assertEqual(instance.fifoPnlRealized, decimal.Decimal("10315"))
        self.assertEqual(instance.mtmPnl, decimal.Decimal("12490"))
        self.assertEqual(instance.code, ())
        self.assertEqual(instance.type, enums.Reorg.MERGER)


class ChangeInDividendAccrualTestCase(unittest.TestCase):
    data = ET.fromstring(
        ('<ChangeInDividendAccrual accountId="U123456" acctAlias="ibflex test" '
         'model="" currency="USD" fxRateToBase="1" assetCategory="STK" symbol="RHDGF" '
         'description="RETAIL HOLDINGS NV" conid="62049667" securityID="ANN741081064" '
         'securityIDType="ISIN" cusip="" isin="ANN741081064" underlyingConid="" '
         'underlyingSymbol="" issuer="" multiplier="1" strike="" expiry="" putCall="" '
         'principalAdjustFactor="" date="2011-09-21" exDate="2011-09-22" '
         'payDate="2011-10-11" quantity="13592" tax="0" fee="0" grossRate="2.5" '
         'grossAmount="33980" netAmount="33980" code="Po" fromAcct="" toAcct="" />')
    )

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.ChangeInDividendAccrual)
        self.assertEqual(instance.accountId, "U123456")
        self.assertEqual(instance.acctAlias, "ibflex test")
        self.assertEqual(instance.model, None)
        self.assertEqual(instance.currency, "USD")
        self.assertEqual(instance.fxRateToBase, decimal.Decimal("1"))
        self.assertEqual(instance.assetCategory, enums.AssetClass.STOCK)
        self.assertEqual(instance.symbol, "RHDGF")
        self.assertEqual(instance.description, "RETAIL HOLDINGS NV")
        self.assertEqual(instance.conid, "62049667")
        self.assertEqual(instance.securityID, "ANN741081064")
        self.assertEqual(instance.securityIDType, "ISIN")
        self.assertEqual(instance.cusip, None)
        self.assertEqual(instance.isin, "ANN741081064")
        self.assertEqual(instance.underlyingConid, None)
        self.assertEqual(instance.underlyingSymbol, None)
        self.assertEqual(instance.issuer, None)
        self.assertEqual(instance.multiplier, decimal.Decimal("1"))
        self.assertEqual(instance.strike, None)
        self.assertEqual(instance.expiry, None)
        self.assertEqual(instance.putCall, None)
        self.assertEqual(instance.principalAdjustFactor, None)
        self.assertEqual(instance.date, datetime.date(2011, 9, 21))
        self.assertEqual(instance.exDate, datetime.date(2011, 9, 22))
        self.assertEqual(instance.payDate, datetime.date(2011, 10, 11))
        self.assertEqual(instance.quantity, decimal.Decimal("13592"))
        self.assertEqual(instance.tax, decimal.Decimal("0"))
        self.assertEqual(instance.fee, decimal.Decimal("0"))
        self.assertEqual(instance.grossRate, decimal.Decimal("2.5"))
        self.assertEqual(instance.grossAmount, decimal.Decimal("33980"))
        self.assertEqual(instance.netAmount, decimal.Decimal("33980"))
        self.assertEqual(instance.code, (enums.Code.POSTACCRUAL, ))
        self.assertEqual(instance.fromAcct, None)
        self.assertEqual(instance.toAcct, None)


class OpenDividendAccrualTestCase(unittest.TestCase):
    data = ET.fromstring(
        ('<OpenDividendAccrual accountId="U123456" acctAlias="ibflex test" model="" '
         'currency="USD" fxRateToBase="1" assetCategory="STK" symbol="CASH" '
         'description="META FINANCIAL GROUP INC" conid="3655441" securityID="" '
         'securityIDType="" cusip="" isin="" listingExchange="NYSE" underlyingConid="" '
         'underlyingSymbol="" underlyingSecurityID="" underlyingListingExchange="" '
         'issuer="" multiplier="1" strike="" expiry="" putCall="" '
         'principalAdjustFactor="" exDate="2011-12-08" payDate="2012-01-01" '
         'quantity="25383" tax="0" fee="0" grossRate="0.13" grossAmount="3299.79" '
         'netAmount="3299.79" code="" fromAcct="" toAcct="" />')
    )

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.OpenDividendAccrual)
        self.assertEqual(instance.accountId, "U123456")
        self.assertEqual(instance.acctAlias, "ibflex test")
        self.assertEqual(instance.model, None)
        self.assertEqual(instance.currency, "USD")
        self.assertEqual(instance.fxRateToBase, decimal.Decimal("1"))
        self.assertEqual(instance.assetCategory, enums.AssetClass.STOCK)
        self.assertEqual(instance.symbol, "CASH")
        self.assertEqual(instance.description, "META FINANCIAL GROUP INC")
        self.assertEqual(instance.conid, "3655441")
        self.assertEqual(instance.securityID, None)
        self.assertEqual(instance.securityIDType, None)
        self.assertEqual(instance.cusip, None)
        self.assertEqual(instance.isin, None)
        self.assertEqual(instance.listingExchange, "NYSE")
        self.assertEqual(instance.underlyingConid, None)
        self.assertEqual(instance.underlyingSymbol, None)
        self.assertEqual(instance.underlyingSecurityID, None)
        self.assertEqual(instance.underlyingListingExchange, None)
        self.assertEqual(instance.issuer, None)
        self.assertEqual(instance.multiplier, decimal.Decimal("1"))
        self.assertEqual(instance.strike, None)
        self.assertEqual(instance.expiry, None)
        self.assertEqual(instance.putCall, None)
        self.assertEqual(instance.principalAdjustFactor, None)
        self.assertEqual(instance.exDate, datetime.date(2011, 12, 8))
        self.assertEqual(instance.payDate, datetime.date(2012, 1, 1))
        self.assertEqual(instance.quantity, decimal.Decimal("25383"))
        self.assertEqual(instance.tax, decimal.Decimal("0"))
        self.assertEqual(instance.fee, decimal.Decimal("0"))
        self.assertEqual(instance.grossRate, decimal.Decimal("0.13"))
        self.assertEqual(instance.grossAmount, decimal.Decimal("3299.79"))
        self.assertEqual(instance.netAmount, decimal.Decimal("3299.79"))
        self.assertEqual(instance.code, ())
        self.assertEqual(instance.fromAcct, None)
        self.assertEqual(instance.toAcct, None)


class SecurityInfoTestCase(unittest.TestCase):
    data = ET.fromstring(
        ('<SecurityInfo assetCategory="STK" symbol="VXX" '
         'description="IPATH S&amp;P 500 VIX S/T FU ETN" conid="80789235" '
         'securityID="" securityIDType="" cusip="" isin="" underlyingConid="" '
         'underlyingSymbol="" issuer="" multiplier="1" strike="" expiry="" putCall="" '
         'principalAdjustFactor="1" maturity="" issueDate="" code="" />')
    )

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.SecurityInfo)
        self.assertEqual(instance.assetCategory, enums.AssetClass.STOCK)
        self.assertEqual(instance.symbol, "VXX")
        self.assertEqual(instance.description, "IPATH S&P 500 VIX S/T FU ETN")
        self.assertEqual(instance.conid, "80789235")
        self.assertEqual(instance.securityID, None)
        self.assertEqual(instance.securityIDType, None)
        self.assertEqual(instance.cusip, None)
        self.assertEqual(instance.isin, None)
        self.assertEqual(instance.underlyingConid, None)
        self.assertEqual(instance.underlyingSymbol, None)
        self.assertEqual(instance.issuer, None)
        self.assertEqual(instance.multiplier, decimal.Decimal("1"))
        self.assertEqual(instance.strike, None)
        self.assertEqual(instance.expiry, None)
        self.assertEqual(instance.putCall, None)
        self.assertEqual(instance.principalAdjustFactor, decimal.Decimal("1"))
        self.assertEqual(instance.maturity, None)
        self.assertEqual(instance.issueDate, None)
        self.assertEqual(instance.code, ())


class ConversionRateTestCase(unittest.TestCase):
    data = ET.fromstring(
        """<ConversionRate reportDate="2011-12-30" fromCurrency="HKD" toCurrency="USD" rate="0.12876" />"""
    )

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.ConversionRate)
        self.assertEqual(instance.reportDate, datetime.date(2011, 12, 30))
        self.assertEqual(instance.fromCurrency, "HKD")
        self.assertEqual(instance.toCurrency, "USD")
        self.assertEqual(instance.rate, decimal.Decimal("0.12876"))


class TransactionTaxTestCase(unittest.TestCase):
    data = ET.fromstring(
        ('<TransactionTax accountId="U123456" acctAlias="ibflex test" model="" currency="USD" '
        'fxRateToBase="1" assetCategory="STK" symbol="SNY" description="SANOFI-ADR" '
        'conid="1234578" securityID="80105N105" securityIDType="CUSIP" cusip="80105N105" '
         'isin="" listingExchange="NASDAQ" underlyingConid="" underlyingSymbol="" '
         'underlyingSecurityID="" underlyingListingExchange="" issuer="" multiplier="1" '
         'strike="" expiry="" putCall="" principalAdjustFactor="" date="2013-11-02" '
         'taxDescription="French Transaction Tax" quantity="0" reportDate="2013-11-02" '
         'taxAmount="-0.347098" tradeId="12345678550" tradePrice="0.0000" '
         'source="STANDALONE" code="" levelOfDetail="SUMMARY" />')
    )

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.TransactionTax)
        self.assertEqual(instance.accountId, "U123456")
        self.assertEqual(instance.acctAlias, "ibflex test")
        self.assertEqual(instance.model, None)
        self.assertEqual(instance.currency, "USD")
        self.assertEqual(instance.fxRateToBase, decimal.Decimal('1'))
        self.assertEqual(instance.assetCategory, enums.AssetClass.STOCK)
        self.assertEqual(instance.symbol, "SNY")
        self.assertEqual(instance.description, "SANOFI-ADR")
        self.assertEqual(instance.conid, "1234578")
        self.assertEqual(instance.securityID, "80105N105")
        self.assertEqual(instance.securityIDType, "CUSIP")
        self.assertEqual(instance.cusip, "80105N105")
        self.assertEqual(instance.isin, None)
        self.assertEqual(instance.listingExchange, "NASDAQ")
        self.assertEqual(instance.underlyingConid, None)
        self.assertEqual(instance.underlyingSymbol, None)
        self.assertEqual(instance.underlyingSecurityID, None)
        self.assertEqual(instance.underlyingListingExchange, None)
        self.assertEqual(instance.issuer, None)
        self.assertEqual(instance.multiplier, decimal.Decimal("1"))
        self.assertEqual(instance.strike, None)
        self.assertEqual(instance.expiry, None)
        self.assertEqual(instance.putCall, None)
        self.assertEqual(instance.principalAdjustFactor, None)
        self.assertEqual(instance.date, datetime.datetime(2013, 11, 2))
        self.assertEqual(instance.taxDescription, "French Transaction Tax")
        self.assertEqual(instance.quantity, decimal.Decimal('0'))
        self.assertEqual(instance.reportDate, datetime.date(2013, 11, 2))
        self.assertEqual(instance.taxAmount, decimal.Decimal("-0.347098"))
        self.assertEqual(instance.tradeId, "12345678550")
        self.assertEqual(instance.tradePrice, decimal.Decimal("0"))
        self.assertEqual(instance.source, "STANDALONE")
        self.assertEqual(instance.code, ())
        self.assertEqual(instance.levelOfDetail, "SUMMARY")


class SalesTaxTestCase(unittest.TestCase):
    data = ET.fromstring(
        ('<SalesTax accountId="U123456" acctAlias="" model="" currency="USD" '
         'fxRateToBase="1" assetCategory="" symbol="" description="" conid="" '
         'securityID="" securityIDType="" cusip="" isin="" listingExchange="" '
         'underlyingConid="" underlyingSymbol="" underlyingSecurityID="" '
         'underlyingListingExchange="" issuer="" multiplier="" strike="" '
         'expiry="" putCall="" principalAdjustFactor="" date="2015-01-03" '
         'country="Finland" taxType="VAT" payer="U123456" '
         'taxableDescription="b****32:CUSIP (NP)" taxableAmount="0.2" '
         'taxRate="0.21" salesTax="-0.042" taxableTransactionID="12913231356" '
         'transactionID="12913221785" code="" />'))

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.SalesTax)
        self.assertEqual(instance.accountId, "U123456")
        self.assertEqual(instance.acctAlias, None)
        self.assertEqual(instance.model, None)
        self.assertEqual(instance.currency, "USD")
        self.assertEqual(instance.fxRateToBase, decimal.Decimal('1'))
        self.assertEqual(instance.assetCategory, None)
        self.assertEqual(instance.symbol, None)
        self.assertEqual(instance.description, None)
        self.assertEqual(instance.conid, None)
        self.assertEqual(instance.securityID, None)
        self.assertEqual(instance.securityIDType, None)
        self.assertEqual(instance.cusip, None)
        self.assertEqual(instance.isin, None)
        self.assertEqual(instance.listingExchange, None)
        self.assertEqual(instance.underlyingConid, None)
        self.assertEqual(instance.underlyingSymbol, None)
        self.assertEqual(instance.underlyingSecurityID, None)
        self.assertEqual(instance.underlyingListingExchange, None)
        self.assertEqual(instance.issuer, None)
        self.assertEqual(instance.multiplier, None)
        self.assertEqual(instance.strike, None)
        self.assertEqual(instance.expiry, None)
        self.assertEqual(instance.putCall, None)
        self.assertEqual(instance.principalAdjustFactor, None)
        self.assertEqual(instance.date, datetime.date(2015, 1, 3))
        self.assertEqual(instance.country, "Finland")
        self.assertEqual(instance.taxType, "VAT")
        self.assertEqual(instance.payer, "U123456")
        self.assertEqual(instance.taxableDescription, "b****32:CUSIP (NP)")
        self.assertEqual(instance.taxableAmount, decimal.Decimal('0.2'))
        self.assertEqual(instance.taxRate, decimal.Decimal('0.21'))
        self.assertEqual(instance.salesTax, decimal.Decimal('-0.042'))
        self.assertEqual(instance.taxableTransactionID, "12913231356")
        self.assertEqual(instance.transactionID, "12913221785")
        self.assertEqual(instance.code, ())


class OrderTestCase(unittest.TestCase):
    data = ET.fromstring(
        ('<Order accountId="U123456" acctAlias="Test Account" model="" '
         'currency="USD" assetCategory="CASH" symbol="EUR.USD" '
         'description="EUR.USD" conid="12087792" securityID="" '
         'securityIDType="" cusip="" isin="" listingExchange="" '
         'underlyingConid="" underlyingSymbol="" underlyingSecurityID="" '
         'underlyingListingExchange="" issuer="" multiplier="1" strike="" '
         'expiry="" putCall="" principalAdjustFactor="" transactionType="" '
         'tradeID="" orderID="92965807" execID="" brokerageOrderID="" '
         'orderReference="" volatilityOrderLink="" clearingFirmID="" '
         'origTradePrice="" origTradeDate="" origTradeID="" '
         'orderTime="20210111;221652" dateTime="20210112;021624" '
         'reportDate="20210112" settleDate="20210114" tradeDate="20210112" '
         'exchange="" buySell="BUY" quantity="30000" price="1.21621" '
         'amount="36486.3" proceeds="-36486.3" commission="-2.557" '
         'brokerExecutionCommission="" brokerClearingCommission="" '
         'thirdPartyExecutionCommission="" thirdPartyClearingCommission="" '
         'thirdPartyRegulatoryCommission="" otherCommission="" '
         'commissionCurrency="CAD" tax="0" code="" orderType="LMT" '
         'levelOfDetail="ORDER" traderID="" isAPIOrder="" allocatedTo="" accruedInt="0" />'))

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.Order)
        self.assertEqual(instance.accountId, "U123456")
        self.assertEqual(instance.acctAlias, "Test Account")
        self.assertEqual(instance.model, None)
        self.assertEqual(instance.currency, "USD")
        self.assertEqual(instance.assetCategory, enums.AssetClass.CASH)
        self.assertEqual(instance.symbol, "EUR.USD")
        self.assertEqual(instance.description, "EUR.USD")
        self.assertEqual(instance.conid, "12087792")
        self.assertEqual(instance.securityID, None)
        self.assertEqual(instance.securityIDType, None)
        self.assertEqual(instance.cusip, None)
        self.assertEqual(instance.isin, None)
        self.assertEqual(instance.listingExchange, None)
        self.assertEqual(instance.underlyingConid, None)
        self.assertEqual(instance.underlyingSymbol, None)
        self.assertEqual(instance.underlyingSecurityID, None)
        self.assertEqual(instance.underlyingListingExchange, None)
        self.assertEqual(instance.issuer, None)
        self.assertEqual(instance.multiplier, decimal.Decimal('1'))
        self.assertEqual(instance.strike, None)
        self.assertEqual(instance.expiry, None)
        self.assertEqual(instance.putCall, None)
        self.assertEqual(instance.principalAdjustFactor, None)
        self.assertEqual(instance.transactionType, None)
        self.assertEqual(instance.tradeID, None)
        self.assertEqual(instance.orderID, decimal.Decimal('92965807'))
        self.assertEqual(instance.execID, None)
        self.assertEqual(instance.brokerageOrderID, None)
        self.assertEqual(instance.orderReference, None)
        self.assertEqual(instance.volatilityOrderLink, None)
        self.assertEqual(instance.clearingFirmID, None)
        self.assertEqual(instance.origTradePrice, None)
        self.assertEqual(instance.origTradeDate, None)
        self.assertEqual(instance.origTradeID, None)
        #  Despite the name, `orderTime` actually contains date/time data.
        self.assertEqual(instance.orderTime, datetime.datetime(2021, 1, 11, 22, 16, 52))
        self.assertEqual(instance.dateTime, datetime.datetime(2021, 1, 12, 2, 16, 24))
        self.assertEqual(instance.reportDate, datetime.date(2021, 1, 12))
        self.assertEqual(instance.settleDate, datetime.date(2021, 1, 14))
        self.assertEqual(instance.tradeDate, datetime.date(2021, 1, 12))
        self.assertEqual(instance.exchange, None)
        self.assertEqual(instance.buySell, enums.BuySell.BUY)
        self.assertEqual(instance.quantity, decimal.Decimal("30000"))
        self.assertEqual(instance.price, decimal.Decimal("1.21621"))
        self.assertEqual(instance.amount, decimal.Decimal("36486.3"))
        self.assertEqual(instance.proceeds, decimal.Decimal("-36486.3"))
        self.assertEqual(instance.commission, decimal.Decimal("-2.557"))
        self.assertEqual(instance.brokerExecutionCommission, None)
        self.assertEqual(instance.brokerClearingCommission, None)
        self.assertEqual(instance.thirdPartyExecutionCommission, None)
        self.assertEqual(instance.thirdPartyClearingCommission, None)
        self.assertEqual(instance.thirdPartyRegulatoryCommission, None)
        self.assertEqual(instance.otherCommission, None)
        self.assertEqual(instance.commissionCurrency, "CAD")
        self.assertEqual(instance.tax, decimal.Decimal("0"))
        self.assertEqual(instance.code, ())
        self.assertEqual(instance.orderType, enums.OrderType.LIMIT)
        self.assertEqual(instance.levelOfDetail, "ORDER")
        self.assertEqual(instance.traderID, None)
        self.assertEqual(instance.isAPIOrder, None)
        self.assertEqual(instance.allocatedTo, None)
        self.assertEqual(instance.accruedInt, decimal.Decimal("0"))


class SymbolSummaryTestCase(unittest.TestCase):
    data = ET.fromstring(
        ('<SymbolSummary accountId="U123456" acctAlias="Test Account" '
         'model="" currency="USD" assetCategory="CASH" symbol="EUR.USD" '
         'description="EUR.USD" conid="12087792" securityID="" '
         'securityIDType="" cusip="" isin="" listingExchange="" '
         'underlyingConid="" underlyingSymbol="" underlyingSecurityID="" '
         'underlyingListingExchange="" issuer="" multiplier="1" strike="" '
         'expiry="" putCall="" principalAdjustFactor="" transactionType="" '
         'tradeID="" orderID="" execID="" brokerageOrderID="" orderReference="" '
         'volatilityOrderLink="" clearingFirmID="" origTradePrice="" '
         'origTradeDate="" origTradeID="" orderTime="" dateTime="" '
         'reportDate="20210112" settleDate="20210114" tradeDate="20210112" '
         'exchange="IDEALFX" buySell="BUY" quantity="30000" price="1.21621" '
         'amount="36486.3" proceeds="-36486.3" commission="-2.557" '
         'brokerExecutionCommission="" brokerClearingCommission="" '
         'thirdPartyExecutionCommission="" thirdPartyClearingCommission="" '
         'thirdPartyRegulatoryCommission="" otherCommission="" '
         'commissionCurrency="CAD" tax="0" code="" orderType="" '
         'levelOfDetail="SYMBOL_SUMMARY" traderID="" isAPIOrder="" '
         'allocatedTo="" accruedInt="0" />'))

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.SymbolSummary)
        self.assertEqual(instance.accountId, "U123456")
        self.assertEqual(instance.acctAlias, "Test Account")
        self.assertEqual(instance.model, None)
        self.assertEqual(instance.currency, "USD")
        self.assertEqual(instance.assetCategory, enums.AssetClass.CASH)
        self.assertEqual(instance.symbol, "EUR.USD")
        self.assertEqual(instance.description, "EUR.USD")
        self.assertEqual(instance.conid, "12087792")
        self.assertEqual(instance.securityID, None)
        self.assertEqual(instance.securityIDType, None)
        self.assertEqual(instance.cusip, None)
        self.assertEqual(instance.isin, None)
        self.assertEqual(instance.listingExchange, None)
        self.assertEqual(instance.underlyingConid, None)
        self.assertEqual(instance.underlyingSymbol, None)
        self.assertEqual(instance.underlyingSecurityID, None)
        self.assertEqual(instance.underlyingListingExchange, None)
        self.assertEqual(instance.issuer, None)
        self.assertEqual(instance.multiplier, decimal.Decimal('1'))
        self.assertEqual(instance.strike, None)
        self.assertEqual(instance.expiry, None)
        self.assertEqual(instance.putCall, None)
        self.assertEqual(instance.principalAdjustFactor, None)
        self.assertEqual(instance.transactionType, None)
        self.assertEqual(instance.tradeID, None)
        self.assertEqual(instance.orderID, None)
        self.assertEqual(instance.execID, None)
        self.assertEqual(instance.brokerageOrderID, None)
        self.assertEqual(instance.orderReference, None)
        self.assertEqual(instance.volatilityOrderLink, None)
        self.assertEqual(instance.clearingFirmID, None)
        self.assertEqual(instance.origTradePrice, None)
        self.assertEqual(instance.origTradeDate, None)
        self.assertEqual(instance.origTradeID, None)
        #  Despite the name, `orderTime` actually contains date/time data.
        self.assertEqual(instance.orderTime, None)
        self.assertEqual(instance.dateTime, None)
        self.assertEqual(instance.reportDate, datetime.date(2021, 1, 12))
        self.assertEqual(instance.settleDate, datetime.date(2021, 1, 14))
        self.assertEqual(instance.tradeDate, datetime.date(2021, 1, 12))
        self.assertEqual(instance.exchange, "IDEALFX")
        self.assertEqual(instance.buySell, enums.BuySell.BUY)
        self.assertEqual(instance.quantity, decimal.Decimal("30000"))
        self.assertEqual(instance.price, decimal.Decimal("1.21621"))
        self.assertEqual(instance.amount, decimal.Decimal("36486.3"))
        self.assertEqual(instance.proceeds, decimal.Decimal("-36486.3"))
        self.assertEqual(instance.commission, decimal.Decimal("-2.557"))
        self.assertEqual(instance.brokerExecutionCommission, None)
        self.assertEqual(instance.brokerClearingCommission, None)
        self.assertEqual(instance.thirdPartyExecutionCommission, None)
        self.assertEqual(instance.thirdPartyClearingCommission, None)
        self.assertEqual(instance.thirdPartyRegulatoryCommission, None)
        self.assertEqual(instance.otherCommission, None)
        self.assertEqual(instance.commissionCurrency, "CAD")
        self.assertEqual(instance.tax, decimal.Decimal("0"))
        self.assertEqual(instance.code, ())
        self.assertEqual(instance.orderType, None)
        self.assertEqual(instance.levelOfDetail, "SYMBOL_SUMMARY")
        self.assertEqual(instance.traderID, None)
        self.assertEqual(instance.isAPIOrder, None)
        self.assertEqual(instance.allocatedTo, None)
        self.assertEqual(instance.accruedInt, decimal.Decimal("0"))


class ChangeInNAVTestCase(unittest.TestCase):

    data = ET.fromstring(
    ('<ChangeInNAV accountId="myaccount" acctAlias="myaccount" fromDate="20210224" toDate="20210224" startingValue="234.567" '
    'endingValue="1234.56" depositsWithdrawals="0" debitCardActivity="0" billPay="0" mtm="11.11" model="" '
    'realized="0" changeInUnrealized="0" costAdjustments="0" transferredPnlAdjustments="0" internalCashTransfers="0" '
    'excessFundSweep="0" assetTransfers="0" grantActivity="0" dividends="0" withholdingTax="0" withholding871m="0" '
    'withholdingTaxCollected="0" changeInDividendAccruals="0" interest="0" changeInInterestAccruals="0" advisorFees="0" '
    'clientFees="0" otherFees="0" feesReceivables="0" commissions="-7.5951887" commissionCreditsRedemption="0" '
    'commissionReceivables="0" forexCommissions="0" transactionTax="0" taxReceivables="0" salesTax="0" billableSalesTax="0" '
    'softDollars="0" netFxTrading="0" fxTranslation="0" linkingAdjustments="0" other="0" twr="0.30531605"'
    ' corporateActionProceeds="0" />'))

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.ChangeInNAV)
        self.assertEqual(instance.accountId, "myaccount")
        self.assertEqual(instance.acctAlias, "myaccount")
        self.assertEqual(instance.fromDate, datetime.date(2021, 2, 24))
        self.assertEqual(instance.toDate, datetime.date(2021, 2, 24))
        self.assertEqual(instance.startingValue, decimal.Decimal("234.567"))
        self.assertEqual(instance.endingValue, decimal.Decimal("1234.56"))
        self.assertEqual(instance.depositsWithdrawals, decimal.Decimal("0"))
        self.assertEqual(instance.debitCardActivity, decimal.Decimal("0"))
        self.assertEqual(instance.billPay, decimal.Decimal("0"))
        self.assertEqual(instance.mtm, decimal.Decimal("11.11"))
        self.assertEqual(instance.model, None)
        self.assertEqual(instance.realized, decimal.Decimal("0"))
        self.assertEqual(instance.changeInUnrealized, decimal.Decimal("0"))
        self.assertEqual(instance.costAdjustments, decimal.Decimal("0"))
        self.assertEqual(instance.transferredPnlAdjustments, decimal.Decimal("0"))
        self.assertEqual(instance.internalCashTransfers, decimal.Decimal("0"))
        self.assertEqual(instance.excessFundSweep, decimal.Decimal("0"))
        self.assertEqual(instance.assetTransfers, decimal.Decimal("0"))
        self.assertEqual(instance.grantActivity, decimal.Decimal("0"))
        self.assertEqual(instance.dividends, decimal.Decimal("0"))
        self.assertEqual(instance.withholdingTax, decimal.Decimal("0"))
        self.assertEqual(instance.withholding871m, decimal.Decimal("0"))
        self.assertEqual(instance.withholdingTaxCollected, decimal.Decimal("0"))
        self.assertEqual(instance.changeInDividendAccruals, decimal.Decimal("0"))
        self.assertEqual(instance.interest, decimal.Decimal("0"))
        self.assertEqual(instance.changeInInterestAccruals, decimal.Decimal("0"))
        self.assertEqual(instance.advisorFees, decimal.Decimal("0"))
        self.assertEqual(instance.clientFees, decimal.Decimal("0"))
        self.assertEqual(instance.otherFees, decimal.Decimal("0"))
        self.assertEqual(instance.feesReceivables, decimal.Decimal("0"))
        self.assertEqual(instance.commissions, decimal.Decimal("-7.5951887"))
        self.assertEqual(instance.commissionCreditsRedemption, decimal.Decimal("0"))
        self.assertEqual(instance.commissionReceivables, decimal.Decimal("0"))
        self.assertEqual(instance.forexCommissions, decimal.Decimal("0"))
        self.assertEqual(instance.transactionTax, decimal.Decimal("0"))
        self.assertEqual(instance.taxReceivables, decimal.Decimal("0"))
        self.assertEqual(instance.salesTax, decimal.Decimal("0"))
        self.assertEqual(instance.billableSalesTax, decimal.Decimal("0"))
        self.assertEqual(instance.softDollars, decimal.Decimal("0"))
        self.assertEqual(instance.netFxTrading, decimal.Decimal("0"))
        self.assertEqual(instance.fxTranslation, decimal.Decimal("0"))
        self.assertEqual(instance.linkingAdjustments, decimal.Decimal("0"))
        self.assertEqual(instance.other, decimal.Decimal("0"))
        self.assertEqual(instance.twr, decimal.Decimal("0.30531605"))


class TradesOrderTestCase(unittest.TestCase):
    """This example of Order comes from a flex report made by clicking Trades->Orders->Select All"""

    data = ET.fromstring(
    ('<Order buySell="BUY" quantity="3" netCash="-876.9314" dateTime="2021-02-03 10:01:50" tradePrice="2.92" '
    'acctAlias="myaccount" assetCategory="OPT" description="IWM 19MAR21 226.0 C" conid="467957000" '
    'underlyingConid="9579970" underlyingSymbol="IWM" multiplier="100" strike="226" expiry="2021-03-19" '
    'putCall="C" ibCommission="-0.9314" ibOrderID="1722040385" accountId="myaccount" model="Independent" '
    'currency="USD" fxRateToBase="1" symbol="IWM   210319C00226000" securityID="" securityIDType="" cusip="" '
    'isin="" listingExchange="CBOE" underlyingSecurityID="US4642876555" underlyingListingExchange="ARCA" issuer="" '
    'tradeID="" reportDate="2021-02-03" principalAdjustFactor="" tradeDate="2021-02-03" settleDateTarget="2021-02-04" '
    'transactionType="" exchange="" tradeMoney="876" proceeds="-876" taxes="0" ibCommissionCurrency="USD" closePrice="3.08" '
    'openCloseIndicator="-" notes="P" cost="876.9314" fifoPnlRealized="0" fxPnl="0" mtmPnl="48" origTradePrice="" '
    'origTradeDate="" origTradeID="" origOrderID="" clearingFirmID="" transactionID="" ibExecID="" brokerageOrderID="" '
    'orderReference="" volatilityOrderLink="" exchOrderId="" extExecID="" orderTime="2021-02-03 10:01:50" openDateTime="" '
    'holdingPeriodDateTime="" whenRealized="" whenReopened="" levelOfDetail="ORDER" changeInPrice="" changeInQuantity="" '
    'orderType="LMT;MKT" traderID="" isAPIOrder="" accruedInt="0" />'))

    def testParse(self):
        instance = parser.parse_data_element(self.data)
        self.assertIsInstance(instance, Types.Order)

        self.assertEqual(instance.buySell, enums.BuySell.BUY)
        self.assertEqual(instance.quantity, decimal.Decimal("3"))
        self.assertEqual(instance.netCash, decimal.Decimal("-876.9314"))
        self.assertEqual(instance.dateTime, datetime.datetime(2021, 2, 3, 10, 1, 50))
        self.assertEqual(instance.tradePrice, decimal.Decimal("2.92"))
        self.assertEqual(instance.acctAlias, "myaccount")
        self.assertEqual(instance.assetCategory, enums.AssetClass.OPTION)
        self.assertEqual(instance.description, "IWM 19MAR21 226.0 C")
        self.assertEqual(instance.conid, "467957000")
        self.assertEqual(instance.underlyingConid, "9579970")
        self.assertEqual(instance.underlyingSymbol, "IWM")
        self.assertEqual(instance.multiplier, decimal.Decimal("100"))
        self.assertEqual(instance.strike, decimal.Decimal("226"))
        self.assertEqual(instance.expiry, datetime.date(2021, 3, 19))
        self.assertEqual(instance.putCall, enums.PutCall.CALL)
        self.assertEqual(instance.ibCommission, decimal.Decimal("-0.9314"))
        self.assertEqual(instance.ibOrderID, "1722040385")
        self.assertEqual(instance.accountId, "myaccount")
        self.assertEqual(instance.model, "Independent")
        self.assertEqual(instance.currency, "USD")
        self.assertEqual(instance.fxRateToBase, decimal.Decimal("1"))
        self.assertEqual(instance.symbol, "IWM   210319C00226000")
        self.assertEqual(instance.securityID, None)
        self.assertEqual(instance.securityIDType, None)
        self.assertEqual(instance.cusip, None)
        self.assertEqual(instance.isin, None)
        self.assertEqual(instance.listingExchange, "CBOE")
        self.assertEqual(instance.underlyingSecurityID, "US4642876555")
        self.assertEqual(instance.underlyingListingExchange, "ARCA")
        self.assertEqual(instance.issuer, None)
        self.assertEqual(instance.tradeID, None)
        self.assertEqual(instance.reportDate, datetime.date(2021, 2, 3))
        self.assertEqual(instance.principalAdjustFactor, None)
        self.assertEqual(instance.tradeDate, datetime.date(2021, 2, 3))
        self.assertEqual(instance.settleDateTarget, datetime.date(2021, 2, 4))
        self.assertEqual(instance.transactionType, None)
        self.assertEqual(instance.exchange, None)
        self.assertEqual(instance.tradeMoney, decimal.Decimal("876"))
        self.assertEqual(instance.proceeds, decimal.Decimal("-876"))
        self.assertEqual(instance.taxes, decimal.Decimal("0"))
        self.assertEqual(instance.ibCommissionCurrency, "USD")
        self.assertEqual(instance.closePrice, decimal.Decimal("3.08"))
        self.assertEqual(instance.openCloseIndicator, enums.OpenClose.UNKNOWN)
        self.assertEqual(instance.notes, "P")
        self.assertEqual(instance.cost, decimal.Decimal("876.9314"))
        self.assertEqual(instance.fifoPnlRealized, decimal.Decimal("0"))
        self.assertEqual(instance.fxPnl, decimal.Decimal("0"))
        self.assertEqual(instance.mtmPnl, decimal.Decimal("48")) 
        self.assertEqual(instance.origTradePrice, None)
        self.assertEqual(instance.origTradeDate, None)
        self.assertEqual(instance.origTradeID, None)
        self.assertEqual(instance.origOrderID, None)
        self.assertEqual(instance.clearingFirmID, None)
        self.assertEqual(instance.transactionID, None)
        self.assertEqual(instance.ibExecID, None)
        self.assertEqual(instance.brokerageOrderID, None)
        self.assertEqual(instance.orderReference, None)
        self.assertEqual(instance.volatilityOrderLink, None)
        self.assertEqual(instance.exchOrderId, None)
        self.assertEqual(instance.extExecID, None)
        self.assertEqual(instance.orderTime, datetime.datetime(2021, 2, 3, 10, 1, 50))
        self.assertEqual(instance.openDateTime, None) 
        self.assertEqual(instance.holdingPeriodDateTime, None)
        self.assertEqual(instance.whenRealized, None)
        self.assertEqual(instance.whenReopened, None)
        self.assertEqual(instance.levelOfDetail, "ORDER")
        self.assertEqual(instance.changeInPrice, None)
        self.assertEqual(instance.changeInQuantity, None)
        self.assertEqual(instance.orderType, enums.OrderType.MULTIPLE)
        self.assertEqual(instance.traderID, None)
        self.assertEqual(instance.isAPIOrder, None)
        self.assertEqual(instance.accruedInt, decimal.Decimal("0"))



if __name__ == '__main__':
    unittest.main(verbosity=3)
