# coding: utf-8
"""
"""


import datetime
import decimal
import enum
from dataclasses import dataclass
from typing import List, Optional, Union


###############################################################################
#  ENUMS
###############################################################################
@enum.unique
class CashTransactionType(enum.Enum):
    DEPOSITWITHDRAW = "Deposits/Withdrawals"
    BROKERINTPAID = "Broker Interest Paid"
    BROKERINTRCVD = "Broker Interest Received"
    WHTAX = "Withholding Tax"
    BONDINTRCVD = "Bond Interest Received"
    BONDINTPAID = "Bond Interest Paid"
    FEES = "Other Fees"
    DIVIDEND = "Dividends"
    PAYMENTINLIEU = "Payment In Lieu Of Dividends"


@enum.unique
class TradeType(enum.Enum):
    EXCHTRADE = "ExchTrade"
    TRADECANCEL = "TradeCancel"
    FRACSHARE = "FracShare"
    FRACSHARECANCEL = "FracShareCancel"
    TRADECORRECT = "TradeCorrect"
    BOOKTRADE = "BookTrade"
    DVPTRADE = "DvpTrade"


@enum.unique
class BuySell(enum.Enum):
    BUY = "BUY"
    CANCELBUY = "BUY (Ca.)"
    SELL = "SELL"
    CANCELSELL = "SELL (Ca.)"


@enum.unique
class OpenClose(enum.Enum):
    OPEN = "O"
    CLOSE = "C"
    OPENCLOSE = "C;O"


@enum.unique
class OrderType(enum.Enum):
    LIMIT = "LMT"
    MARKET = "MKT"
    MARKETONCLOSE = "MOC"


@enum.unique
class CorporateActionType(enum.Enum):
    BONDCONVERSION = "BC"
    BONDMATURITY = "BM"
    CONTRACTSOULTE = "CA"
    CONTRACTCONSOLIDATION = "CC"
    CASHDIV = "CD"
    CHOICEDIV = "CH"
    CONVERTIBLEISSUE = "CI"
    CONTRACTSPINOFF = "CO"
    COUPONPAYMENT = "CP"
    CONTRACTSPLIT = "CS"
    CFDTERMINATION = "CT"
    DIVRIGHTSISSUE = "DI"
    DELISTWORTHLESS = "DW"
    EXPIREDIVRIGHT = "ED"
    FEEALLOCATION = "FA"
    FORWARDSPLITISSUE = "FI"
    FORWARDSPLIT = "FS"
    GENERICVOLUNTARY = "GV"
    CHOICEDIVDELIVERY = "HD"
    CHOICEDIVISSUE = "HI"
    ISSUECHANGE = "IC"
    ASSETPURCHASE = "OR"
    PURCHASEISSUE = "PI"
    PROXYVOTE = "PV"
    RIGHTSISSUE = "RI"
    REVERSESPLIT = "RS"
    STOCKDIV = "SD"
    SPINOFF = "SO"
    SUBSCRIBERIGHTS = "SR"
    MERGER = "TC"
    TENDERISSUE = "TI"
    TENDER = "TO"


@enum.unique
class OptionEAEType(enum.Enum):
    ASSIGNMENT = "Assignment"
    EXERCISE = "Exercise"
    EXPIRATION = "Expiration"
    SELL = "Sell"


@enum.unique
class PositionSide(enum.Enum):
    LONG = "Long"
    SHORT = "Short"


@enum.unique
class TradeTransferDirection(enum.Enum):
    TO = "To"
    FROM = "From"


@enum.unique
class TransferType(enum.Enum):
    INTERNAL = "INTERNAL"
    ACATS = "ACATS"


@enum.unique
class TransferDirection(enum.Enum):
    IN = "IN"
    OUT = "OUT"


@enum.unique
class DeliveredReceived(enum.Enum):
    DELIVERED = "Delivered"
    RECEIVED = "Received"


###############################################################################
#  TYPE ALIASES
###############################################################################
OptionalDecimal = Optional[decimal.Decimal]


FlexElement = Union[
    "FlexQueryResponse", "FlexStatement", "AccountInformation", "ChangeInNAV",
    "MTMPerformanceSummaryUnderlying", "EquitySummaryByReportDateInBase",
    "CashReportCurrency", "StatementOfFundsLine", "ChangeInPositionValue",
    "OpenPosition", "FxLot", "Trade", "TradeConfirmation", "OptionEAE",
    "TradeTransfer", "InterestAccrualsCurrency", "SLBActivity", "Transfer",
    "CorporateAction", "CashTransaction", "ChangeInDividendAccrual",
    "OpenDividendAccrual", "SecurityInfo", "ConversionRate",
    "PriorPeriodPosition",
]


