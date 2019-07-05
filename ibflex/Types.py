# coding: utf-8
"""Python data types for IB Flex format XML data.

These class definitions are introspected by ibflex.parser to type-convert
IB data.  They're dataclasses, made immutable by passing `Frozen=True` to the
class  decorator.  Class attributes are annotated with PEP 484 type hints.

Except for the top-level XML elements, i.e. <FlexQueryResponse>,
<FlexStatements>, and <FlexStatement>, the Flex format cleanly differentiates
between data-bearing elements and container elements.  Data elements hold
their values in XML element attributes; container elements are sequences
of child elements (usually data elements, but sometimes other containers).

XML element attributes are represented by class attributes hinted with the
Python type to which their values should be converted.  Almost all are marked
`Optional`, since Flex report configuration allows any of them to be included
or omitted individually.  Default value is `None` for a single value, or an
empty tuple for a sequence.

Specifically defined enums are an exception; the parser handles missing values
for them, so you shouldn't specify a default value.  The enums therefore need
to come first in the class definition to avoid offending dataclass.

Some data elements have XML attributes whose values are sequences delimited by
commas or semicolons.  These are represented as by class attributes hinted as
a variable-length `Tuple` of their sequence item type (`str` or an Enum type).

XML container elements are represented as variable-length `Tuple` of contained
child type.


TODO - need types for:
    FdicInsuredDepositsByBank
    ComplexPositions
    HKIPOSubscriptionActivity
    PendingExcercises
    FxTransactions
    UnbookedTrades
    RoutingCommissions
    IBGNoteTransactions
    Adjustments
    DebitCardActivities
    SoftDollars
    SalesTaxes
    CFDCharges
    SLBOpenContracts
    HKIPOOpenSubscriptions
"""

__all__ = [
    "CashAction", "TradeType", "BuySell", "OpenClose", "OrderType", "Reorg",
    "OptionAction", "LongShort", "TransferType", "ToFrom", "InOut",
    "DeliveredReceived", "FlexElement", "FlexQueryResponse", "FlexStatement",
    "AccountInformation", "ChangeInNAV", "MTMPerformanceSummaryUnderlying",
    "EquitySummaryByReportDateInBase", "MTDYTDPerformanceSummaryUnderlying",
    "CashReportCurrency", "FIFOPerformanceSummaryUnderlying",
    "NetStockPosition", "UnsettledTransfer", "UnbundledCommissionDetail",
    "StatementOfFundsLine", "ChangeInPositionValue", "OpenPosition", "FxLot",
    "Trade", "TradeConfirm", "OptionEAE", "TradeTransfer",
    "TierInterestDetail", "HardToBorrowDetail", "InterestAccrualsCurrency",
    "SLBActivity", "Transfer", "CorporateAction", "CashTransaction",
    "ChangeInDividendAccrual", "OpenDividendAccrual", "SecurityInfo",
    "ConversionRate", "PriorPeriodPosition",
]


import datetime
import decimal
from decimal import Decimal
import enum
from dataclasses import dataclass
from typing import Tuple, Optional, _GenericAlias, _VariadicGenericAlias


###############################################################################
#  ENUMS
#  Values are the text sent by IB in XML element attribute.
#  Names keep the convention of using UPPERCASE for Enums.
###############################################################################
@enum.unique
class CashAction(enum.Enum):
    DEPOSITWITHDRAW = "Deposits & Withdrawals"
    BROKERINTPAID = "Broker Interest Paid"
    BROKERINTRCVD = "Broker Interest Received"
    WHTAX = "Withholding Tax"
    BONDINTRCVD = "Bond Interest Received"
    BONDINTPAID = "Bond Interest Paid"
    FEES = "Other Fees"
    DIVIDEND = "Dividends"
    PAYMENTINLIEU = "Payment In Lieu Of Dividends"


@enum.unique
class Code(enum.Enum):
    """Used for both `code` and `notes` attributes.
    """
    ASSIGNMENT = "A"
    AUTOEXERCISE = "AEx"        # Automatic exercise for dividend-related recommendation
    ADJUSTMENT = "Adj"          # Adjustment
    ALLOCATION = "Al"           # Allocation
    AWAY = "Aw"                 # Away Trade
    BUYIN = "B"                 # Automatic Buy-in
    BORROW = "Bo"               # Direct Borrow
    CLOSING = "C"               # Closing Trade
    CASHDELIVERY = "CD"         # Cash Delivery
    COMPLEX = "CP"              # Complex Position
    CANCEL = "Ca"               # Cancelled
    CORRECT = "Co"              # Corrected Trade
    CROSSING = "Cx"             # Part or all of this transaction was a Crossing executed as dual agent by IB for two IB customers
    ETF = "ETF"                 # ETF Creation/Redemption
    EXPIRED = "Ep"              # Resulted from an Expired Position
    EXERCISE = "Ex"             # Exercise
    GUARANTEED = "G"            # Trade in Guaranteed Account Segment
    HIGHESTCOST = "HC"          # Highest Cost tax lot-matching method
    HFINVESTMENT = "HFI"        # Investment Transferred to Hedge Fund
    HFREDEMPTION = "HFR"        # Redemption from Hedge Fund
    INTERNAL = "I"              # Internal Transfer
    AFFILIATE = "IA"            # This transaction was executed against an IB affiliate
    INVESTOR = "INV"            # Investment Transfer from Investor
    MARGINLOW = "L"             # Ordered by IB (Margin Violation)
    WASHSALE = "LD"             # Adjusted by Loss Disallowed from Wash Sale
    LIFO = "LI"                 # Last In, First Out (LIFO) tax lot-matching method
    LTCG = "LT"                 # Long-term P/L
    LOAN = "Lo"                 # Direct Loan
    MANUAL = "M"                # Entered manually by IB
    MANUALEXERCISE = "MEx"      # Manual exercise for dividend-related recommendation
    MAXLOSS = "ML"              # Maximize Losses tax basis election
    MAXLTCG = "MLG"             # Maximize Long-Term Gain tax lot-matching method
    MINLTCG = "MLL"             # Maximize Long-Term Loss tax lot-matching method
    MAXSTCG = "MSG"             # Maximize Short-Term Gain tax lot-matching method
    MINSTCG = "MSL"             # Maximize Short-Term Loss tax lot-matching method
    OPENING = "O"               # Opening Trade
    PARTIAL = "P"               # Partial Execution
    PRICEIMPROVEMENT = "PI"     # Price Improvement
    POSTACCRUAL = "Po"          # Interest or Dividend Accrual Posting
    PRINCIPAL = "Pr"            # Part or all of this transaction was executed by the Exchange as a Crossing by IB against an IB affiliate and is therefore classified as a Principal and not an agency trade
    REINVESTMENT = "R"          # Dividend Reinvestment
    REDEMPTION = "RED"          # Redemption to Investor
    REVERSE = "Re"              # Interest or Dividend Accrual Reversal
    REIMBURSEMENT = "Ri"        # Reimbursement
    SOLICITEDIB = "SI"          # This order was solicited by Interactive Brokers
    SPECIFICLOT = "SL"          # Specific Lot tax lot-matching method
    SOLICITEDOTHER = "SO"       # This order was marked as solicited by your Introducing Broker
    SHORTENEDSETTLEMENT = "SS"  # Customer designated this trade for shortened settlement and so is subject to execution at prices above the prevailing market
    STCG = "ST"                 # Short-term P/L
    STOCKYIELD = "SY"           # Positions that may be eligible for Stock Yield.
    TRANSFER = "T"              # Transfer


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
class Reorg(enum.Enum):
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
class OptionAction(enum.Enum):
    ASSIGN = "Assignment"
    EXERCISE = "Exercise"
    EXPIRE = "Expiration"
    SELL = "Sell"


