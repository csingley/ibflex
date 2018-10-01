# coding: utf-8
"""
Schemata for type conversion and validation of Interactive Brokers Flex Query
data, as parsed by ElementTree.

https://www.interactivebrokers.com/en/software/reportguide/reportguide.htm#reportguide/activity_flex_query_reference.htm
"""
# stdlib imports
import itertools


# local imports
from ibflex.fields import (
    Field, Boolean, String, Integer, Decimal, OneOf, Time, Date, DateTime, List
)
from ibflex.fieldutils import CURRENCY_CODES


class FlexSchemaError(Exception):
    """ Base class for errors in this module """
    pass


class SchemaMetaclass(type):
    """
    Metaclass for Schema class.  Removes the fields declared on Schema
    subclasses, and rebinds them to a ``fields`` attribute, which is a dict
    mapping attribute names to field objects.
    """
    def __new__(metacls, clsname, bases, attrs):
        # Create the class
        cls = super(SchemaMetaclass, metacls).__new__(metacls, clsname, bases, attrs)

        # Collect inherited Fields into fields attribute
        # Iterate through MRO in reverse to preserve correct inheritance order
        fields_ = {}
        for base in cls.__mro__[:0:-1]:
            for name in dir(base):
                attr = getattr(base, name)
                if isinstance(attr, Field):
                    fields_[name] = attr

        # Collect declared Fields into fields attribute
        fields_.update({k: v for k, v in attrs.items() if isinstance(v, Field)})

        cls.fields = fields_
        return cls


class Schema(metaclass=SchemaMetaclass):
    """
    Base schema class with which to define custom schemata.
    """
    @classmethod
    def convert(cls, elem):
        data = elem.attrib
        output = {key: field.convert(data.pop(key, None))
                  for key, field in cls.fields.items()}
        if data:
            msg = "{} schema doesn't define {}".format(cls.__name__,
                                                       list(data.keys()))
            raise FlexSchemaError(msg)
        return output


###############################################################################
# MIXINS
###############################################################################
class AccountMixin(object):
    accountId = String()
    acctAlias = String()
    model = String()


class CurrencyMixin(object):
    currency = OneOf(*CURRENCY_CODES)
    fxRateToBase = Decimal()


class SecurityMixin(object):
    assetCategory = String()
    symbol = String()
    description = String()
    conid = String()
    securityID = String()
    securityIDType = String()
    cusip = String()
    isin = String()
    underlyingConid = String()
    underlyingSymbol = String()
    issuer = String()
    multiplier = Decimal()
    strike = Decimal()
    expiry = Date()
    putCall = String()
    principalAdjustFactor = Decimal()


class TradeMixin(AccountMixin, CurrencyMixin, SecurityMixin):
    tradeID = String()
    reportDate = Date()
    tradeDate = Date()
    tradeTime = Time()
    settleDateTarget = Date()
    transactionType = OneOf(
        "ExchTrade", "TradeCancel", "FracShare", "FracShareCancel",
        "TradeCorrect", "BookTrade", "DvpTrade")
    exchange = String()
    quantity = Decimal()
    tradePrice = Decimal()
    tradeMoney = Decimal()
    proceeds = Decimal()
    taxes = Decimal()
    ibCommission = Decimal()
    ibCommissionCurrency = OneOf(*CURRENCY_CODES)
    netCash = Decimal()
    closePrice = Decimal()
    openCloseIndicator = OneOf("O", "C", "C;O")
    notes = List(separator=';')
    cost = Decimal()
    fifoPnlRealized = Decimal()
    fxPnl = Decimal()
    mtmPnl = Decimal()
    origTradePrice = Decimal()
    origTradeDate = Date()
    origTradeID = String()
    origOrderID = String()
    clearingFirmID = String()
    transactionID = String()
    openDateTime = DateTime()
    holdingPeriodDateTime = DateTime()
    whenRealized = DateTime()
    whenReopened = DateTime()
    levelOfDetail = OneOf(
        "EXECUTION", "ORDER", "CLOSED_LOT", "TRADE_TRANSFERS")