###############################################################################
#  MIXINS
###############################################################################
@dataclass(frozen=True)
class AccountMixin:
    accountId: str
    acctAlias: str
    model: str


@dataclass(frozen=True)
class CurrencyMixin:
    currency: str
    fxRateToBase: decimal.Decimal


@dataclass(frozen=True)
class SecurityMixin:
    assetCategory: str
    symbol: str
    description: str
    conid: str
    securityID: str
    securityIDType: str
    cusip: str
    isin: str
    underlyingConid: str
    underlyingSymbol: str
    issuer: str
    multiplier: decimal.Decimal
    strike: decimal.Decimal
    expiry: datetime.date
    putCall: str
    principalAdjustFactor: decimal.Decimal


@dataclass(frozen=True)
class TradeMixin(AccountMixin, CurrencyMixin, SecurityMixin):
    tradeID: str
    reportDate: datetime.date
    tradeDate: datetime.date
    tradeTime: datetime.time
    settleDateTarget: datetime.date
    transactionType: TradeType
    exchange: str
    quantity: decimal.Decimal
    tradePrice: decimal.Decimal
    tradeMoney: decimal.Decimal
    proceeds: decimal.Decimal
    taxes: decimal.Decimal
    ibCommission: decimal.Decimal
    ibCommissionCurrency: str
    netCash: decimal.Decimal
    closePrice: decimal.Decimal
    openCloseIndicator: OpenClose
    notes: List[str]  # separator = ";"
    cost: decimal.Decimal
    fifoPnlRealized: decimal.Decimal
    fxPnl: decimal.Decimal
    mtmPnl: decimal.Decimal
    origTradePrice: decimal.Decimal
    origTradeDate: datetime.date
    origTradeID: str
    origOrderID: str
    clearingFirmID: str
    transactionID: str
    openDateTime: datetime.datetime
    holdingPeriodDateTime: datetime.datetime
    whenRealized: datetime.datetime
    whenReopened: datetime.datetime
    levelOfDetail: str


@dataclass(frozen=True)
class DividendAccrualMixin(AccountMixin, CurrencyMixin, SecurityMixin):
    exDate: datetime.date
    payDate: datetime.date
    quantity: decimal.Decimal
    tax: decimal.Decimal
    fee: decimal.Decimal
    grossRate: decimal.Decimal
    grossAmount: decimal.Decimal
    netAmount: decimal.Decimal
    code: List[str]
    fromAcct: str
    toAcct: str


###############################################################################
#  ELEMENTS
###############################################################################
@dataclass(frozen=True)
class FlexQueryResponse:
    """ Top-level element """
    queryName: str
    type: str
    FlexStatements: List["FlexStatement"]


