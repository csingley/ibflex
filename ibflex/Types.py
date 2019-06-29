# coding: utf-8
"""
"""

__all__ = [
    "CashTransactionType", "TradeType", "BuySell", "OpenClose", "OrderType",
    "CorporateActionType", "OptionEAEType", "PositionSide", "TransferType",
    "TradeTransferDirection", "TransferDirection", "DeliveredReceived",
    "FlexElement", "FlexQueryResponse", "FlexStatement", "AccountInformation",
    "ChangeInNAV", "MTMPerformanceSummaryUnderlying",
    "EquitySummaryByReportDateInBase", "CashReportCurrency",
    "StatementOfFundsLine", "ChangeInPositionValue", "OpenPosition", "FxLot",
    "Trade", "TradeConfirmation", "OptionEAE", "TradeTransfer",
    "InterestAccrualsCurrency", "SLBActivity", "Transfer", "CorporateAction",
    "CashTransaction", "ChangeInDividendAccrual", "OpenDividendAccrual",
    "SecurityInfo", "ConversionRate", "PriorPeriodPosition",
]

import datetime
import decimal
from decimal import Decimal
import enum
from dataclasses import dataclass
from typing import List, Optional


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
class FlexElement:
    """ Base class for data element types """


@dataclass(frozen=True)
class FlexQueryResponse(FlexElement):
    """ Root element """
    queryName: str
    type: str
    FlexStatements: List["FlexStatement"]


@dataclass(frozen=True)
class FlexStatement(FlexElement):
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
class AccountInformation(FlexElement):
    """ Child of <FlexStatement> """
    accountId: str
    acctAlias: str
    currency: str
    name: str
    accountType: str
    customerType: str
    accountCapabilities: List[str]
    tradingPermissions: List[str]
    dateOpened: datetime.date
    dateFunded: Optional[datetime.date]
    dateClosed: Optional[datetime.date]
    masterName: Optional[str]
    ibEntity: Optional[str]


#  Type alias to work around https://github.com/python/mypy/issues/1775
_AccountInformation = AccountInformation


@dataclass(frozen=True)
class ChangeInNAV(FlexElement, AccountMixin):
    """ Child of <FlexStatement> """
    fromDate: datetime.date
    toDate: datetime.date
    startingValue: Optional[Decimal] = None
    mtm: Optional[Decimal] = None
    realized: Optional[Decimal] = None
    changeInUnrealized: Optional[Decimal] = None
    costAdjustments: Optional[Decimal] = None
    transferredPnlAdjustments: Optional[Decimal] = None
    depositsWithdrawals: Optional[Decimal] = None
    internalCashTransfers: Optional[Decimal] = None
    assetTransfers: Optional[Decimal] = None
    debitCardActivity: Optional[Decimal] = None
    billPay: Optional[Decimal] = None
    dividends: Optional[Decimal] = None
    withholdingTax: Optional[Decimal] = None
    withholding871m: Optional[Decimal] = None
    withholdingTaxCollected: Optional[Decimal] = None
    changeInDividendAccruals: Optional[Decimal] = None
    interest: Optional[Decimal] = None
    changeInInterestAccruals: Optional[Decimal] = None
    advisorFees: Optional[Decimal] = None
    clientFees: Optional[Decimal] = None
    otherFees: Optional[Decimal] = None
    feesReceivables: Optional[Decimal] = None
    commissions: Optional[Decimal] = None
    commissionReceivables: Optional[Decimal] = None
    forexCommissions: Optional[Decimal] = None
    transactionTax: Optional[Decimal] = None
    taxReceivables: Optional[Decimal] = None
    salesTax: Optional[Decimal] = None
    softDollars: Optional[Decimal] = None
    netFxTrading: Optional[Decimal] = None
    fxTranslation: Optional[Decimal] = None
    linkingAdjustments: Optional[Decimal] = None
    other: Optional[Decimal] = None
    endingValue: Optional[Decimal] = None
    twr: Optional[Decimal] = None
    corporateActionProceeds: Optional[Decimal] = None