class DividendAccrualMixin(AccountMixin, CurrencyMixin, SecurityMixin):
    exDate = Date()
    payDate = Date()
    quantity = Decimal()
    tax = Decimal()
    fee = Decimal()
    grossRate = Decimal()
    grossAmount = Decimal()
    netAmount = Decimal()
    code = List()
    fromAcct = String()
    toAcct = String()


###############################################################################
# SCHEMATA
###############################################################################
class FlexQueryResponse(Schema):
    """ Top-level element """
    queryName = String()
    type = String()


class FlexStatements(Schema):
    """ Wrapped in <FlexQueryResponse> """
    count = Integer()


class FlexStatement(Schema):
    accountId = String()
    fromDate = Date()
    toDate = Date()
    period = String()
    whenGenerated = DateTime()


class AccountInformation(Schema):
    accountId = String()
    acctAlias = String()
    currency = OneOf(*CURRENCY_CODES)
    name = String()
    accountType = OneOf(
        "Individual", "Institution Master", "Institution Client",
        "Advisor Master", "Advisor Master Consolidated", "Advisor Client",
        "Broker Master", "Broker Master Consolidated", "Broker Client",
        "Fund Advisor")
    customerType = OneOf(
        "Individual", "Joint", "Trust", "IRA", "Corporate", "Partnership",
        "Limited Liability Corporation", "Unincorporated Business",
        "IRA Traditional Rollover", "IRA Traditional New",
        "IRA Traditional Inherited", "IRA Roth New", "IRA Roth Inherited",
        "IRA SEP New", "IRA SEP Inherited")
    accountCapabilities = List(
        valid=["Cash", "Margin", "Portfolio Margin", "IBPrime"])
    tradingPermissions = List(
        valid=["Stocks", "Options", "Mutual Funds", "Futures", "Forex",
               "Bonds", "CFDs", "IBG Notes", "Warrants", "US Treasury Bills",
               "Futures Options", "SSF", "Stock Loan",
               "Stock Borrow"])
    dateOpened = Date()
    dateFunded = Date()
    dateClosed = Date()
    masterName = String()
    ibEntity = OneOf("IBLLC-US", "IB-UK", "IB-UKL", "IB-CAN", "IB-JP", "IB-IN")


class EquitySummaryByReportDateInBase(Schema, AccountMixin):
    """ Wrapped in <EquitySummaryInBase> """
    reportDate = Date()
    cash = Decimal()
    cashLong = Decimal()
    cashShort = Decimal()
    slbCashCollateral = Decimal()
    slbCashCollateralLong = Decimal()
    slbCashCollateralShort = Decimal()
    stock = Decimal()
    stockLong = Decimal()
    stockShort = Decimal()
    slbDirectSecuritiesBorrowed = Decimal()
    slbDirectSecuritiesBorrowedLong = Decimal()
    slbDirectSecuritiesBorrowedShort = Decimal()
    slbDirectSecuritiesLent = Decimal()
    slbDirectSecuritiesLentLong = Decimal()
    slbDirectSecuritiesLentShort = Decimal()
    options = Decimal()
    optionsLong = Decimal()
    optionsShort = Decimal()
    commodities = Decimal()
    commoditiesLong = Decimal()
    commoditiesShort = Decimal()
    bonds = Decimal()
    bondsLong = Decimal()
    bondsShort = Decimal()
    notes = Decimal()
    notesLong = Decimal()
    notesShort = Decimal()
    funds = Decimal()
    fundsLong = Decimal()
    fundsShort = Decimal()
    interestAccruals = Decimal()
    interestAccrualsLong = Decimal()
    interestAccrualsShort = Decimal()
    softDollars = Decimal()
    softDollarsLong = Decimal()
    softDollarsShort = Decimal()
    forexCfdUnrealizedPl = Decimal()
    forexCfdUnrealizedPlLong = Decimal()
    forexCfdUnrealizedPlShort = Decimal()
    dividendAccruals = Decimal()
    dividendAccrualsLong = Decimal()
    dividendAccrualsShort = Decimal()
    fdicInsuredBankSweepAccount = Decimal()
    fdicInsuredBankSweepAccountLong = Decimal()
    fdicInsuredBankSweepAccountShort = Decimal()
    fdicInsuredBankSweepAccountCashComponent = Decimal()
    fdicInsuredBankSweepAccountCashComponentLong = Decimal()
    fdicInsuredBankSweepAccountCashComponentShort = Decimal()
    fdicInsuredAccountInterestAccruals = Decimal()
    fdicInsuredAccountInterestAccrualsLong = Decimal()
    fdicInsuredAccountInterestAccrualsShort = Decimal()
    fdicInsuredAccountInterestAccrualsComponent = Decimal()
    fdicInsuredAccountInterestAccrualsComponentLong = Decimal()
    fdicInsuredAccountInterestAccrualsComponentShort = Decimal()
    total = Decimal()
    totalLong = Decimal()
    totalShort = Decimal()
    brokerInterestAccrualsComponent = Decimal()
    brokerCashComponent = Decimal()
    cfdUnrealizedPl = Decimal()

    