@dataclass(frozen=True)
class FlexStatement:
    """ Wrapped in <FlexStatements> """
    accountId: str
    fromDate: datetime.date
    toDate: datetime.date
    period: str
    whenGenerated: datetime.datetime
    AccountInformation: "_AccountInformation"
    #  NAVSummaryInBase - FIXME
    ChangeInNAV: Optional["_ChangeInNAV"] = None
    MTMPerformanceSummaryInBase: Optional[
        List["MTMPerformanceSummaryUnderlying"]
    ] = None
    #  Realized & Unrealized Performance Summary in Base - FIXME
    #  Month & Year to Date Performance Summary in Base - FIXME
    EquitySummaryInBase: Optional[
        List["EquitySummaryByReportDateInBase"]
    ] = None
    CashReport: Optional[List["CashReportCurrency"]] = None
    #  Debit Card Activity - FIXME
    FdicInsuredDepositsByBank: Optional[List] = None  # FIXME
    StmtFunds: Optional[List["StatementOfFundsLine"]] = None
    ChangeInPositionValues: Optional[List["ChangeInPositionValue"]] = None
    OpenPositions: Optional[List["OpenPosition"]] = None
    ComplexPositions: Optional[List] = None  # FIXME
    #  Net Stock Position Summary - FIXME
    FxPositions: Optional[List["FxLot"]] = None  # N.B. FXLot wrapped in FxLots
    Trades: Optional[List["Trade"]] = None
    TradeConfirms: Optional[List["TradeConfirmation"]] = None
    TransactionTaxes: Optional[List] = None  # FIXME
    OptionEAE: Optional[List["_OptionEAE"]] = None
    #  Pending Exercises - FIXME
    TradeTransfers: Optional[List["TradeTransfer"]] = None
    #  Forex P/L Details - FIXME
    UnbookedTrades: Optional[List] = None  # FIXME
    RoutingCommissions: Optional[List] = None  # FIXME
    IBGNoteTransactions: Optional[List] = None  # FIXME
    UnsettledTransfers: Optional[List] = None  # FIXME
    UnbundledCommissionDetails: Optional[List] = None  # FIXME
    PriorPeriodPositions: Optional[List["PriorPeriodPosition"]] = None
    #  Soft Dollar Activity - FIXME
    CorporateActions: Optional[List["CorporateAction"]] = None
    ClientFees: Optional[List] = None  # FIXME
    #  Client Fee Expense Details - FIXME
    SoftDollars: Optional[List] = None  # FIXME
    CashTransactions: Optional[List["CashTransaction"]] = None
    CFDCharges: Optional[List] = None  # FIXME
    InterestAccruals: Optional[List["InterestAccrualsCurrency"]] = None
    SLBOpenContracts: Optional[List] = None  # FIXME
    SLBActivities: Optional[List["SLBActivity"]] = None
    Transfers: Optional[List["Transfer"]] = None
    ChangeInDividendAccruals: Optional[List["_ChangeInDividendAccrual"]] = None
    OpenDividendAccruals: Optional[List["OpenDividendAccrual"]] = None
    SecuritiesInfo: Optional[List["SecurityInfo"]] = None
    ConversionRates: Optional[List["ConversionRate"]] = None


@dataclass(frozen=True)
class AccountInformation:
    """ Wrapped in <FlexStatement> """
    accountId: str
    acctAlias: str
    currency: str
    name: str
    accountType: str
    customerType: str
    accountCapabilities: List[str]
    tradingPermissions: List[str]
    dateOpened: datetime.date
    dateFunded: datetime.date
    dateClosed: datetime.date
    masterName: str
    ibEntity: str


#  Type alias to work around https://github.com/python/mypy/issues/1775
_AccountInformation = AccountInformation


@dataclass(frozen=True)
class ChangeInNAV(AccountMixin):
    """ Wrapped in <FlexStatement> """
    fromDate: datetime.date
    toDate: datetime.date
    startingValue: OptionalDecimal = None
    mtm: OptionalDecimal = None
    realized: OptionalDecimal = None
    changeInUnrealized: OptionalDecimal = None
    costAdjustments: OptionalDecimal = None
    transferredPnlAdjustments: OptionalDecimal = None
    depositsWithdrawals: OptionalDecimal = None
    internalCashTransfers: OptionalDecimal = None
    assetTransfers: OptionalDecimal = None
    debitCardActivity: OptionalDecimal = None
    billPay: OptionalDecimal = None
    dividends: OptionalDecimal = None
    withholdingTax: OptionalDecimal = None
    withholding871m: OptionalDecimal = None
    withholdingTaxCollected: OptionalDecimal = None
    changeInDividendAccruals: OptionalDecimal = None
    interest: OptionalDecimal = None
    changeInInterestAccruals: OptionalDecimal = None
    advisorFees: OptionalDecimal = None
    clientFees: OptionalDecimal = None
    otherFees: OptionalDecimal = None
    feesReceivables: OptionalDecimal = None
    commissions: OptionalDecimal = None
    commissionReceivables: OptionalDecimal = None
    forexCommissions: OptionalDecimal = None
    transactionTax: OptionalDecimal = None
    taxReceivables: OptionalDecimal = None
    salesTax: OptionalDecimal = None
    softDollars: OptionalDecimal = None
    netFxTrading: OptionalDecimal = None
    fxTranslation: OptionalDecimal = None
    linkingAdjustments: OptionalDecimal = None
    other: OptionalDecimal = None
    endingValue: OptionalDecimal = None
    twr: OptionalDecimal = None
    corporateActionProceeds: OptionalDecimal = None


#  Type alias to work around https://github.com/python/mypy/issues/1775
_ChangeInNAV = ChangeInNAV