#  Type alias to work around https://github.com/python/mypy/issues/1775
_ChangeInNAV = ChangeInNAV


@dataclass(frozen=True)
class MTMPerformanceSummaryUnderlying(FlexElement, AccountMixin, SecurityMixin):
    """ Wrapped in <MTMPerformanceSummaryInBase> """
    listingExchange: str
    underlyingSecurityID: str
    underlyingListingExchange: str
    reportDate: datetime.date
    prevCloseQuantity: Optional[Decimal] = None
    prevClosePrice: Optional[Decimal] = None
    closeQuantity: Optional[Decimal] = None
    closePrice: Optional[Decimal] = None
    transactionMtm: Optional[Decimal] = None
    priorOpenMtm: Optional[Decimal] = None
    commissions: Optional[Decimal] = None
    other: Optional[Decimal] = None
    total: Optional[Decimal] = None
    code: Optional[List[str]] = None


@dataclass(frozen=True)
class EquitySummaryByReportDateInBase(FlexElement, AccountMixin):
    """ Wrapped in <EquitySummaryInBase> """
    reportDate: datetime.date
    cash: Optional[Decimal] = None
    cashLong: Optional[Decimal] = None
    cashShort: Optional[Decimal] = None
    slbCashCollateral: Optional[Decimal] = None
    slbCashCollateralLong: Optional[Decimal] = None
    slbCashCollateralShort: Optional[Decimal] = None
    stock: Optional[Decimal] = None
    stockLong: Optional[Decimal] = None
    stockShort: Optional[Decimal] = None
    slbDirectSecuritiesBorrowed: Optional[Decimal] = None
    slbDirectSecuritiesBorrowedLong: Optional[Decimal] = None
    slbDirectSecuritiesBorrowedShort: Optional[Decimal] = None
    slbDirectSecuritiesLent: Optional[Decimal] = None
    slbDirectSecuritiesLentLong: Optional[Decimal] = None
    slbDirectSecuritiesLentShort: Optional[Decimal] = None
    options: Optional[Decimal] = None
    optionsLong: Optional[Decimal] = None
    optionsShort: Optional[Decimal] = None
    commodities: Optional[Decimal] = None
    commoditiesLong: Optional[Decimal] = None
    commoditiesShort: Optional[Decimal] = None
    bonds: Optional[Decimal] = None
    bondsLong: Optional[Decimal] = None
    bondsShort: Optional[Decimal] = None
    notes: Optional[Decimal] = None
    notesLong: Optional[Decimal] = None
    notesShort: Optional[Decimal] = None
    funds: Optional[Decimal] = None
    fundsLong: Optional[Decimal] = None
    fundsShort: Optional[Decimal] = None
    interestAccruals: Optional[Decimal] = None
    interestAccrualsLong: Optional[Decimal] = None
    interestAccrualsShort: Optional[Decimal] = None
    softDollars: Optional[Decimal] = None
    softDollarsLong: Optional[Decimal] = None
    softDollarsShort: Optional[Decimal] = None
    forexCfdUnrealizedPl: Optional[Decimal] = None
    forexCfdUnrealizedPlLong: Optional[Decimal] = None
    forexCfdUnrealizedPlShort: Optional[Decimal] = None
    dividendAccruals: Optional[Decimal] = None
    dividendAccrualsLong: Optional[Decimal] = None
    dividendAccrualsShort: Optional[Decimal] = None
    fdicInsuredBankSweepAccount: Optional[Decimal] = None
    fdicInsuredBankSweepAccountLong: Optional[Decimal] = None
    fdicInsuredBankSweepAccountShort: Optional[Decimal] = None
    fdicInsuredBankSweepAccountCashComponent: Optional[Decimal] = None
    fdicInsuredBankSweepAccountCashComponentLong: Optional[Decimal] = None
    fdicInsuredBankSweepAccountCashComponentShort: Optional[Decimal] = None
    fdicInsuredAccountInterestAccruals: Optional[Decimal] = None
    fdicInsuredAccountInterestAccrualsLong: Optional[Decimal] = None
    fdicInsuredAccountInterestAccrualsShort: Optional[Decimal] = None
    fdicInsuredAccountInterestAccrualsComponent: Optional[Decimal] = None
    fdicInsuredAccountInterestAccrualsComponentLong: Optional[Decimal] = None
    fdicInsuredAccountInterestAccrualsComponentShort: Optional[Decimal] = None
    total: Optional[Decimal] = None
    totalLong: Optional[Decimal] = None
    totalShort: Optional[Decimal] = None
    brokerInterestAccrualsComponent: Optional[Decimal] = None
    brokerCashComponent: Optional[Decimal] = None
    cfdUnrealizedPl: Optional[Decimal] = None