class CashReportCurrency(Schema, AccountMixin):
    """ Wrapped in <CashReport> """
    currency = OneOf(*CURRENCY_CODES)
    fromDate = Date()
    toDate = Date()
    startingCash = Decimal()
    startingCashSec = Decimal()
    startingCashCom = Decimal()
    clientFees = Decimal()
    clientFeesSec = Decimal()
    clientFeesCom = Decimal()
    clientFeesMTD = Decimal()
    clientFeesYTD = Decimal()
    commissions = Decimal()
    commissionsSec = Decimal()
    commissionsCom = Decimal()
    commissionsMTD = Decimal()
    commissionsYTD = Decimal()
    billableCommissions = Decimal()
    billableCommissionsSec = Decimal()
    billableCommissionsCom = Decimal()
    billableCommissionsMTD = Decimal()
    billableCommissionsYTD = Decimal()
    depositWithdrawals = Decimal()
    depositWithdrawalsSec = Decimal()
    depositWithdrawalsCom = Decimal()
    depositWithdrawalsMTD = Decimal()
    depositWithdrawalsYTD = Decimal()
    deposits = Decimal()
    depositsSec = Decimal()
    depositsCom = Decimal()
    depositsMTD = Decimal()
    depositsYTD = Decimal()
    withdrawals = Decimal()
    withdrawalsSec = Decimal()
    withdrawalsCom = Decimal()
    withdrawalsMTD = Decimal()
    withdrawalsYTD = Decimal()
    accountTransfers = Decimal()
    accountTransfersSec = Decimal()
    accountTransfersCom = Decimal()
    accountTransfersMTD = Decimal()
    accountTransfersYTD = Decimal()
    linkingAdjustments = Decimal()
    linkingAdjustmentsSec = Decimal()
    linkingAdjustmentsCom = Decimal()
    internalTransfers = Decimal()
    internalTransfersSec = Decimal()
    internalTransfersCom = Decimal()
    internalTransfersMTD = Decimal()
    internalTransfersYTD = Decimal()
    dividends = Decimal()
    dividendsSec = Decimal()
    dividendsCom = Decimal()
    dividendsMTD = Decimal()
    dividendsYTD = Decimal()
    insuredDepositInterest = Decimal()
    insuredDepositInterestSec = Decimal()
    insuredDepositInterestCom = Decimal()
    insuredDepositInterestMTD = Decimal()
    insuredDepositInterestYTD = Decimal()
    brokerInterest = Decimal()
    brokerInterestSec = Decimal()
    brokerInterestCom = Decimal()
    brokerInterestMTD = Decimal()
    brokerInterestYTD = Decimal()
    bondInterest = Decimal()
    bondInterestSec = Decimal()
    bondInterestCom = Decimal()
    bondInterestMTD = Decimal()
    bondInterestYTD = Decimal()
    cashSettlingMtm = Decimal()
    cashSettlingMtmSec = Decimal()
    cashSettlingMtmCom = Decimal()
    cashSettlingMtmMTD = Decimal()
    cashSettlingMtmYTD = Decimal()
    realizedVm = Decimal()
    realizedVmSec = Decimal()
    realizedVmCom = Decimal()
    realizedVmMTD = Decimal()
    realizedVmYTD = Decimal()
    cfdCharges = Decimal()
    cfdChargesSec = Decimal()
    cfdChargesCom = Decimal()
    cfdChargesMTD = Decimal()
    cfdChargesYTD = Decimal()
    netTradesSales = Decimal()
    netTradesSalesSec = Decimal()
    netTradesSalesCom = Decimal()
    netTradesSalesMTD = Decimal()
    netTradesSalesYTD = Decimal()
    netTradesPurchases = Decimal()
    netTradesPurchasesSec = Decimal()
    netTradesPurchasesCom = Decimal()
    netTradesPurchasesMTD = Decimal()
    netTradesPurchasesYTD = Decimal()
    advisorFees = Decimal()
    advisorFeesSec = Decimal()
    advisorFeesCom = Decimal()
    advisorFeesMTD = Decimal()
    advisorFeesYTD = Decimal()
    feesReceivables = Decimal()
    feesReceivablesSec = Decimal()
    feesReceivablesCom = Decimal()
    feesReceivablesMTD = Decimal()
    feesReceivablesYTD = Decimal()
    paymentInLieu = Decimal()
    paymentInLieuSec = Decimal()
    paymentInLieuCom = Decimal()
    paymentInLieuMTD = Decimal()
    paymentInLieuYTD = Decimal()
    transactionTax = Decimal()
    transactionTaxSec = Decimal()
    transactionTaxCom = Decimal()
    transactionTaxMTD = Decimal()
    transactionTaxYTD = Decimal()
    taxReceivables = Decimal()
    taxReceivablesSec = Decimal()
    taxReceivablesCom = Decimal()
    taxReceivablesMTD = Decimal()
    taxReceivablesYTD = Decimal()
    withholdingTax = Decimal()
    withholdingTaxSec = Decimal()
    withholdingTaxCom = Decimal()
    withholdingTaxMTD = Decimal()
    withholdingTaxYTD = Decimal()
    withholding871m = Decimal()
    withholding871mSec = Decimal()
    withholding871mCom = Decimal()
    withholding871mMTD = Decimal()
    withholding871mYTD = Decimal()
    withholdingCollectedTax = Decimal()
    withholdingCollectedTaxSec = Decimal()
    withholdingCollectedTaxCom = Decimal()
    withholdingCollectedTaxMTD = Decimal()
    withholdingCollectedTaxYTD = Decimal()
    salesTax = Decimal()
    salesTaxSec = Decimal()
    salesTaxCom = Decimal()
    salesTaxMTD = Decimal()
    salesTaxYTD = Decimal()
    fxTranslationGainLoss = Decimal()
    fxTranslationGainLossSec = Decimal()
    fxTranslationGainLossCom = Decimal()
    otherFees = Decimal()
    otherFeesSec = Decimal()
    otherFeesCom = Decimal()
    otherFeesMTD = Decimal()
    otherFeesYTD = Decimal()
    other = Decimal()
    otherSec = Decimal()
    otherCom = Decimal()
    endingCash = Decimal()
    endingCashSec = Decimal()
    endingCashCom = Decimal()
    endingSettledCash = Decimal()
    endingSettledCashSec = Decimal()
    endingSettledCashCom = Decimal()