@dataclass(frozen=True)
class MTMPerformanceSummaryUnderlying(AccountMixin, SecurityMixin):
    """ Wrapped in <MTMPerformanceSummaryInBase> """
    listingExchange: str
    underlyingSecurityID: str
    underlyingListingExchange: str
    reportDate: datetime.date
    prevCloseQuantity: OptionalDecimal = None
    prevClosePrice: OptionalDecimal = None
    closeQuantity: OptionalDecimal = None
    closePrice: OptionalDecimal = None
    transactionMtm: OptionalDecimal = None
    priorOpenMtm: OptionalDecimal = None
    commissions: OptionalDecimal = None
    other: OptionalDecimal = None
    total: OptionalDecimal = None
    code: Optional[List[str]] = None


@dataclass(frozen=True)
class EquitySummaryByReportDateInBase(AccountMixin):
    """ Wrapped in <EquitySummaryInBase> """
    reportDate: datetime.date
    cash: OptionalDecimal = None
    cashLong: OptionalDecimal = None
    cashShort: OptionalDecimal = None
    slbCashCollateral: OptionalDecimal = None
    slbCashCollateralLong: OptionalDecimal = None
    slbCashCollateralShort: OptionalDecimal = None
    stock: OptionalDecimal = None
    stockLong: OptionalDecimal = None
    stockShort: OptionalDecimal = None
    slbDirectSecuritiesBorrowed: OptionalDecimal = None
    slbDirectSecuritiesBorrowedLong: OptionalDecimal = None
    slbDirectSecuritiesBorrowedShort: OptionalDecimal = None
    slbDirectSecuritiesLent: OptionalDecimal = None
    slbDirectSecuritiesLentLong: OptionalDecimal = None
    slbDirectSecuritiesLentShort: OptionalDecimal = None
    options: OptionalDecimal = None
    optionsLong: OptionalDecimal = None
    optionsShort: OptionalDecimal = None
    commodities: OptionalDecimal = None
    commoditiesLong: OptionalDecimal = None
    commoditiesShort: OptionalDecimal = None
    bonds: OptionalDecimal = None
    bondsLong: OptionalDecimal = None
    bondsShort: OptionalDecimal = None
    notes: OptionalDecimal = None
    notesLong: OptionalDecimal = None
    notesShort: OptionalDecimal = None
    funds: OptionalDecimal = None
    fundsLong: OptionalDecimal = None
    fundsShort: OptionalDecimal = None
    interestAccruals: OptionalDecimal = None
    interestAccrualsLong: OptionalDecimal = None
    interestAccrualsShort: OptionalDecimal = None
    softDollars: OptionalDecimal = None
    softDollarsLong: OptionalDecimal = None
    softDollarsShort: OptionalDecimal = None
    forexCfdUnrealizedPl: OptionalDecimal = None
    forexCfdUnrealizedPlLong: OptionalDecimal = None
    forexCfdUnrealizedPlShort: OptionalDecimal = None
    dividendAccruals: OptionalDecimal = None
    dividendAccrualsLong: OptionalDecimal = None
    dividendAccrualsShort: OptionalDecimal = None
    fdicInsuredBankSweepAccount: OptionalDecimal = None
    fdicInsuredBankSweepAccountLong: OptionalDecimal = None
    fdicInsuredBankSweepAccountShort: OptionalDecimal = None
    fdicInsuredBankSweepAccountCashComponent: OptionalDecimal = None
    fdicInsuredBankSweepAccountCashComponentLong: OptionalDecimal = None
    fdicInsuredBankSweepAccountCashComponentShort: OptionalDecimal = None
    fdicInsuredAccountInterestAccruals: OptionalDecimal = None
    fdicInsuredAccountInterestAccrualsLong: OptionalDecimal = None
    fdicInsuredAccountInterestAccrualsShort: OptionalDecimal = None
    fdicInsuredAccountInterestAccrualsComponent: OptionalDecimal = None
    fdicInsuredAccountInterestAccrualsComponentLong: OptionalDecimal = None
    fdicInsuredAccountInterestAccrualsComponentShort: OptionalDecimal = None
    total: OptionalDecimal = None
    totalLong: OptionalDecimal = None
    totalShort: OptionalDecimal = None
    brokerInterestAccrualsComponent: OptionalDecimal = None
    brokerCashComponent: OptionalDecimal = None
    cfdUnrealizedPl: OptionalDecimal = None