@dataclass(frozen=True)
class CashReportCurrency(FlexElement, AccountMixin):
    """ Wrapped in <CashReport> """
    currency: str
    fromDate: datetime.date
    toDate: datetime.date
    startingCash: Optional[Decimal] = None
    startingCashSec: Optional[Decimal] = None
    startingCashCom: Optional[Decimal] = None
    clientFees: Optional[Decimal] = None
    clientFeesSec: Optional[Decimal] = None
    clientFeesCom: Optional[Decimal] = None
    clientFeesMTD: Optional[Decimal] = None
    clientFeesYTD: Optional[Decimal] = None
    commissions: Optional[Decimal] = None
    commissionsSec: Optional[Decimal] = None
    commissionsCom: Optional[Decimal] = None
    commissionsMTD: Optional[Decimal] = None
    commissionsYTD: Optional[Decimal] = None
    billableCommissions: Optional[Decimal] = None
    billableCommissionsSec: Optional[Decimal] = None
    billableCommissionsCom: Optional[Decimal] = None
    billableCommissionsMTD: Optional[Decimal] = None
    billableCommissionsYTD: Optional[Decimal] = None
    depositWithdrawals: Optional[Decimal] = None
    depositWithdrawalsSec: Optional[Decimal] = None
    depositWithdrawalsCom: Optional[Decimal] = None
    depositWithdrawalsMTD: Optional[Decimal] = None
    depositWithdrawalsYTD: Optional[Decimal] = None
    deposits: Optional[Decimal] = None
    depositsSec: Optional[Decimal] = None
    depositsCom: Optional[Decimal] = None
    depositsMTD: Optional[Decimal] = None
    depositsYTD: Optional[Decimal] = None
    withdrawals: Optional[Decimal] = None
    withdrawalsSec: Optional[Decimal] = None
    withdrawalsCom: Optional[Decimal] = None
    withdrawalsMTD: Optional[Decimal] = None
    withdrawalsYTD: Optional[Decimal] = None
    accountTransfers: Optional[Decimal] = None
    accountTransfersSec: Optional[Decimal] = None
    accountTransfersCom: Optional[Decimal] = None
    accountTransfersMTD: Optional[Decimal] = None
    accountTransfersYTD: Optional[Decimal] = None
    linkingAdjustments: Optional[Decimal] = None
    linkingAdjustmentsSec: Optional[Decimal] = None
    linkingAdjustmentsCom: Optional[Decimal] = None
    internalTransfers: Optional[Decimal] = None
    internalTransfersSec: Optional[Decimal] = None
    internalTransfersCom: Optional[Decimal] = None
    internalTransfersMTD: Optional[Decimal] = None
    internalTransfersYTD: Optional[Decimal] = None
    dividends: Optional[Decimal] = None
    dividendsSec: Optional[Decimal] = None
    dividendsCom: Optional[Decimal] = None
    dividendsMTD: Optional[Decimal] = None
    dividendsYTD: Optional[Decimal] = None
    insuredDepositInterest: Optional[Decimal] = None
    insuredDepositInterestSec: Optional[Decimal] = None
    insuredDepositInterestCom: Optional[Decimal] = None
    insuredDepositInterestMTD: Optional[Decimal] = None
    insuredDepositInterestYTD: Optional[Decimal] = None
    brokerInterest: Optional[Decimal] = None
    brokerInterestSec: Optional[Decimal] = None
    brokerInterestCom: Optional[Decimal] = None
    brokerInterestMTD: Optional[Decimal] = None
    brokerInterestYTD: Optional[Decimal] = None
    bondInterest: Optional[Decimal] = None
    bondInterestSec: Optional[Decimal] = None
    bondInterestCom: Optional[Decimal] = None
    bondInterestMTD: Optional[Decimal] = None
    bondInterestYTD: Optional[Decimal] = None
    cashSettlingMtm: Optional[Decimal] = None
    cashSettlingMtmSec: Optional[Decimal] = None
    cashSettlingMtmCom: Optional[Decimal] = None
    cashSettlingMtmMTD: Optional[Decimal] = None
    cashSettlingMtmYTD: Optional[Decimal] = None
    realizedVm: Optional[Decimal] = None
    realizedVmSec: Optional[Decimal] = None
    realizedVmCom: Optional[Decimal] = None
    realizedVmMTD: Optional[Decimal] = None
    realizedVmYTD: Optional[Decimal] = None
    cfdCharges: Optional[Decimal] = None
    cfdChargesSec: Optional[Decimal] = None
    cfdChargesCom: Optional[Decimal] = None
    cfdChargesMTD: Optional[Decimal] = None
    cfdChargesYTD: Optional[Decimal] = None
    netTradesSales: Optional[Decimal] = None
    netTradesSalesSec: Optional[Decimal] = None
    netTradesSalesCom: Optional[Decimal] = None
    netTradesSalesMTD: Optional[Decimal] = None
    netTradesSalesYTD: Optional[Decimal] = None
    netTradesPurchases: Optional[Decimal] = None
    netTradesPurchasesSec: Optional[Decimal] = None
    netTradesPurchasesCom: Optional[Decimal] = None
    netTradesPurchasesMTD: Optional[Decimal] = None
    netTradesPurchasesYTD: Optional[Decimal] = None
    advisorFees: Optional[Decimal] = None
    advisorFeesSec: Optional[Decimal] = None
    advisorFeesCom: Optional[Decimal] = None
    advisorFeesMTD: Optional[Decimal] = None
    advisorFeesYTD: Optional[Decimal] = None
    feesReceivables: Optional[Decimal] = None
    feesReceivablesSec: Optional[Decimal] = None
    feesReceivablesCom: Optional[Decimal] = None
    feesReceivablesMTD: Optional[Decimal] = None
    feesReceivablesYTD: Optional[Decimal] = None
    paymentInLieu: Optional[Decimal] = None
    paymentInLieuSec: Optional[Decimal] = None
    paymentInLieuCom: Optional[Decimal] = None
    paymentInLieuMTD: Optional[Decimal] = None
    paymentInLieuYTD: Optional[Decimal] = None
    transactionTax: Optional[Decimal] = None
    transactionTaxSec: Optional[Decimal] = None
    transactionTaxCom: Optional[Decimal] = None
    transactionTaxMTD: Optional[Decimal] = None
    transactionTaxYTD: Optional[Decimal] = None
    taxReceivables: Optional[Decimal] = None
    taxReceivablesSec: Optional[Decimal] = None
    taxReceivablesCom: Optional[Decimal] = None
    taxReceivablesMTD: Optional[Decimal] = None
    taxReceivablesYTD: Optional[Decimal] = None
    withholdingTax: Optional[Decimal] = None
    withholdingTaxSec: Optional[Decimal] = None
    withholdingTaxCom: Optional[Decimal] = None
    withholdingTaxMTD: Optional[Decimal] = None
    withholdingTaxYTD: Optional[Decimal] = None
    withholding871m: Optional[Decimal] = None
    withholding871mSec: Optional[Decimal] = None
    withholding871mCom: Optional[Decimal] = None
    withholding871mMTD: Optional[Decimal] = None
    withholding871mYTD: Optional[Decimal] = None
    withholdingCollectedTax: Optional[Decimal] = None
    withholdingCollectedTaxSec: Optional[Decimal] = None
    withholdingCollectedTaxCom: Optional[Decimal] = None
    withholdingCollectedTaxMTD: Optional[Decimal] = None
    withholdingCollectedTaxYTD: Optional[Decimal] = None
    salesTax: Optional[Decimal] = None
    salesTaxSec: Optional[Decimal] = None
    salesTaxCom: Optional[Decimal] = None
    salesTaxMTD: Optional[Decimal] = None
    salesTaxYTD: Optional[Decimal] = None
    fxTranslationGainLoss: Optional[Decimal] = None
    fxTranslationGainLossSec: Optional[Decimal] = None
    fxTranslationGainLossCom: Optional[Decimal] = None
    otherFees: Optional[Decimal] = None
    otherFeesSec: Optional[Decimal] = None
    otherFeesCom: Optional[Decimal] = None
    otherFeesMTD: Optional[Decimal] = None
    otherFeesYTD: Optional[Decimal] = None
    other: Optional[Decimal] = None
    otherSec: Optional[Decimal] = None
    otherCom: Optional[Decimal] = None
    endingCash: Optional[Decimal] = None
    endingCashSec: Optional[Decimal] = None
    endingCashCom: Optional[Decimal] = None
    endingSettledCash: Optional[Decimal] = None
    endingSettledCashSec: Optional[Decimal] = None
    endingSettledCashCom: Optional[Decimal] = None