class StatementOfFundsLine(Schema, AccountMixin, SecurityMixin):
    """ Wrapped in <StmtFunds> """
    currency = OneOf(*CURRENCY_CODES)
    reportDate = Date()
    date = Date()
    activityDescription = String()
    tradeID = String()
    debit = Decimal()
    credit = Decimal()
    amount = Decimal()
    balance = Decimal()
    buySell = String()


class ChangeInPositionValue(Schema, AccountMixin):
    """ Wrapped in <ChangeInPositionValues> """
    currency = OneOf(*CURRENCY_CODES)
    assetCategory = String()
    priorPeriodValue = Decimal()
    transactions = Decimal()
    mtmPriorPeriodPositions = Decimal()
    mtmTransactions = Decimal()
    corporateActions = Decimal()
    other = Decimal()
    accountTransfers = Decimal()
    linkingAdjustments = Decimal()
    fxTranslationPnl = Decimal()
    futurePriceAdjustments = Decimal()
    settledCash = Decimal()
    endOfPeriodValue = Decimal()


class OpenPosition(Schema, AccountMixin, CurrencyMixin, SecurityMixin):
    """ Wrapped in <OpenPositions> """
    reportDate = Date()
    position = Decimal()
    markPrice = Decimal()
    positionValue = Decimal()
    openPrice = Decimal()
    costBasisPrice = Decimal()
    costBasisMoney = Decimal()
    percentOfNAV = Decimal()
    fifoPnlUnrealized = Decimal()
    side = OneOf('Long', 'Short')
    levelOfDetail = OneOf('LOT', 'SUMMARY')
    openDateTime = DateTime()
    holdingPeriodDateTime = DateTime()
    code = List()
    originatingOrderID = String()
    originatingTransactionID = String()
    accruedInt = String()