@dataclass(frozen=True)
class CashReportCurrency(AccountMixin):
    """ Wrapped in <CashReport> """
    currency: str
    fromDate: datetime.date
    toDate: datetime.date
    startingCash: OptionalDecimal = None
    startingCashSec: OptionalDecimal = None
    startingCashCom: OptionalDecimal = None
    clientFees: OptionalDecimal = None
    clientFeesSec: OptionalDecimal = None
    clientFeesCom: OptionalDecimal = None
    clientFeesMTD: OptionalDecimal = None
    clientFeesYTD: OptionalDecimal = None
    commissions: OptionalDecimal = None
    commissionsSec: OptionalDecimal = None
    commissionsCom: OptionalDecimal = None
    commissionsMTD: OptionalDecimal = None
    commissionsYTD: OptionalDecimal = None
    billableCommissions: OptionalDecimal = None
    billableCommissionsSec: OptionalDecimal = None
    billableCommissionsCom: OptionalDecimal = None
    billableCommissionsMTD: OptionalDecimal = None
    billableCommissionsYTD: OptionalDecimal = None
    depositWithdrawals: OptionalDecimal = None
    depositWithdrawalsSec: OptionalDecimal = None
    depositWithdrawalsCom: OptionalDecimal = None
    depositWithdrawalsMTD: OptionalDecimal = None
    depositWithdrawalsYTD: OptionalDecimal = None
    deposits: OptionalDecimal = None
    depositsSec: OptionalDecimal = None
    depositsCom: OptionalDecimal = None
    depositsMTD: OptionalDecimal = None
    depositsYTD: OptionalDecimal = None
    withdrawals: OptionalDecimal = None
    withdrawalsSec: OptionalDecimal = None
    withdrawalsCom: OptionalDecimal = None
    withdrawalsMTD: OptionalDecimal = None
    withdrawalsYTD: OptionalDecimal = None
    accountTransfers: OptionalDecimal = None
    accountTransfersSec: OptionalDecimal = None
    accountTransfersCom: OptionalDecimal = None
    accountTransfersMTD: OptionalDecimal = None
    accountTransfersYTD: OptionalDecimal = None
    linkingAdjustments: OptionalDecimal = None
    linkingAdjustmentsSec: OptionalDecimal = None
    linkingAdjustmentsCom: OptionalDecimal = None
    internalTransfers: OptionalDecimal = None
    internalTransfersSec: OptionalDecimal = None
    internalTransfersCom: OptionalDecimal = None
    internalTransfersMTD: OptionalDecimal = None
    internalTransfersYTD: OptionalDecimal = None
    dividends: OptionalDecimal = None
    dividendsSec: OptionalDecimal = None
    dividendsCom: OptionalDecimal = None
    dividendsMTD: OptionalDecimal = None
    dividendsYTD: OptionalDecimal = None
    insuredDepositInterest: OptionalDecimal = None
    insuredDepositInterestSec: OptionalDecimal = None
    insuredDepositInterestCom: OptionalDecimal = None
    insuredDepositInterestMTD: OptionalDecimal = None
    insuredDepositInterestYTD: OptionalDecimal = None
    brokerInterest: OptionalDecimal = None
    brokerInterestSec: OptionalDecimal = None
    brokerInterestCom: OptionalDecimal = None
    brokerInterestMTD: OptionalDecimal = None
    brokerInterestYTD: OptionalDecimal = None
    bondInterest: OptionalDecimal = None
    bondInterestSec: OptionalDecimal = None
    bondInterestCom: OptionalDecimal = None
    bondInterestMTD: OptionalDecimal = None
    bondInterestYTD: OptionalDecimal = None
    cashSettlingMtm: OptionalDecimal = None
    cashSettlingMtmSec: OptionalDecimal = None
    cashSettlingMtmCom: OptionalDecimal = None
    cashSettlingMtmMTD: OptionalDecimal = None
    cashSettlingMtmYTD: OptionalDecimal = None
    realizedVm: OptionalDecimal = None
    realizedVmSec: OptionalDecimal = None
    realizedVmCom: OptionalDecimal = None
    realizedVmMTD: OptionalDecimal = None
    realizedVmYTD: OptionalDecimal = None
    cfdCharges: OptionalDecimal = None
    cfdChargesSec: OptionalDecimal = None
    cfdChargesCom: OptionalDecimal = None
    cfdChargesMTD: OptionalDecimal = None
    cfdChargesYTD: OptionalDecimal = None
    netTradesSales: OptionalDecimal = None
    netTradesSalesSec: OptionalDecimal = None
    netTradesSalesCom: OptionalDecimal = None
    netTradesSalesMTD: OptionalDecimal = None
    netTradesSalesYTD: OptionalDecimal = None
    netTradesPurchases: OptionalDecimal = None
    netTradesPurchasesSec: OptionalDecimal = None
    netTradesPurchasesCom: OptionalDecimal = None
    netTradesPurchasesMTD: OptionalDecimal = None
    netTradesPurchasesYTD: OptionalDecimal = None
    advisorFees: OptionalDecimal = None
    advisorFeesSec: OptionalDecimal = None
    advisorFeesCom: OptionalDecimal = None
    advisorFeesMTD: OptionalDecimal = None
    advisorFeesYTD: OptionalDecimal = None
    feesReceivables: OptionalDecimal = None
    feesReceivablesSec: OptionalDecimal = None
    feesReceivablesCom: OptionalDecimal = None
    feesReceivablesMTD: OptionalDecimal = None
    feesReceivablesYTD: OptionalDecimal = None
    paymentInLieu: OptionalDecimal = None
    paymentInLieuSec: OptionalDecimal = None
    paymentInLieuCom: OptionalDecimal = None
    paymentInLieuMTD: OptionalDecimal = None
    paymentInLieuYTD: OptionalDecimal = None
    transactionTax: OptionalDecimal = None
    transactionTaxSec: OptionalDecimal = None
    transactionTaxCom: OptionalDecimal = None
    transactionTaxMTD: OptionalDecimal = None
    transactionTaxYTD: OptionalDecimal = None
    taxReceivables: OptionalDecimal = None
    taxReceivablesSec: OptionalDecimal = None
    taxReceivablesCom: OptionalDecimal = None
    taxReceivablesMTD: OptionalDecimal = None
    taxReceivablesYTD: OptionalDecimal = None
    withholdingTax: OptionalDecimal = None
    withholdingTaxSec: OptionalDecimal = None
    withholdingTaxCom: OptionalDecimal = None
    withholdingTaxMTD: OptionalDecimal = None
    withholdingTaxYTD: OptionalDecimal = None
    withholding871m: OptionalDecimal = None
    withholding871mSec: OptionalDecimal = None
    withholding871mCom: OptionalDecimal = None
    withholding871mMTD: OptionalDecimal = None
    withholding871mYTD: OptionalDecimal = None
    withholdingCollectedTax: OptionalDecimal = None
    withholdingCollectedTaxSec: OptionalDecimal = None
    withholdingCollectedTaxCom: OptionalDecimal = None
    withholdingCollectedTaxMTD: OptionalDecimal = None
    withholdingCollectedTaxYTD: OptionalDecimal = None
    salesTax: OptionalDecimal = None
    salesTaxSec: OptionalDecimal = None
    salesTaxCom: OptionalDecimal = None
    salesTaxMTD: OptionalDecimal = None
    salesTaxYTD: OptionalDecimal = None
    fxTranslationGainLoss: OptionalDecimal = None
    fxTranslationGainLossSec: OptionalDecimal = None
    fxTranslationGainLossCom: OptionalDecimal = None
    otherFees: OptionalDecimal = None
    otherFeesSec: OptionalDecimal = None
    otherFeesCom: OptionalDecimal = None
    otherFeesMTD: OptionalDecimal = None
    otherFeesYTD: OptionalDecimal = None
    other: OptionalDecimal = None
    otherSec: OptionalDecimal = None
    otherCom: OptionalDecimal = None
    endingCash: OptionalDecimal = None
    endingCashSec: OptionalDecimal = None
    endingCashCom: OptionalDecimal = None
    endingSettledCash: OptionalDecimal = None
    endingSettledCashSec: OptionalDecimal = None
    endingSettledCashCom: OptionalDecimal = None