@enum.unique
class LongShort(enum.Enum):
    LONG = "Long"
    SHORT = "Short"


@enum.unique
class ToFrom(enum.Enum):
    TO = "To"
    FROM = "From"


@enum.unique
class TransferType(enum.Enum):
    INTERNAL = "INTERNAL"
    ACATS = "ACATS"


@enum.unique
class InOut(enum.Enum):
    IN = "IN"
    OUT = "OUT"


@enum.unique
class DeliveredReceived(enum.Enum):
    DELIVERED = "Delivered"
    RECEIVED = "Received"


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
    FlexStatements: Tuple["FlexStatement", ...]


@dataclass(frozen=True)
class FlexStatement(FlexElement):
    """ Wrapped in <FlexStatements> """
    accountId: str
    fromDate: datetime.date
    toDate: datetime.date
    period: str
    whenGenerated: datetime.datetime
    AccountInformation: Optional["_AccountInformation"] = None
    ChangeInNAV: Optional["_ChangeInNAV"] = None
    CashReport: Tuple["CashReportCurrency", ...] = ()
    MTDYTDPerformanceSummary: Tuple["MTDYTDPerformanceSummaryUnderlying", ...] = ()
    MTMPerformanceSummaryInBase: Tuple["MTMPerformanceSummaryUnderlying", ...] = ()
    EquitySummaryInBase: Tuple["EquitySummaryByReportDateInBase", ...] = ()
    FIFOPerformanceSummaryInBase: Tuple["FIFOPerformanceSummaryUnderlying", ...] = ()
    FdicInsuredDepositsByBank: Tuple = ()  # TODO
    StmtFunds: Tuple["StatementOfFundsLine", ...] = ()
    ChangeInPositionValues: Tuple["ChangeInPositionValue", ...] = ()
    OpenPositions: Tuple["OpenPosition", ...] = ()
    NetStockPositionSummary: Tuple["NetStockPosition", ...] = ()
    ComplexPositions: Tuple = ()  # TODO
    FxPositions: Tuple["FxLot", ...] = ()  # N.B. FXLot wrapped in FxLots
    Trades: Tuple["Trade", ...] = ()
    HKIPOSubscriptionActivity: Tuple = ()  # TODO
    TradeConfirms: Tuple["TradeConfirm", ...] = ()
    TransactionTaxes: Tuple = ()
    OptionEAE: Tuple["_OptionEAE", ...] = ()
    # Not a typo - they really spell it "Excercises"
    PendingExcercises: Tuple = ()  # TODO
    TradeTransfers: Tuple["TradeTransfer", ...] = ()
    FxTransactions: Tuple = ()  # TODO
    UnbookedTrades: Tuple = ()  # TODO
    RoutingCommissions: Tuple = ()  # TODO
    IBGNoteTransactions: Tuple = ()  # TODO
    UnsettledTransfers: Tuple["UnsettledTransfer", ...] = ()
    UnbundledCommissionDetails: Tuple["UnbundledCommissionDetail", ...] = ()
    Adjustments: Tuple = ()  # TODO
    PriorPeriodPositions: Tuple["PriorPeriodPosition", ...] = ()
    CorporateActions: Tuple["CorporateAction", ...] = ()
    ClientFees: Tuple["ClientFee", ...] = ()
    ClientFeesDetail: Tuple["_ClientFeesDetail", ...] = ()
    DebitCardActivities: Tuple = ()  # TODO
    SoftDollars: Tuple = ()  # TODO
    CashTransactions: Tuple["CashTransaction", ...] = ()
    SalesTaxes: Tuple = ()  # TODO
    CFDCharges: Tuple = ()  # TODO
    InterestAccruals: Tuple["InterestAccrualsCurrency", ...] = ()
    TierInterestDetails: Tuple["TierInterestDetail", ...] = ()
    HardToBorrowDetails: Tuple["HardToBorrowDetail", ...] = ()
    HardToBorrowMarkupDetails: Tuple = ()
    SLBOpenContracts: Tuple = ()  # TODO
    SLBActivities: Tuple["SLBActivity", ...] = ()
    SLBFees: Tuple = ()
    Transfers: Tuple["Transfer", ...] = ()
    ChangeInDividendAccruals: Tuple["_ChangeInDividendAccrual", ...] = ()
    OpenDividendAccruals: Tuple["OpenDividendAccrual", ...] = ()
    SecuritiesInfo: Tuple["SecurityInfo", ...] = ()
    ConversionRates: Tuple["ConversionRate", ...] = ()
    HKIPOOpenSubscriptions: Tuple = ()  # TODO

    def __repr__(self):
        repr = (
            f"{type(self).__name__}(accountId={self.accountId}, "
            f"fromDate={self.fromDate}, toDate={self.toDate}, period={self.period}, "
            f"whenGenerated={self.whenGenerated})"
        )

        sequences = (
            (k, getattr(self, k)) for k, v in self.__annotations__.items()
            if type(v) in (_GenericAlias, _VariadicGenericAlias)
            and v.__origin__ is tuple
        )
        nonempty_sequences = ", ".join(
            f"len({name})={len(value)}" for (name, value) in sequences if value
        )
        if nonempty_sequences:
            repr += ", "
            for seq in nonempty_sequences:
                repr += seq
        repr += ")"
        return repr



@dataclass(frozen=True)
class AccountInformation(FlexElement):
    """ Child of <FlexStatement> """
    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    currency: Optional[str] = None
    name: Optional[str] = None
    accountType: Optional[str] = None
    customerType: Optional[str] = None
    accountCapabilities: Tuple[str, ...] = ()
    tradingPermissions: Tuple[str, ...] = ()
    registeredRepName: Optional[str] = None
    registeredRepPhone: Optional[str] = None
    dateOpened: Optional[datetime.date] = None
    dateFunded: Optional[datetime.date] = None
    dateClosed: Optional[datetime.date] = None
    street: Optional[str] = None
    street2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postalCode: Optional[str] = None
    streetResidentialAddress: Optional[str] = None
    street2ResidentialAddress: Optional[str] = None
    cityResidentialAddress: Optional[str] = None
    stateResidentialAddress: Optional[str] = None
    countryResidentialAddress: Optional[str] = None
    postalCodeResidentialAddress: Optional[str] = None
    masterName: Optional[str] = None
    ibEntity: Optional[str] = None
    primaryEmail: Optional[str] = None


#  Type alias to work around https://github.com/python/mypy/issues/1775
_AccountInformation = AccountInformation