class FxLot(Schema, AccountMixin):
    """ Wrapped in <FxLots> """
    assetCategory = String()
    reportDate = Date()
    functionalCurrency = OneOf(*CURRENCY_CODES)
    fxCurrency = OneOf(*CURRENCY_CODES)
    quantity = Decimal()
    costPrice = Decimal()
    costBasis = Decimal()
    closePrice = Decimal()
    value = Decimal()
    unrealizedPL = Decimal()
    code = List()
    lotDescription = String()
    lotOpenDateTime = DateTime()
    levelOfDetail = OneOf('LOT', 'SUMMARY')


class Trade(Schema, TradeMixin):
    """ Wrapped in <Trades> """
    buySell = OneOf("BUY", "BUY (Ca.)", "SELL", "SELL (Ca.)")
    ibOrderID = String()
    ibExecID = String()
    brokerageOrderID = String()
    orderReference = String()
    volatilityOrderLink = String()
    exchOrderId = String()
    extExecID = String()
    # Despite the name, orderTime actually contains both date & time data.
    orderTime = DateTime()
    changeInPrice = Decimal()
    changeInQuantity = Decimal()
    orderType = OneOf("LMT", "MKT")
    traderID = String()
    isAPIOrder = Boolean()


class TradeConfirmation(Schema, TradeMixin):
    """ Wrapped in <TradeConfirms> """
    buySell = OneOf("BUY", "BUY (Ca.)", "SELL", "SELL (Ca.)")
    levelOfDetail = OneOf("SYMBOL_SUMMARY", "ORDER", "EXECUTION")
    commissionCurrency = OneOf(*CURRENCY_CODES)
    price = Decimal()
    thirdPartyClearingCommission = Decimal()
    orderID = Decimal()
    allocatedTo = String()
    thirdPartyRegulatoryCommission = Decimal()
    dateTime = DateTime()
    brokerExecutionCommission = Decimal()
    thirdPartyExecutionCommission = Decimal()
    amount = Decimal()
    otherCommission = Decimal()
    commission = Decimal()
    brokerClearingCommission = Decimal()
    ibOrderID = String()
    ibExecID = String()
    execID = String()
    brokerageOrderID = String()
    orderReference = String()
    volatilityOrderLink = String()
    exchOrderId = String()
    extExecID = String()
    # Despite the name, orderTime actually contains both date & time data.
    orderTime = DateTime()
    changeInPrice = Decimal()
    changeInQuantity = Decimal()
    orderType = OneOf("LMT", "MKT", "MOC")
    traderID = String()
    isAPIOrder = Boolean()
    code = List()
    tax = Decimal()
    listingExchange = String()
    underlyingListingExchange = String()
    settleDate = String()
    underlyingSecurityID = String()

    
class OptionEAE(Schema, AccountMixin, CurrencyMixin, SecurityMixin):
    """
    Option Exercise, Assignment, or Expiration

    Wrapped in (identically-named) <OptionEAE>
    """
    date = Date()
    transactionType = OneOf("Assignment", "Exercise", "Expiration", "Sell")
    quantity = Decimal()
    tradePrice = Decimal()
    markPrice = Decimal()
    proceeds = Decimal()
    commisionsAndTax = Decimal()
    costBasis = Decimal()
    realizedPnl = Decimal()
    fxPnl = Decimal()
    mtmPnl = Decimal()
    tradeID = String()