@dataclass(frozen=True)
class StatementOfFundsLine(AccountMixin, SecurityMixin):
    """ Wrapped in <StmtFunds> """
    currency: str
    reportDate: datetime.date
    date: datetime.date
    activityDescription: str
    tradeID: str
    debit: decimal.Decimal
    credit: decimal.Decimal
    amount: decimal.Decimal
    balance: decimal.Decimal
    buySell: str


@dataclass(frozen=True)
class ChangeInPositionValue(AccountMixin):
    """ Wrapped in <ChangeInPositionValues> """
    currency: str
    assetCategory: str
    priorPeriodValue: decimal.Decimal
    transactions: decimal.Decimal
    mtmPriorPeriodPositions: decimal.Decimal
    mtmTransactions: decimal.Decimal
    corporateActions: decimal.Decimal
    other: decimal.Decimal
    accountTransfers: decimal.Decimal
    linkingAdjustments: decimal.Decimal
    fxTranslationPnl: decimal.Decimal
    futurePriceAdjustments: decimal.Decimal
    settledCash: decimal.Decimal
    endOfPeriodValue: decimal.Decimal


@dataclass(frozen=True)
class OpenPosition(AccountMixin, CurrencyMixin, SecurityMixin):
    """ Wrapped in <OpenPositions> """
    reportDate: datetime.date
    position: decimal.Decimal
    markPrice: decimal.Decimal
    positionValue: decimal.Decimal
    openPrice: decimal.Decimal
    costBasisPrice: decimal.Decimal
    costBasisMoney: decimal.Decimal
    percentOfNAV: decimal.Decimal
    fifoPnlUnrealized: decimal.Decimal
    side: str
    levelOfDetail: str
    openDateTime: datetime.datetime
    holdingPeriodDateTime: datetime.datetime
    code: List[str]
    originatingOrderID: str
    originatingTransactionID: str
    accruedInt: str