@dataclass(frozen=True)
class ChangeInNAV(FlexElement):
    """ Child of <FlexStatement> """
    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    fromDate: Optional[datetime.date] = None
    toDate: Optional[datetime.date] = None
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
class MTMPerformanceSummaryUnderlying(FlexElement):
    """ Wrapped in <MTMPerformanceSummaryInBase> """
    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    assetCategory: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    securityID: Optional[str] = None
    securityIDType: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    sedol: Optional[str] = None
    listingExchange: Optional[str] = None
    underlyingConid: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    underlyingSecurityID: Optional[str] = None
    underlyingListingExchange: Optional[str] = None
    issuer: Optional[str] = None
    multiplier: Optional[decimal.Decimal] = None
    strike: Optional[decimal.Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[str] = None
    principalAdjustFactor: Optional[decimal.Decimal] = None
    reportDate: Optional[datetime.date] = None
    prevCloseQuantity: Optional[Decimal] = None
    prevClosePrice: Optional[Decimal] = None
    closeQuantity: Optional[Decimal] = None
    closePrice: Optional[Decimal] = None
    transactionMtm: Optional[Decimal] = None
    priorOpenMtm: Optional[Decimal] = None
    commissions: Optional[Decimal] = None
    other: Optional[Decimal] = None
    total: Optional[Decimal] = None
    code: Tuple[Code, ...] = ()
    corpActionMtm: Optional[Decimal] = None
    dividends: Optional[Decimal] = None


@dataclass(frozen=True)
class EquitySummaryByReportDateInBase(FlexElement):
    """ Wrapped in <EquitySummaryInBase> """
    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    reportDate: Optional[datetime.date] = None
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
    bonds: Optional[Decimal] = None
    bondsLong: Optional[Decimal] = None
    bondsShort: Optional[Decimal] = None
    notes: Optional[Decimal] = None
    notesLong: Optional[Decimal] = None
    notesShort: Optional[Decimal] = None
    interestAccruals: Optional[Decimal] = None
    interestAccrualsLong: Optional[Decimal] = None
    interestAccrualsShort: Optional[Decimal] = None
    softDollars: Optional[Decimal] = None
    softDollarsLong: Optional[Decimal] = None
    softDollarsShort: Optional[Decimal] = None
    dividendAccruals: Optional[Decimal] = None
    dividendAccrualsLong: Optional[Decimal] = None
    dividendAccrualsShort: Optional[Decimal] = None
    total: Optional[Decimal] = None
    totalLong: Optional[Decimal] = None
    totalShort: Optional[Decimal] = None
    commodities: Optional[Decimal] = None
    commoditiesLong: Optional[Decimal] = None
    commoditiesShort: Optional[Decimal] = None
    funds: Optional[Decimal] = None
    fundsLong: Optional[Decimal] = None
    fundsShort: Optional[Decimal] = None
    forexCfdUnrealizedPl: Optional[Decimal] = None
    forexCfdUnrealizedPlLong: Optional[Decimal] = None
    forexCfdUnrealizedPlShort: Optional[Decimal] = None
    brokerInterestAccrualsComponent: Optional[Decimal] = None
    brokerCashComponent: Optional[Decimal] = None
    cfdUnrealizedPl: Optional[Decimal] = None
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
    brokerCashComponentLong: Optional[Decimal] = None
    brokerCashComponentShort: Optional[Decimal] = None
    brokerInterestAccrualsComponentLong: Optional[Decimal] = None
    brokerInterestAccrualsComponentShort: Optional[Decimal] = None
    cfdUnrealizedPlLong: Optional[Decimal] = None
    cfdUnrealizedPlShort: Optional[Decimal] = None


@dataclass(frozen=True)
class MTDYTDPerformanceSummaryUnderlying(FlexElement):
    """ Wrapped in <MTDYTDPerformanceSummary> """
    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    assetCategory: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    securityID: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    listingExchange: Optional[str] = None
    underlyingConid: Optional[str] = None
    underlyingSecurityID: Optional[str] = None
    underlyingListingExchange: Optional[str] = None
    mtmMTD: Optional[Decimal] = None
    mtmYTD: Optional[Decimal] = None
    realSTMTD: Optional[Decimal] = None
    realSTYTD: Optional[Decimal] = None
    realLTMTD: Optional[Decimal] = None
    realLTYTD: Optional[Decimal] = None
    securityIDType: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    issuer: Optional[str] = None
    multiplier: Optional[Decimal] = None
    strike: Optional[decimal.Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[str] = None
    principalAdjustFactor: Optional[Decimal] = None
    realizedPnlMTD: Optional[Decimal] = None
    realizedCapitalGainsPnlMTD: Optional[Decimal] = None
    realizedFxPnlMTD: Optional[Decimal] = None
    realizedPnlYTD: Optional[Decimal] = None
    realizedCapitalGainsPnlYTD: Optional[Decimal] = None
    realizedFxPnlYTD: Optional[Decimal] = None


@dataclass(frozen=True)
class CashReportCurrency(FlexElement):
    """ Wrapped in <CashReport> """
    accountId: Optional[str] = None
    currency: Optional[str] = None
    fromDate: Optional[datetime.date] = None
    toDate: Optional[datetime.date] = None
    startingCash: Optional[Decimal] = None
    startingCashSec: Optional[Decimal] = None
    startingCashCom: Optional[Decimal] = None
    clientFees: Optional[Decimal] = None
    clientFeesSec: Optional[Decimal] = None
    clientFeesCom: Optional[Decimal] = None
    commissions: Optional[Decimal] = None
    commissionsSec: Optional[Decimal] = None
    commissionsCom: Optional[Decimal] = None
    billableCommissions: Optional[Decimal] = None
    billableCommissionsSec: Optional[Decimal] = None
    billableCommissionsCom: Optional[Decimal] = None
    depositWithdrawals: Optional[Decimal] = None
    depositWithdrawalsSec: Optional[Decimal] = None
    depositWithdrawalsCom: Optional[Decimal] = None
    deposits: Optional[Decimal] = None
    depositsSec: Optional[Decimal] = None
    depositsCom: Optional[Decimal] = None
    withdrawals: Optional[Decimal] = None
    withdrawalsSec: Optional[Decimal] = None
    withdrawalsCom: Optional[Decimal] = None
    accountTransfers: Optional[Decimal] = None
    accountTransfersSec: Optional[Decimal] = None
    accountTransfersCom: Optional[Decimal] = None
    internalTransfers: Optional[Decimal] = None
    internalTransfersSec: Optional[Decimal] = None
    internalTransfersCom: Optional[Decimal] = None
    dividends: Optional[Decimal] = None
    dividendsSec: Optional[Decimal] = None
    dividendsCom: Optional[Decimal] = None
    brokerInterest: Optional[Decimal] = None
    brokerInterestSec: Optional[Decimal] = None
    brokerInterestCom: Optional[Decimal] = None
    bondInterest: Optional[Decimal] = None
    bondInterestSec: Optional[Decimal] = None
    bondInterestCom: Optional[Decimal] = None
    cashSettlingMtm: Optional[Decimal] = None
    cashSettlingMtmSec: Optional[Decimal] = None
    cashSettlingMtmCom: Optional[Decimal] = None
    cfdCharges: Optional[Decimal] = None
    cfdChargesSec: Optional[Decimal] = None
    cfdChargesCom: Optional[Decimal] = None
    netTradesSales: Optional[Decimal] = None
    netTradesSalesSec: Optional[Decimal] = None
    netTradesSalesCom: Optional[Decimal] = None
    netTradesPurchases: Optional[Decimal] = None
    netTradesPurchasesSec: Optional[Decimal] = None
    netTradesPurchasesCom: Optional[Decimal] = None
    feesReceivables: Optional[Decimal] = None
    feesReceivablesSec: Optional[Decimal] = None
    feesReceivablesCom: Optional[Decimal] = None
    paymentInLieu: Optional[Decimal] = None
    paymentInLieuSec: Optional[Decimal] = None
    paymentInLieuCom: Optional[Decimal] = None
    transactionTax: Optional[Decimal] = None
    transactionTaxSec: Optional[Decimal] = None
    transactionTaxCom: Optional[Decimal] = None
    withholdingTax: Optional[Decimal] = None
    withholdingTaxSec: Optional[Decimal] = None
    withholdingTaxCom: Optional[Decimal] = None
    fxTranslationGainLoss: Optional[Decimal] = None
    fxTranslationGainLossSec: Optional[Decimal] = None
    fxTranslationGainLossCom: Optional[Decimal] = None
    otherFees: Optional[Decimal] = None
    otherFeesSec: Optional[Decimal] = None
    otherFeesCom: Optional[Decimal] = None
    endingCash: Optional[Decimal] = None
    endingCashSec: Optional[Decimal] = None
    endingCashCom: Optional[Decimal] = None
    endingSettledCash: Optional[Decimal] = None
    endingSettledCashSec: Optional[Decimal] = None
    endingSettledCashCom: Optional[Decimal] = None
    clientFeesMTD: Optional[Decimal] = None
    clientFeesYTD: Optional[Decimal] = None
    commissionsMTD: Optional[Decimal] = None
    commissionsYTD: Optional[Decimal] = None
    billableCommissionsMTD: Optional[Decimal] = None
    billableCommissionsYTD: Optional[Decimal] = None
    depositWithdrawalsMTD: Optional[Decimal] = None
    depositWithdrawalsYTD: Optional[Decimal] = None
    depositsMTD: Optional[Decimal] = None
    depositsYTD: Optional[Decimal] = None
    withdrawalsMTD: Optional[Decimal] = None
    withdrawalsYTD: Optional[Decimal] = None
    accountTransfersMTD: Optional[Decimal] = None
    accountTransfersYTD: Optional[Decimal] = None
    internalTransfersMTD: Optional[Decimal] = None
    internalTransfersYTD: Optional[Decimal] = None
    dividendsMTD: Optional[Decimal] = None
    dividendsYTD: Optional[Decimal] = None
    insuredDepositInterestMTD: Optional[Decimal] = None
    insuredDepositInterestYTD: Optional[Decimal] = None
    brokerInterestMTD: Optional[Decimal] = None
    brokerInterestYTD: Optional[Decimal] = None
    bondInterestMTD: Optional[Decimal] = None
    bondInterestYTD: Optional[Decimal] = None
    cashSettlingMtmMTD: Optional[Decimal] = None
    cashSettlingMtmYTD: Optional[Decimal] = None
    realizedVmMTD: Optional[Decimal] = None
    realizedVmYTD: Optional[Decimal] = None
    cfdChargesMTD: Optional[Decimal] = None
    cfdChargesYTD: Optional[Decimal] = None
    netTradesSalesMTD: Optional[Decimal] = None
    netTradesSalesYTD: Optional[Decimal] = None
    advisorFeesMTD: Optional[Decimal] = None
    advisorFeesYTD: Optional[Decimal] = None
    feesReceivablesMTD: Optional[Decimal] = None
    feesReceivablesYTD: Optional[Decimal] = None
    netTradesPurchasesMTD: Optional[Decimal] = None
    netTradesPurchasesYTD: Optional[Decimal] = None
    paymentInLieuMTD: Optional[Decimal] = None
    paymentInLieuYTD: Optional[Decimal] = None
    transactionTaxMTD: Optional[Decimal] = None
    transactionTaxYTD: Optional[Decimal] = None
    taxReceivablesMTD: Optional[Decimal] = None
    taxReceivablesYTD: Optional[Decimal] = None
    withholdingTaxMTD: Optional[Decimal] = None
    withholdingTaxYTD: Optional[Decimal] = None
    withholding871mMTD: Optional[Decimal] = None
    withholding871mYTD: Optional[Decimal] = None
    withholdingCollectedTaxMTD: Optional[Decimal] = None
    withholdingCollectedTaxYTD: Optional[Decimal] = None
    salesTaxMTD: Optional[Decimal] = None
    salesTaxYTD: Optional[Decimal] = None
    otherFeesMTD: Optional[Decimal] = None
    otherFeesYTD: Optional[Decimal] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    avgCreditBalance: Optional[Decimal] = None
    avgCreditBalanceSec: Optional[Decimal] = None
    avgCreditBalanceCom: Optional[Decimal] = None
    avgDebitBalance: Optional[Decimal] = None
    avgDebitBalanceSec: Optional[Decimal] = None
    avgDebitBalanceCom: Optional[Decimal] = None
    linkingAdjustments: Optional[Decimal] = None
    linkingAdjustmentsSec: Optional[Decimal] = None
    linkingAdjustmentsCom: Optional[Decimal] = None
    insuredDepositInterest: Optional[Decimal] = None
    insuredDepositInterestSec: Optional[Decimal] = None
    insuredDepositInterestCom: Optional[Decimal] = None
    realizedVm: Optional[Decimal] = None
    realizedVmSec: Optional[Decimal] = None
    realizedVmCom: Optional[Decimal] = None
    advisorFees: Optional[Decimal] = None
    advisorFeesSec: Optional[Decimal] = None
    advisorFeesCom: Optional[Decimal] = None
    taxReceivables: Optional[Decimal] = None
    taxReceivablesSec: Optional[Decimal] = None
    taxReceivablesCom: Optional[Decimal] = None
    withholding871m: Optional[Decimal] = None
    withholding871mSec: Optional[Decimal] = None
    withholding871mCom: Optional[Decimal] = None
    withholdingCollectedTax: Optional[Decimal] = None
    withholdingCollectedTaxSec: Optional[Decimal] = None
    withholdingCollectedTaxCom: Optional[Decimal] = None
    salesTax: Optional[Decimal] = None
    salesTaxSec: Optional[Decimal] = None
    salesTaxCom: Optional[Decimal] = None
    other: Optional[Decimal] = None
    otherSec: Optional[Decimal] = None
    otherCom: Optional[Decimal] = None
    levelOfDetail: Optional[str] = None
    debitCardActivity: Optional[Decimal] = None
    debitCardActivitySec: Optional[Decimal] = None
    debitCardActivityCom: Optional[Decimal] = None
    debitCardActivityMTD: Optional[Decimal] = None
    debitCardActivityYTD: Optional[Decimal] = None
    billPay: Optional[Decimal] = None
    billPaySec: Optional[Decimal] = None
    billPayCom: Optional[Decimal] = None
    billPayMTD: Optional[Decimal] = None
    billPayYTD: Optional[Decimal] = None
    realizedForexVm: Optional[Decimal] = None
    realizedForexVmSec: Optional[Decimal] = None
    realizedForexVmCom: Optional[Decimal] = None
    realizedForexVmMTD: Optional[Decimal] = None
    realizedForexVmYTD: Optional[Decimal] = None
    ipoSubscription: Optional[Decimal] = None
    ipoSubscriptionSec: Optional[Decimal] = None
    ipoSubscriptionCom: Optional[Decimal] = None
    ipoSubscriptionMTD: Optional[Decimal] = None
    ipoSubscriptionYTD: Optional[Decimal] = None


@dataclass(frozen=True)
class StatementOfFundsLine(FlexElement):
    """ Wrapped in <StmtFunds> """
    accountId: Optional[str] = None
    balance: Optional[Decimal] = None
    debit: Optional[Decimal] = None
    credit: Optional[Decimal] = None
    currency: Optional[str] = None
    tradeID: Optional[str] = None
    # Despite the name, `date` actually contains date/time data.
    date: Optional[datetime.datetime] = None
    reportDate: Optional[datetime.date] = None
    activityDescription: Optional[str] = None
    amount: Optional[decimal.Decimal] = None
    buySell: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    assetCategory: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    securityID: Optional[str] = None
    securityIDType: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    underlyingConid: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    issuer: Optional[str] = None
    multiplier: Optional[decimal.Decimal] = None
    strike: Optional[decimal.Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[str] = None
    principalAdjustFactor: Optional[decimal.Decimal] = None
    fxRateToBase: Optional[Decimal] = None
    listingExchange: Optional[str] = None
    underlyingSecurityID: Optional[str] = None
    underlyingListingExchange: Optional[str] = None
    settleDate: Optional[str] = None
    activityCode: Optional[str] = None  # FIXME
    orderID: Optional[str] = None
    tradeQuantity: Optional[Decimal] = None
    tradePrice: Optional[Decimal] = None
    tradeGross: Optional[Decimal] = None
    tradeCommission: Optional[Decimal] = None
    tradeTax: Optional[Decimal] = None
    tradeCode: Optional[str] = None
    levelOfDetail: Optional[str] = None


@dataclass(frozen=True)
class ChangeInPositionValue(FlexElement):
    """ Wrapped in <ChangeInPositionValues> """
    currency: Optional[str] = None
    assetCategory: Optional[str] = None
    priorPeriodValue: Optional[Decimal] = None
    transactions: Optional[Decimal] = None
    mtmPriorPeriodPositions: Optional[Decimal] = None
    mtmTransactions: Optional[Decimal] = None
    corporateActions: Optional[Decimal] = None
    accountTransfers: Optional[Decimal] = None
    fxTranslationPnl: Optional[Decimal] = None
    futurePriceAdjustments: Optional[Decimal] = None
    settledCash: Optional[Decimal] = None
    endOfPeriodValue: Optional[Decimal] = None
    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    other: Optional[Decimal] = None
    linkingAdjustments: Optional[Decimal] = None


@dataclass(frozen=True)
class OpenPosition(FlexElement):
    """ Wrapped in <OpenPositions> """
    side: LongShort
    accountId: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[decimal.Decimal] = None
    reportDate: Optional[datetime.date] = None
    assetCategory: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    securityID: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    multiplier: Optional[decimal.Decimal] = None
    position: Optional[decimal.Decimal] = None
    markPrice: Optional[decimal.Decimal] = None
    positionValue: Optional[decimal.Decimal] = None
    openPrice: Optional[decimal.Decimal] = None
    costBasisPrice: Optional[decimal.Decimal] = None
    costBasisMoney: Optional[decimal.Decimal] = None
    fifoPnlUnrealized: Optional[decimal.Decimal] = None
    levelOfDetail: Optional[str] = None
    openDateTime: Optional[datetime.datetime] = None
    holdingPeriodDateTime: Optional[datetime.datetime] = None
    securityIDType: Optional[str] = None
    issuer: Optional[str] = None
    underlyingConid: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    code: Tuple[Code, ...] = ()
    originatingOrderID: Optional[str] = None
    originatingTransactionID: Optional[str] = None
    accruedInt: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    sedol: Optional[str] = None
    percentOfNAV: Optional[decimal.Decimal] = None
    strike: Optional[decimal.Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[str] = None
    principalAdjustFactor: Optional[decimal.Decimal] = None
    listingExchange: Optional[str] = None
    underlyingSecurityID: Optional[str] = None
    underlyingListingExchange: Optional[str] = None
    positionValueInBase: Optional[Decimal] = None
    unrealizedCapitalGainsPnl: Optional[Decimal] = None
    unrealizedlFxPnl: Optional[Decimal] = None


@dataclass(frozen=True)
class FxLot(FlexElement):
    """ Wrapped in <FxLots>, which in turn is wrapped in <FxPositions> """
    accountId: Optional[str] = None
    assetCategory: Optional[str] = None
    reportDate: Optional[datetime.date] = None
    functionalCurrency: Optional[str] = None
    fxCurrency: Optional[str] = None
    quantity: Optional[Decimal] = None
    costPrice: Optional[Decimal] = None
    costBasis: Optional[Decimal] = None
    closePrice: Optional[Decimal] = None
    value: Optional[Decimal] = None
    unrealizedPL: Optional[Decimal] = None
    code: Tuple[Code, ...] = ()
    lotDescription: Optional[str] = None
    lotOpenDateTime: Optional[datetime.datetime] = None
    levelOfDetail: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None


@dataclass(frozen=True)
class Trade(FlexElement):
    """ Wrapped in <Trades> """
    transactionType: TradeType
    openCloseIndicator: OpenClose
    buySell: BuySell
    orderType: OrderType
    accountId: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    assetCategory: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    listingExchange: Optional[str] = None
    multiplier: Optional[Decimal] = None
    strike: Optional[Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[str] = None
    tradeID: Optional[str] = None
    reportDate: Optional[datetime.date] = None
    tradeDate: Optional[datetime.date] = None
    tradeTime: Optional[datetime.time] = None
    settleDateTarget: Optional[datetime.date] = None
    exchange: Optional[str] = None
    quantity: Optional[Decimal] = None
    tradePrice: Optional[Decimal] = None
    tradeMoney: Optional[Decimal] = None
    taxes: Optional[Decimal] = None
    ibCommission: Optional[Decimal] = None
    ibCommissionCurrency: Optional[str] = None
    netCash: Optional[Decimal] = None
    netCashInBase: Optional[Decimal] = None
    closePrice: Optional[Decimal] = None
    notes: Tuple[Code, ...] = () # separator = ";"
    cost: Optional[Decimal] = None
    mtmPnl: Optional[Decimal] = None
    origTradePrice: Optional[Decimal] = None
    origTradeDate: Optional[datetime.date] = None
    origTradeID: Optional[str] = None
    origOrderID: Optional[str] = None
    openDateTime: Optional[datetime.datetime] = None
    fifoPnlRealized: Optional[Decimal] = None
    capitalGainsPnl: Optional[Decimal] = None
    levelOfDetail: Optional[str] = None
    ibOrderID: Optional[str] = None
    # Despite the name, `orderTime` actually contains date/time data.
    orderTime: Optional[datetime.datetime] = None
    changeInPrice: Optional[Decimal] = None
    changeInQuantity: Optional[Decimal] = None
    proceeds: Optional[decimal.Decimal] = None
    fxPnl: Optional[decimal.Decimal] = None
    clearingFirmID: Optional[str] = None
    #  Effective 2013, every Trade has a `transactionID` attribute that can't
    #  be deselected in the Flex query template.
    transactionID: Optional[str] = None
    holdingPeriodDateTime: Optional[datetime.datetime] = None
    ibExecID: Optional[str] = None
    brokerageOrderID: Optional[str] = None
    orderReference: Optional[str] = None
    volatilityOrderLink: Optional[str] = None
    exchOrderId: Optional[str] = None
    extExecID: Optional[str] = None
    traderID: Optional[str] = None
    isAPIOrder: Optional[bool] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    securityID: Optional[str] = None
    securityIDType: Optional[str] = None
    principalAdjustFactor: Optional[Decimal] = None
    dateTime: Optional[datetime.datetime] = None
    underlyingConid: Optional[str] = None
    underlyingSecurityID: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    underlyingListingExchange: Optional[str] = None
    issuer: Optional[str] = None
    sedol: Optional[str] = None
    whenRealized: Optional[datetime.datetime] = None
    whenReopened: Optional[datetime.datetime] = None


@dataclass(frozen=True)
class UnbundledCommissionDetail(FlexElement):
    """ Wrapped in <UnbundledCommissionDetails> """
    buySell: BuySell
    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    assetCategory: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    securityID: Optional[str] = None
    securityIDType: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    sedol: Optional[str] = None
    listingExchange: Optional[str] = None
    underlyingConid: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    underlyingSecurityID: Optional[str] = None
    underlyingListingExchange: Optional[str] = None
    issuer: Optional[str] = None
    multiplier: Optional[decimal.Decimal] = None
    strike: Optional[decimal.Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[str] = None
    principalAdjustFactor: Optional[Decimal] = None
    dateTime: Optional[datetime.datetime] = None
    exchange: Optional[str] = None
    quantity: Optional[Decimal] = None
    price: Optional[Decimal] = None
    tradeID: Optional[str] = None
    orderReference: Optional[str] = None
    totalCommission: Optional[Decimal] = None
    brokerExecutionCharge: Optional[Decimal] = None
    brokerClearingCharge: Optional[Decimal] = None
    thirdPartyExecutionCharge: Optional[Decimal] = None
    thirdPartyClearingCharge: Optional[Decimal] = None
    thirdPartyRegulatoryCharge: Optional[Decimal] = None
    regFINRATradingActivityFee: Optional[Decimal] = None
    regSection31TransactionFee: Optional[Decimal] = None
    regOther: Optional[Decimal] = None
    other: Optional[Decimal] = None


@dataclass(frozen=True)
class TradeConfirm(FlexElement):
    """ Wrapped in <TradeConfirms> """
    transactionType: TradeType
    openCloseIndicator: OpenClose
    buySell: BuySell
    orderType: OrderType
    accountId: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    assetCategory: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    securityID: Optional[str] = None
    securityIDType: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    underlyingConid: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    issuer: Optional[str] = None
    multiplier: Optional[Decimal] = None
    strike: Optional[Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[str] = None
    principalAdjustFactor: Optional[Decimal] = None
    tradeID: Optional[str] = None
    reportDate: Optional[datetime.date] = None
    tradeDate: Optional[datetime.date] = None
    tradeTime: Optional[datetime.time] = None
    settleDateTarget: Optional[datetime.date] = None
    exchange: Optional[str] = None
    quantity: Optional[Decimal] = None
    tradePrice: Optional[Decimal] = None
    tradeMoney: Optional[Decimal] = None
    proceeds: Optional[Decimal] = None
    taxes: Optional[Decimal] = None
    ibCommission: Optional[Decimal] = None
    ibCommissionCurrency: Optional[str] = None
    netCash: Optional[Decimal] = None
    closePrice: Optional[Decimal] = None
    notes: Tuple[Code, ...] = ()  # separator = ";"
    cost: Optional[Decimal] = None
    fifoPnlRealized: Optional[Decimal] = None
    fxPnl: Optional[Decimal] = None
    mtmPnl: Optional[Decimal] = None
    origTradePrice: Optional[Decimal] = None
    origTradeDate: Optional[datetime.date] = None
    origTradeID: Optional[str] = None
    origOrderID: Optional[str] = None
    clearingFirmID: Optional[str] = None
    transactionID: Optional[str] = None
    openDateTime: Optional[datetime.datetime] = None
    holdingPeriodDateTime: Optional[datetime.datetime] = None
    whenRealized: Optional[datetime.datetime] = None
    whenReopened: Optional[datetime.datetime] = None
    levelOfDetail: Optional[str] = None
    commissionCurrency: Optional[str] = None
    price: Optional[Decimal] = None
    thirdPartyClearingCommission: Optional[Decimal] = None
    orderID: Optional[Decimal] = None
    allocatedTo: Optional[str] = None
    thirdPartyRegulatoryCommission: Optional[Decimal] = None
    dateTime: Optional[datetime.datetime] = None
    brokerExecutionCommission: Optional[Decimal] = None
    thirdPartyExecutionCommission: Optional[Decimal] = None
    amount: Optional[Decimal] = None
    otherCommission: Optional[Decimal] = None
    commission: Optional[Decimal] = None
    brokerClearingCommission: Optional[Decimal] = None
    ibOrderID: Optional[str] = None
    ibExecID: Optional[str] = None
    execID: Optional[str] = None
    brokerageOrderID: Optional[str] = None
    orderReference: Optional[str] = None
    volatilityOrderLink: Optional[str] = None
    exchOrderId: Optional[str] = None
    extExecID: Optional[str] = None
    #  Despite the name, `orderTime` actually contains date/time data.
    orderTime: Optional[datetime.datetime] = None
    changeInPrice: Optional[Decimal] = None
    changeInQuantity: Optional[Decimal] = None
    traderID: Optional[str] = None
    isAPIOrder: Optional[bool] = None
    code: Tuple[Code, ...] = ()
    tax: Optional[Decimal] = None
    listingExchange: Optional[str] = None
    underlyingListingExchange: Optional[str] = None
    settleDate: Optional[str] = None
    underlyingSecurityID: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    accruedInt: Optional[Decimal] = None


@dataclass(frozen=True)
class OptionEAE(FlexElement):
    """Option Exercise Assignment or Expiration

    Wrapped in (identically-named) <OptionEAE>
    """
    transactionType: OptionAction
    accountId: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    assetCategory: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    securityID: Optional[str] = None
    securityIDType: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    underlyingConid: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    issuer: Optional[str] = None
    multiplier: Optional[Decimal] = None
    strike: Optional[Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[str] = None
    principalAdjustFactor: Optional[Decimal] = None
    date: Optional[datetime.date] = None
    quantity: Optional[Decimal] = None
    tradePrice: Optional[Decimal] = None
    markPrice: Optional[Decimal] = None
    proceeds: Optional[Decimal] = None
    commisionsAndTax: Optional[Decimal] = None
    costBasis: Optional[Decimal] = None
    realizedPnl: Optional[Decimal] = None
    fxPnl: Optional[Decimal] = None
    mtmPnl: Optional[Decimal] = None
    tradeID: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None


#  Type alias to work around https://github.com/python/mypy/issues/1775
_OptionEAE = OptionEAE


@dataclass(frozen=True)
class TradeTransfer(FlexElement):
    """ Wrapped in <TradeTransfers> """
    transactionType: TradeType
    openCloseIndicator: OpenClose
    direction: ToFrom
    deliveredReceived: DeliveredReceived
    accountId: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    assetCategory: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    underlyingConid: Optional[str] = None
    tradeID: Optional[str] = None
    reportDate: Optional[datetime.date] = None
    tradeDate: Optional[datetime.date] = None
    tradeTime: Optional[datetime.time] = None
    settleDateTarget: Optional[datetime.date] = None
    exchange: Optional[str] = None
    quantity: Optional[Decimal] = None
    tradePrice: Optional[Decimal] = None
    tradeMoney: Optional[Decimal] = None
    taxes: Optional[Decimal] = None
    ibCommission: Optional[Decimal] = None
    ibCommissionCurrency: Optional[str] = None
    closePrice: Optional[Decimal] = None
    notes: Tuple[Code, ...] = ()  # separator = ";"
    cost: Optional[Decimal] = None
    fifoPnlRealized: Optional[Decimal] = None
    mtmPnl: Optional[Decimal] = None
    brokerName: Optional[str] = None
    brokerAccount: Optional[str] = None
    awayBrokerCommission: Optional[Decimal] = None
    regulatoryFee: Optional[Decimal] = None
    netTradeMoney: Optional[Decimal] = None
    netTradeMoneyInBase: Optional[Decimal] = None
    netTradePrice: Optional[Decimal] = None
    multiplier: Optional[Decimal] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    sedol: Optional[str] = None
    securityID: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    issuer: Optional[str] = None
    strike: Optional[decimal.Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[str] = None
    principalAdjustFactor: Optional[Decimal] = None
    proceeds: Optional[Decimal] = None
    fxPnl: Optional[Decimal] = None
    netCash: Optional[Decimal] = None
    origTradePrice: Optional[Decimal] = None
    # Oddly, `origTradeDate` appears to have hard-coded YYYYMMDD format
    # instead of the date format from the report configuration.
    origTradeDate: Optional[datetime.date] = None
    origTradeID: Optional[str] = None
    origOrderID: Optional[str] = None
    clearingFirmID: Optional[str] = None
    transactionID: Optional[str] = None
    openDateTime: Optional[datetime.datetime] = None
    holdingPeriodDateTime: Optional[datetime.datetime] = None
    whenRealized: Optional[datetime.datetime] = None
    whenReopened: Optional[datetime.datetime] = None
    levelOfDetail: Optional[str] = None
    securityIDType: Optional[str] = None


@dataclass(frozen=True)
class InterestAccrualsCurrency(FlexElement):
    """ Wrapped in <InterestAccruals> """
    accountId: Optional[str] = None
    currency: Optional[str] = None
    fromDate: Optional[datetime.date] = None
    toDate: Optional[datetime.date] = None
    startingAccrualBalance: Optional[Decimal] = None
    interestAccrued: Optional[Decimal] = None
    accrualReversal: Optional[Decimal] = None
    endingAccrualBalance: Optional[Decimal] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    fxTranslation: Optional[Decimal] = None


@dataclass(frozen=True)
class TierInterestDetail(FlexElement):
    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    interestType: Optional[str] = None
    valueDate: Optional[datetime.date] = None
    tierBreak: Optional[str] = None
    balanceThreshold: Optional[Decimal] = None
    securitiesPrincipal: Optional[Decimal] = None
    commoditiesPrincipal: Optional[Decimal] = None
    ibuklPrincipal: Optional[Decimal] = None
    totalPrincipal: Optional[Decimal] = None
    rate: Optional[Decimal] = None
    securitiesInterest: Optional[Decimal] = None
    commoditiesInterest: Optional[Decimal] = None
    ibuklInterest: Optional[Decimal] = None
    totalInterest: Optional[Decimal] = None
    code: Tuple[Code, ...] = ()
    fromAcct: Optional[str] = None
    toAcct: Optional[str] = None


@dataclass(frozen=True)
class HardToBorrowDetail(FlexElement):
    """ Wrapped in <HardToBorrowDetails> """
    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    assetCategory: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    securityID: Optional[str] = None
    securityIDType: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    listingExchange: Optional[str] = None
    underlyingConid: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    underlyingSecurityID: Optional[str] = None
    underlyingListingExchange: Optional[str] = None
    issuer: Optional[str] = None
    multiplier: Optional[Decimal] = None
    strike: Optional[Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[str] = None
    principalAdjustFactor: Optional[Decimal] = None
    valueDate: Optional[datetime.date] = None
    quantity: Optional[Decimal] = None
    price: Optional[Decimal] = None
    value: Optional[Decimal] = None
    borrowFeeRate: Optional[Decimal] = None
    borrowFee: Optional[Decimal] = None
    code: Tuple[Code, ...] = ()
    fromAcct: Optional[str] = None
    toAcct: Optional[str] = None


@dataclass(frozen=True)
class SLBActivity(FlexElement):
    """ Wrapped in <SLBActivities> """
    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    assetCategory: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    securityID: Optional[str] = None
    securityIDType: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    underlyingConid: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    issuer: Optional[str] = None
    multiplier: Optional[Decimal] = None
    strike: Optional[Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[str] = None
    principalAdjustFactor: Optional[Decimal] = None
    date: Optional[datetime.date] = None
    slbTransactionId: Optional[str] = None
    activityDescription: Optional[str] = None
    type: Optional[str] = None
    exchange: Optional[str] = None
    quantity: Optional[Decimal] = None
    feeRate: Optional[Decimal] = None
    collateralAmount: Optional[Decimal] = None
    markQuantity: Optional[Decimal] = None
    markPriorPrice: Optional[Decimal] = None
    markCurrentPrice: Optional[Decimal] = None


@dataclass(frozen=True)
class Transfer(FlexElement):
    """ Wrapped in <Transfers> """
    type: TransferType
    direction: InOut
    accountId: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    assetCategory: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    securityID: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    listingExchange: Optional[str] = None
    underlyingSecurityID: Optional[str] = None
    underlyingListingExchange: Optional[str] = None
    reportDate: Optional[datetime.date] = None
    underlyingConid: Optional[str] = None
    date: Optional[datetime.date] = None
    account: Optional[str] = None
    quantity: Optional[Decimal] = None
    transferPrice: Optional[Decimal] = None
    positionAmount: Optional[Decimal] = None
    positionAmountInBase: Optional[Decimal] = None
    capitalGainsPnl: Optional[Decimal] = None
    cashTransfer: Optional[Decimal] = None
    code: Tuple[Code, ...] = ()
    clientReference: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    sedol: Optional[str] = None
    securityIDType: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    issuer: Optional[str] = None
    multiplier: Optional[decimal.Decimal] = None
    strike: Optional[decimal.Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[str] = None
    principalAdjustFactor: Optional[Decimal] = None
    company: Optional[str] = None
    accountName: Optional[str] = None
    pnlAmount: Optional[Decimal] = None
    pnlAmountInBase: Optional[Decimal] = None
    fxPnl: Optional[Decimal] = None
    transactionID: Optional[str] = None


@dataclass(frozen=True)
class UnsettledTransfer(FlexElement):
    """ Wrapped in <UnsettledTransfers> """
    direction: ToFrom
    accountId: Optional[str] = None
    currency: Optional[str] = None
    assetCategory: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    securityID: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    sedol: Optional[str] = None
    underlyingConid: Optional[str] = None
    stage: Optional[str] = None
    tradeDate: Optional[datetime.date] = None
    targetSettlement: Optional[datetime.date] = None
    contra: Optional[str] = None
    quantity: Optional[Decimal] = None
    tradePrice: Optional[Decimal] = None
    tradeAmount: Optional[Decimal] = None
    tradeAmountInBase: Optional[Decimal] = None
    transactionID: Optional[str] = None


@dataclass(frozen=True)
class PriorPeriodPosition(FlexElement):
    """ Wrapped in <PriorPeriodPositions> """
    accountId: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    assetCategory: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    securityID: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    listingExchange: Optional[str] = None
    underlyingConid: Optional[str] = None
    underlyingSecurityID: Optional[str] = None
    underlyingListingExchange: Optional[str] = None
    priorMtmPnl: Optional[Decimal] = None
    date: Optional[datetime.date] = None
    price: Optional[Decimal] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    sedol: Optional[str] = None
    securityIDType: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    issuer: Optional[str] = None
    multiplier: Optional[decimal.Decimal] = None
    strike: Optional[decimal.Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[str] = None
    principalAdjustFactor: Optional[decimal.Decimal] = None


@dataclass(frozen=True)
class CorporateAction(FlexElement):
    """ Wrapped in <CorporateActions> """
    accountId: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    assetCategory: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    securityID: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    listingExchange: Optional[str] = None
    underlyingConid: Optional[str] = None
    underlyingSecurityID: Optional[str] = None
    underlyingListingExchange: Optional[str] = None
    actionDescription: Optional[str] = None
    dateTime: Optional[datetime.datetime] = None
    amount: Optional[Decimal] = None
    quantity: Optional[Decimal] = None
    fifoPnlRealized: Optional[Decimal] = None
    capitalGainsPnl: Optional[Decimal] = None
    fxPnl: Optional[Decimal] = None
    mtmPnl: Optional[Decimal] = None
    #  Effective 2010, CorporateAction has a `type` attribute
    type: Optional[Reorg] = None
    code: Tuple[Code, ...] = ()
    sedol: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    securityIDType: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    issuer: Optional[str] = None
    multiplier: Optional[Decimal] = None
    strike: Optional[Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[str] = None
    principalAdjustFactor: Optional[Decimal] = None
    reportDate: Optional[datetime.date] = None
    proceeds: Optional[Decimal] = None
    value: Optional[Decimal] = None


@dataclass(frozen=True)
class CashTransaction(FlexElement):
    """ Wrapped in <CashTransactions> """
    type: CashAction
    accountId: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    assetCategory: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    securityID: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    listingExchange: Optional[str] = None
    underlyingConid: Optional[str] = None
    underlyingSecurityID: Optional[str] = None
    underlyingListingExchange: Optional[str] = None
    amount: Optional[Decimal] = None
    dateTime: Optional[datetime.datetime] = None
    sedol: Optional[str] = None
    symbol: Optional[str] = None
    securityIDType: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    issuer: Optional[str] = None
    multiplier: Optional[decimal.Decimal] = None
    strike: Optional[decimal.Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[str] = None
    principalAdjustFactor: Optional[decimal.Decimal] = None
    tradeID: Optional[str] = None
    code: Tuple[Code, ...] = ()
    transactionID: Optional[str] = None
    reportDate: Optional[datetime.date] = None
    clientReference: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None


@dataclass(frozen=True)
class ChangeInDividendAccrual(FlexElement):
    """ Wrapped in <ChangeInDividendAccruals> """
    date: datetime.date
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    accountId: Optional[str] = None
    assetCategory: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    securityID: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    sedol: Optional[str] = None
    listingExchange: Optional[str] = None
    underlyingSecurityID: Optional[str] = None
    underlyingListingExchange: Optional[str] = None
    reportDate: Optional[datetime.date] = None
    underlyingConid: Optional[str] = None
    exDate: Optional[datetime.date] = None
    payDate: Optional[datetime.date] = None
    quantity: Optional[Decimal] = None
    tax: Optional[Decimal] = None
    fee: Optional[Decimal] = None
    grossRate: Optional[Decimal] = None
    grossAmount: Optional[Decimal] = None
    netAmount: Optional[Decimal] = None
    code: Tuple[Code, ...] = ()
    securityIDType: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    issuer: Optional[str] = None
    multiplier: Optional[Decimal] = None
    strike: Optional[Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[str] = None
    principalAdjustFactor: Optional[Decimal] = None
    fromAcct: Optional[str] = None
    toAcct: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None


#  Type alias to work around https://github.com/python/mypy/issues/1775
_ChangeInDividendAccrual = ChangeInDividendAccrual


@dataclass(frozen=True)
class OpenDividendAccrual(FlexElement):
    """ Wrapped in <OpenDividendAccruals> """
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    accountId: Optional[str] = None
    assetCategory: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    securityID: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    underlyingConid: Optional[str] = None
    exDate: Optional[datetime.date] = None
    payDate: Optional[datetime.date] = None
    quantity: Optional[Decimal] = None
    tax: Optional[Decimal] = None
    fee: Optional[Decimal] = None
    grossRate: Optional[Decimal] = None
    grossAmount: Optional[Decimal] = None
    netAmount: Optional[Decimal] = None
    code: Tuple[Code, ...] = ()
    sedol: Optional[str] = None
    securityIDType: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    issuer: Optional[str] = None
    multiplier: Optional[Decimal] = None
    strike: Optional[Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[str] = None
    principalAdjustFactor: Optional[Decimal] = None
    fromAcct: Optional[str] = None
    toAcct: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None


@dataclass(frozen=True)
class SecurityInfo(FlexElement):
    """ Wrapped in <SecuritiesInfo> """
    assetCategory: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    securityID: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    listingExchange: Optional[str] = None
    underlyingSecurityID: Optional[str] = None
    underlyingListingExchange: Optional[str] = None
    underlyingConid: Optional[str] = None
    underlyingCategory: Optional[str] = None
    subCategory: Optional[str] = None
    multiplier: Optional[Decimal] = None
    strike: Optional[Decimal] = None
    expiry: Optional[datetime.date] = None
    maturity: Optional[str] = None
    issueDate: Optional[datetime.date] = None
    type: Optional[str] = None
    sedol: Optional[str] = None
    securityIDType: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    issuer: Optional[str] = None
    putCall: Optional[str] = None
    principalAdjustFactor: Optional[decimal.Decimal] = None
    code: Tuple[Code, ...] = ()


@dataclass(frozen=True)
class ConversionRate(FlexElement):
    """ Wrapped in <ConversionRates> """
    reportDate: Optional[datetime.date] = None
    fromCurrency: Optional[str] = None
    toCurrency: Optional[str] = None
    rate: Optional[Decimal] = None


@dataclass(frozen=True)
class FIFOPerformanceSummaryUnderlying(FlexElement):
    assetCategory: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    securityID: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    underlyingConid: Optional[str] = None
    realizedSTProfit: Optional[Decimal] = None
    realizedSTLoss: Optional[Decimal] = None
    realizedLTProfit: Optional[Decimal] = None
    realizedLTLoss: Optional[Decimal] = None
    totalRealizedPnl: Optional[Decimal] = None
    unrealizedProfit: Optional[Decimal] = None
    unrealizedLoss: Optional[Decimal] = None
    totalUnrealizedPnl: Optional[Decimal] = None
    totalFifoPnl: Optional[Decimal] = None
    sedol: Optional[str] = None
    securityIDType: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    issuer: Optional[str] = None
    unrealizedSTProfit: Optional[decimal.Decimal] = None
    unrealizedSTLoss: Optional[decimal.Decimal] = None
    unrealizedLTProfit: Optional[decimal.Decimal] = None
    unrealizedLTLoss: Optional[decimal.Decimal] = None


@dataclass(frozen=True)
class NetStockPosition(FlexElement):
    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    currency: Optional[str] = None
    assetCategory: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    securityID: Optional[str] = None
    securityIDType: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    sedol: Optional[str] = None
    listingExchange: Optional[str] = None
    underlyingConid: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    underlyingSecurityID: Optional[str] = None
    underlyingListingExchange: Optional[str] = None
    issuer: Optional[str] = None
    multiplier: Optional[Decimal] = None
    strike: Optional[Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[str] = None
    principalAdjustFactor: Optional[Decimal] = None
    reportDate: Optional[datetime.date] = None
    sharesAtIb: Optional[Decimal] = None
    sharesBorrowed: Optional[Decimal] = None
    sharesLent: Optional[Decimal] = None
    netShares: Optional[Decimal] = None


@dataclass(frozen=True)
class ClientFee(FlexElement):
    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    feeType: Optional[str] = None
    date: Optional[datetime.datetime] = None
    description: Optional[str] = None
    expenseIndicator: Optional[str] = None
    revenue: Optional[Decimal] = None
    expense: Optional[Decimal] = None
    net: Optional[Decimal] = None
    revenueInBase: Optional[Decimal] = None
    expenseInBase: Optional[Decimal] = None
    netInBase: Optional[Decimal] = None
    tradeID: Optional[str] = None
    execID: Optional[str] = None
    levelOfDetail: Optional[str] = None


@dataclass(frozen=True)
class ClientFeesDetail(FlexElement):
    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    date: Optional[datetime.datetime] = None
    tradeID: Optional[str] = None
    execID: Optional[str] = None
    totalRevenue: Optional[Decimal] = None
    totalCommission: Optional[Decimal] = None
    brokerExecutionCharge: Optional[Decimal] = None
    clearingCharge: Optional[Decimal] = None
    thirdPartyExecutionCharge: Optional[Decimal] = None
    thirdPartyRegulatoryCharge: Optional[Decimal] = None
    regFINRATradingActivityFee: Optional[Decimal] = None
    regSection31TransactionFee: Optional[Decimal] = None
    regOther: Optional[Decimal] = None
    totalNet: Optional[Decimal] = None
    totalNetInBase: Optional[Decimal] = None
    levelOfDetail: Optional[str] = None
    other: Optional[Decimal] = None


#  Type alias to work around https://github.com/python/mypy/issues/1775
_ClientFeesDetail = ClientFeesDetail