class TradeTransfer(Schema, TradeMixin):
    """ Wrapped in <TradeTransfers> """
    # Oddly, TradeTransfer uses YYYYMMDD format for origTradeDate
    # instead of ISO format like Trade
    origTradeDate = Date()
    brokerName = String()
    brokerAccount = String()
    awayBrokerCommission = Decimal()
    regulatoryFee = Decimal()
    direction = OneOf("To", "From")
    deliveredReceived = OneOf("Delivered", "Received")
    netTradeMoney = Decimal()
    netTradeMoneyInBase = Decimal()
    netTradePrice = Decimal()


class CashTransaction(Schema, AccountMixin, CurrencyMixin, SecurityMixin):
    """ Wrapped in <CashTransactions> """
    # Despite the name, dateTime actually contains only the date.
    dateTime = Date()
    amount = Decimal()
    type = OneOf("Deposits/Withdrawals", "Broker Interest Paid",
                 "Broker Interest Received", "Withholding Tax",
                 "Bond Interest Received", "Bond Interest Paid", "Other Fees",
                 "Dividends", "Payment In Lieu Of Dividends")
    tradeID = String()
    code = List()
    transactionID = String()
    reportDate = Date()
    clientReference = String()


class InterestAccrualsCurrency(Schema, AccountMixin):
    """ Wrapped in <InterestAccruals> """
    currency = OneOf(*CURRENCY_CODES)
    fromDate = Date()
    toDate = Date()
    startingAccrualBalance = Decimal()
    interestAccrued = Decimal()
    accrualReversal = Decimal()
    fxTranslation = Decimal()
    endingAccrualBalance = Decimal()


class SLBActivity(Schema, AccountMixin, CurrencyMixin, SecurityMixin):
    """ Wrapped in <SLBActivities> """
    date = Date()
    slbTransactionId = String()
    activityDescription = String()
    type = OneOf("DirectBorrow", "DirectLoan", "ManagedLoan")
    exchange = String()
    quantity = Decimal()
    feeRate = Decimal()
    collateralAmount = Decimal()
    markQuantity = Decimal()
    markPriorPrice = Decimal()
    markCurrentPrice = Decimal()


class Transfer(Schema, AccountMixin, CurrencyMixin, SecurityMixin):
    """ Wrapped in <Transfers> """
    date = Date()
    type = OneOf("INTERNAL", "ACATS")
    direction = OneOf("IN", "OUT")
    company = String()
    account = String()
    accountName = String()
    quantity = Decimal()
    transferPrice = Decimal()
    positionAmount = Decimal()
    positionAmountInBase = Decimal()
    pnlAmount = Decimal()
    pnlAmountInBase = Decimal()
    fxPnl = Decimal()
    cashTransfer = Decimal()
    code = List()
    clientReference = String()


class CorporateAction(Schema, AccountMixin, CurrencyMixin, SecurityMixin):
    """ Wrapped in <CorporateActions> """
    reportDate = Date()
    dateTime = DateTime()
    amount = Decimal()
    proceeds = Decimal()
    value = Decimal()
    quantity = Decimal()
    fifoPnlRealized = Decimal()
    mtmPnl = Decimal()
    code = List()
    type = OneOf(
        "BC", "BM", "CA", "CC", "CD", "CH", "CI", "CO", "CP", "CS", "CT",
        "DI", "DW", "ED", "FA", "FI", "FS", "GV", "HD", "HI", "IC", "OR",
        "PI", "PV", "RI", "RS", "SD", "SO", "SR", "TC", "TI", "TO")


class ChangeInDividendAccrual(Schema, DividendAccrualMixin):
    """ Wrapped in <ChangeInDividendAccruals> """
    date = Date()


class OpenDividendAccrual(Schema, DividendAccrualMixin):
    """ Wrapped in <OpenDividendAccruals> """
    pass


class SecurityInfo(Schema, SecurityMixin):
    """ Wrapped in <SecuritiesInfo> """
    maturity = String()
    issueDate = Date()
    code = List()
    type = String()