@dataclass(frozen=True)
class FxLot(AccountMixin):
    """ Wrapped in <FxLots> """
    assetCategory: str
    reportDate: datetime.date
    functionalCurrency: str
    fxCurrency: str
    quantity: decimal.Decimal
    costPrice: decimal.Decimal
    costBasis: decimal.Decimal
    closePrice: decimal.Decimal
    value: decimal.Decimal
    unrealizedPL: decimal.Decimal
    code: List[str]
    lotDescription: str
    lotOpenDateTime: datetime.datetime
    levelOfDetail: str


@dataclass(frozen=True)
class Trade(TradeMixin):
    """ Wrapped in <Trades> """
    buySell: BuySell
    ibOrderID: str
    ibExecID: str
    brokerageOrderID: str
    orderReference: str
    volatilityOrderLink: str
    exchOrderId: str
    extExecID: str
    # Despite the name, `orderTime` actually contains date/time data.
    orderTime: datetime.datetime
    changeInPrice: decimal.Decimal
    changeInQuantity: decimal.Decimal
    orderType: OrderType
    traderID: str
    isAPIOrder: bool


@dataclass(frozen=True)
class TradeConfirmation(TradeMixin):
    """ Wrapped in <TradeConfirms> """
    buySell: BuySell
    commissionCurrency: str
    price: decimal.Decimal
    thirdPartyClearingCommission: decimal.Decimal
    orderID: decimal.Decimal
    allocatedTo: str
    thirdPartyRegulatoryCommission: decimal.Decimal
    dateTime: datetime.datetime
    brokerExecutionCommission: decimal.Decimal
    thirdPartyExecutionCommission: decimal.Decimal
    amount: decimal.Decimal
    otherCommission: decimal.Decimal
    commission: decimal.Decimal
    brokerClearingCommission: decimal.Decimal
    ibOrderID: str
    ibExecID: str
    execID: str
    brokerageOrderID: str
    orderReference: str
    volatilityOrderLink: str
    exchOrderId: str
    extExecID: str
    # Despite the name, `orderTime` actually contains date/time data.
    orderTime: datetime.datetime
    changeInPrice: decimal.Decimal
    changeInQuantity: decimal.Decimal
    orderType: OrderType
    traderID: str
    isAPIOrder: bool
    code: List[str]
    tax: decimal.Decimal
    listingExchange: str
    underlyingListingExchange: str
    settleDate: str
    underlyingSecurityID: str


@dataclass(frozen=True)
class OptionEAE(AccountMixin, CurrencyMixin, SecurityMixin):
    """Option Exercise Assignment or Expiration

    Wrapped in (identically-named) <OptionEAE>
    """
    date: datetime.date
    transactionType: OptionEAEType
    quantity: decimal.Decimal
    tradePrice: decimal.Decimal
    markPrice: decimal.Decimal
    proceeds: decimal.Decimal
    commisionsAndTax: decimal.Decimal
    costBasis: decimal.Decimal
    realizedPnl: decimal.Decimal
    fxPnl: decimal.Decimal
    mtmPnl: decimal.Decimal
    tradeID: str


#  Type alias to work around https://github.com/python/mypy/issues/1775
_OptionEAE = OptionEAE