@dataclass(frozen=True)
class StatementOfFundsLine(FlexElement, AccountMixin, SecurityMixin):
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
class ChangeInPositionValue(FlexElement, AccountMixin):
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
class OpenPosition(FlexElement, AccountMixin, CurrencyMixin, SecurityMixin):
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
class FxLot(FlexElement, AccountMixin):
    """ Wrapped in <FxLots>, which in turn is wrapped in <FxPositions> """
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
class Trade(FlexElement, TradeMixin):
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
class TradeConfirmation(FlexElement, TradeMixin):
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
class OptionEAE(FlexElement, AccountMixin, CurrencyMixin, SecurityMixin):
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
class TradeTransfer(FlexElement, TradeMixin):
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
class InterestAccrualsCurrency(FlexElement, AccountMixin):
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
class SLBActivity(FlexElement, AccountMixin, CurrencyMixin, SecurityMixin):
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
class Transfer(FlexElement, AccountMixin, CurrencyMixin, SecurityMixin):
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
class PriorPeriodPosition(FlexElement, AccountMixin, CurrencyMixin, SecurityMixin):
    """ Wrapped in <PriorPeriodPositions> """
    priorMtmPnl: decimal.Decimal
    date: datetime.date
    price: decimal.Decimal


@dataclass(frozen=True)
class CorporateAction(FlexElement, AccountMixin, CurrencyMixin, SecurityMixin):
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
class CashTransaction(FlexElement, AccountMixin, CurrencyMixin, SecurityMixin):
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
class ChangeInDividendAccrual(FlexElement, DividendAccrualMixin):
    """ Wrapped in <ChangeInDividendAccruals> """
    date: datetime.date


#  Type alias to work around https://github.com/python/mypy/issues/1775
_ChangeInDividendAccrual = ChangeInDividendAccrual


@dataclass(frozen=True)
class OpenDividendAccrual(FlexElement, DividendAccrualMixin):
    """ Wrapped in <OpenDividendAccruals> """
    pass


@dataclass(frozen=True)
class SecurityInfo(FlexElement, SecurityMixin):
    """ Wrapped in <SecuritiesInfo> """
    maturity: str
    issueDate: datetime.date
    code: List[str]


@dataclass(frozen=True)
class ConversionRate(FlexElement):
    """ Wrapped in <ConversionRates> """
    reportDate: datetime.date
    fromCurrency: str
    toCurrency: str
    rate: decimal.Decimal