class ConversionRate(Schema):
    """ Wrapped in <ConversionRates> """
    reportDate = Date()
    fromCurrency = OneOf(*CURRENCY_CODES)
    toCurrency = OneOf(*CURRENCY_CODES)
    rate = Decimal()


class PriorPeriodPosition(Schema, AccountMixin, CurrencyMixin, SecurityMixin):
    """ Wrapped in <PriorPeriodPositions> """
    priorMtmPnl = Decimal()
    date = Date()
    price = Decimal()


class MTMPerformanceSummaryUnderlying(Schema, AccountMixin, SecurityMixin):
    """ Wrapped in <MTMPerformanceSummaryInBase> """
    listingExchange = String()
    underlyingSecurityID = String()
    underlyingListingExchange = String()
    reportDate = Date()
    prevCloseQuantity = Decimal()
    prevClosePrice = Decimal()
    closeQuantity = Decimal()
    closePrice = Decimal()
    transactionMtm = Decimal()
    priorOpenMtm = Decimal()
    commissions = Decimal()
    other = Decimal()
    total = Decimal()
    code = List()

    
class ChangeInNAV(Schema, AccountMixin):
    """ Wrapped in <FlexStatement> """
    fromDate = Date()
    toDate = Date()
    startingValue = Decimal()
    mtm = Decimal()
    realized = Decimal()
    changeInUnrealized = Decimal()
    costAdjustments = Decimal()
    transferredPnlAdjustments = Decimal()
    depositsWithdrawals = Decimal()
    internalCashTransfers = Decimal()
    assetTransfers = Decimal()
    debitCardActivity = Decimal()
    billPay = Decimal()
    dividends = Decimal()
    withholdingTax = Decimal()
    withholding871m = Decimal()
    withholdingTaxCollected = Decimal()
    changeInDividendAccruals = Decimal()
    interest = Decimal()
    changeInInterestAccruals = Decimal()
    advisorFees = Decimal()
    clientFees = Decimal()
    otherFees = Decimal()
    feesReceivables = Decimal()
    commissions = Decimal()
    commissionReceivables = Decimal()
    forexCommissions = Decimal()
    transactionTax = Decimal()
    taxReceivables = Decimal()
    salesTax = Decimal()
    softDollars = Decimal()
    netFxTrading = Decimal()
    fxTranslation = Decimal()
    linkingAdjustments = Decimal()
    other = Decimal()
    endingValue = Decimal()
    twr = Decimal()
    corporateActionProceeds = Decimal()
    
    
# Map of list container tag to element schema
elementSchemata = {
    "EquitySummaryInBase": EquitySummaryByReportDateInBase,
    "CashReport": CashReportCurrency,
    "StmtFunds": StatementOfFundsLine,
    "FdicInsuredDepositsByBank": None,
    "ChangeInPositionValues": ChangeInPositionValue,
    "OpenPositions": OpenPosition,
    "ComplexPositions": None,
    "FxLots": FxLot,
    "Trades": Trade,
    "TradeConfirms": TradeConfirmation,
    "TransactionTaxes": None,
    "OptionEAE": OptionEAE,
    "TradeTransfers": TradeTransfer,
    "RoutingCommissions": None,
    "IBGNoteTransactions": None,
    "CashTransactions": CashTransaction,
    "CFDCharges": None,
    "InterestAccruals": InterestAccrualsCurrency,
    "SLBOpenContracts": None,
    "SLBActivities": SLBActivity,
    "Transfers": Transfer,
    "CorporateActions": CorporateAction,
    "ClientFees": None,
    "SoftDollars": None,
    "ChangeInDividendAccruals": ChangeInDividendAccrual,
    "OpenDividendAccruals": OpenDividendAccrual,
    "SecuritiesInfo": SecurityInfo,
    "ConversionRates": ConversionRate,
    "PriorPeriodPositions": PriorPeriodPosition,
    "MTMPerformanceSummaryInBase": MTMPerformanceSummaryUnderlying,
    "ChangeInNAV": ChangeInNAV
}