@dataclass(frozen=True)
class TradeTransfer(TradeMixin):
    """ Wrapped in <TradeTransfers> """
    # Oddly, `origTradeDate` appears to have hard-coded YYYYMMDD format
    # instead of the date format from the report configuration.
    origTradeDate: datetime.date
    brokerName: str
    brokerAccount: str
    awayBrokerCommission: decimal.Decimal
    regulatoryFee: decimal.Decimal
    direction: TradeTransferDirection
    deliveredReceived: DeliveredReceived
    netTradeMoney: decimal.Decimal
    netTradeMoneyInBase: decimal.Decimal
    netTradePrice: decimal.Decimal


@dataclass(frozen=True)
class InterestAccrualsCurrency(AccountMixin):
    """ Wrapped in <InterestAccruals> """
    currency: str
    fromDate: datetime.date
    toDate: datetime.date
    startingAccrualBalance: decimal.Decimal
    interestAccrued: decimal.Decimal
    accrualReversal: decimal.Decimal
    fxTranslation: decimal.Decimal
    endingAccrualBalance: decimal.Decimal


@dataclass(frozen=True)
class SLBActivity(AccountMixin, CurrencyMixin, SecurityMixin):
    """ Wrapped in <SLBActivities> """
    date: datetime.date
    slbTransactionId: str
    activityDescription: str
    type: str
    exchange: str
    quantity: decimal.Decimal
    feeRate: decimal.Decimal
    collateralAmount: decimal.Decimal
    markQuantity: decimal.Decimal
    markPriorPrice: decimal.Decimal
    markCurrentPrice: decimal.Decimal


@dataclass(frozen=True)
class Transfer(AccountMixin, CurrencyMixin, SecurityMixin):
    """ Wrapped in <Transfers> """
    date: datetime.date
    type: TransferType
    direction: TransferDirection
    company: str
    account: str
    accountName: str
    quantity: decimal.Decimal
    transferPrice: decimal.Decimal
    positionAmount: decimal.Decimal
    positionAmountInBase: decimal.Decimal
    pnlAmount: decimal.Decimal
    pnlAmountInBase: decimal.Decimal
    fxPnl: decimal.Decimal
    cashTransfer: decimal.Decimal
    code: List[str]
    clientReference: str


@dataclass(frozen=True)
class CorporateAction(AccountMixin, CurrencyMixin, SecurityMixin):
    """ Wrapped in <CorporateActions> """
    reportDate: datetime.date
    dateTime: datetime.datetime
    amount: decimal.Decimal
    proceeds: decimal.Decimal
    value: decimal.Decimal
    quantity: decimal.Decimal
    fifoPnlRealized: decimal.Decimal
    mtmPnl: decimal.Decimal
    code: List[str]
    type: CorporateActionType


@dataclass(frozen=True)
class CashTransaction(AccountMixin, CurrencyMixin, SecurityMixin):
    """ Wrapped in <CashTransactions> """
    # Despite the name, `dateTime` actually contains only the date.
    dateTime: datetime.date
    amount: decimal.Decimal
    type: CashTransactionType
    tradeID: str
    code: List[str]
    transactionID: str
    reportDate: datetime.date
    clientReference: str


@dataclass(frozen=True)
class ChangeInDividendAccrual(DividendAccrualMixin):
    """ Wrapped in <ChangeInDividendAccruals> """
    date: datetime.date


#  Type alias to work around https://github.com/python/mypy/issues/1775
_ChangeInDividendAccrual = ChangeInDividendAccrual


@dataclass(frozen=True)
class OpenDividendAccrual(DividendAccrualMixin):
    """ Wrapped in <OpenDividendAccruals> """
    pass


@dataclass(frozen=True)
class SecurityInfo(SecurityMixin):
    """ Wrapped in <SecuritiesInfo> """
    maturity: str
    issueDate: datetime.date
    code: List[str]


@dataclass(frozen=True)
class ConversionRate:
    """ Wrapped in <ConversionRates> """
    reportDate: datetime.date
    fromCurrency: str
    toCurrency: str
    rate: decimal.Decimal


@dataclass(frozen=True)
class PriorPeriodPosition(AccountMixin, CurrencyMixin, SecurityMixin):
    """ Wrapped in <PriorPeriodPositions> """
    priorMtmPnl: decimal.Decimal
    date: datetime.date
    price: decimal.Decimal
