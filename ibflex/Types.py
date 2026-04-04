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
    SoftDollars
    CFDCharges
    SLBOpenContracts
    HKIPOOpenSubscriptions
    SLBCollaterals
    SLBContract
    SLBOpenContract
"""

__all__ = [
    "FlexElement",
    "FlexQueryResponse",
    "FlexStatement",
    "AccountInformation",
    "ChangeInNAV",
    "MTMPerformanceSummaryUnderlying",
    "EquitySummaryByReportDateInBase",
    "MTDYTDPerformanceSummaryUnderlying",
    "CashReportCurrency",
    "FIFOPerformanceSummaryUnderlying",
    "NetStockPosition",
    "UnsettledTransfer",
    "UnbundledCommissionDetail",
    "StatementOfFundsLine",
    "ChangeInPositionValue",
    "OpenPosition",
    "FxLot",
    "Trade",
    "TradeConfirm",
    "OptionEAE",
    "TradeTransfer",
    "TierInterestDetail",
    "HardToBorrowDetail",
    "InterestAccrualsCurrency",
    "SLBActivity",
    "Transfer",
    "CorporateAction",
    "CashTransaction",
    "ChangeInDividendAccrual",
    "OpenDividendAccrual",
    "SecurityInfo",
    "ConversionRate",
    "PriorPeriodPosition",
    "ClientFee",
    "ClientFeesDetail",
    "SalesTax",
    "DebitCardActivity",
    "SymbolSummary",
    "Order",
    "AssetSummary",
    "SLBContract",
    "SLBOpenContract",
]


import datetime
import decimal
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Tuple

from ibflex import enums


@dataclass(frozen=True)
class FlexElement:
    """Base class for data element types"""


@dataclass(frozen=True)
class FlexQueryResponse(FlexElement):
    """Root element"""

    queryName: str
    type: str
    FlexStatements: Tuple["FlexStatement", ...]

    def __repr__(self):
        repr = (
            f"{type(self).__name__}("
            f"queryName={self.queryName!r}, "
            f"type={self.type!r}, "
            f"len(FlexStatements)={len(self.FlexStatements)}"
            ")"
        )
        return repr


@dataclass(frozen=True)
class FlexStatement(FlexElement):
    """Wrapped in <FlexStatements>"""

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
    DebitCardActivities: Tuple["DebitCardActivity", ...] = ()
    SoftDollars: Tuple = ()  # TODO
    CashTransactions: Tuple["CashTransaction", ...] = ()
    SalesTaxes: Tuple["SalesTax", ...] = ()
    CFDCharges: Tuple = ()  # TODO
    InterestAccruals: Tuple["InterestAccrualsCurrency", ...] = ()
    TierInterestDetails: Tuple["TierInterestDetail", ...] = ()
    HardToBorrowDetails: Tuple["HardToBorrowDetail", ...] = ()
    HardToBorrowMarkupDetails: Tuple = ()
    SLBOpenContracts: Tuple = ()  # TODO
    SLBActivities: Tuple["SLBActivity", ...] = ()
    SLBFees: Tuple["SLBFee", ...] = ()
    Transfers: Tuple["Transfer", ...] = ()
    ChangeInDividendAccruals: Tuple["_ChangeInDividendAccrual", ...] = ()
    OpenDividendAccruals: Tuple["OpenDividendAccrual", ...] = ()
    SecuritiesInfo: Tuple["SecurityInfo", ...] = ()
    ConversionRates: Tuple["ConversionRate", ...] = ()
    HKIPOOpenSubscriptions: Tuple = ()  # TODO
    CommissionCredits: Tuple = ()  # TODO
    StockGrantActivities: Tuple = ()  # TODO
    SLBCollaterals: Tuple = ()  # TODO
    IncentiveCouponAccrualDetails: Tuple = ()  # TODO
    DepositsOnHold: Tuple = ()  # TODO

    def __repr__(self):
        repr = (
            f"{type(self).__name__}("
            f"accountId={self.accountId!r}, "
            f"fromDate={self.fromDate!r}, "
            f"toDate={self.toDate!r}, "
            f"period={self.period!r}, "
            f"whenGenerated={self.whenGenerated!r}"
        )

        sequences = (
            (k, getattr(self, k))
            for k, v in self.__annotations__.items()
            if hasattr(v, "__origin__") and v.__origin__ is tuple
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
    """Child of <FlexStatement>"""

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
    accountRepName: Optional[str] = None
    accountRepPhone: Optional[str] = None


#  Type alias to work around https://github.com/python/mypy/issues/1775
_AccountInformation = AccountInformation


@dataclass(frozen=True)
class ChangeInNAV(FlexElement):
    """Child of <FlexStatement>"""

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
    brokerFees: Optional[Decimal] = None
    changeInBrokerFeeAccruals: Optional[Decimal] = None
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
    commissionCreditsRedemption: Optional[Decimal] = None
    grantActivity: Optional[Decimal] = None
    excessFundSweep: Optional[Decimal] = None
    billableSalesTax: Optional[Decimal] = None


#  Type alias to work around https://github.com/python/mypy/issues/1775
_ChangeInNAV = ChangeInNAV


@dataclass(frozen=True)
class MTMPerformanceSummaryUnderlying(FlexElement):
    """Wrapped in <MTMPerformanceSummaryInBase>"""

    assetCategory: Optional[enums.AssetClass] = None
    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
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
    putCall: Optional[enums.PutCall] = None
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
    code: Tuple[enums.Code, ...] = ()
    corpActionMtm: Optional[Decimal] = None
    dividends: Optional[Decimal] = None
    serialNumber: Optional[str] = None
    deliveryType: Optional[str] = None
    commodityType: Optional[str] = None
    fineness: Optional[decimal.Decimal] = None
    weight: Optional[str] = None
    otherWithAccruals: Optional[decimal.Decimal] = None
    totalWithAccruals: Optional[decimal.Decimal] = None


@dataclass(frozen=True)
class EquitySummaryByReportDateInBase(FlexElement):
    """Wrapped in <EquitySummaryInBase>"""

    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    reportDate: Optional[datetime.date] = None
    cash: Optional[decimal.Decimal] = None
    cashLong: Optional[decimal.Decimal] = None
    cashShort: Optional[decimal.Decimal] = None
    slbCashCollateral: Optional[decimal.Decimal] = None
    slbCashCollateralLong: Optional[decimal.Decimal] = None
    slbCashCollateralShort: Optional[decimal.Decimal] = None
    stock: Optional[decimal.Decimal] = None
    stockLong: Optional[decimal.Decimal] = None
    stockShort: Optional[decimal.Decimal] = None
    slbDirectSecuritiesBorrowed: Optional[decimal.Decimal] = None
    slbDirectSecuritiesBorrowedLong: Optional[decimal.Decimal] = None
    slbDirectSecuritiesBorrowedShort: Optional[decimal.Decimal] = None
    slbDirectSecuritiesLent: Optional[decimal.Decimal] = None
    slbDirectSecuritiesLentLong: Optional[decimal.Decimal] = None
    slbDirectSecuritiesLentShort: Optional[decimal.Decimal] = None
    options: Optional[decimal.Decimal] = None
    optionsLong: Optional[decimal.Decimal] = None
    optionsShort: Optional[decimal.Decimal] = None
    bonds: Optional[decimal.Decimal] = None
    bondsLong: Optional[decimal.Decimal] = None
    bondsShort: Optional[decimal.Decimal] = None
    bondInterestAccrualsComponent: Optional[decimal.Decimal] = None
    bondInterestAccrualsComponentLong: Optional[decimal.Decimal] = None
    bondInterestAccrualsComponentShort: Optional[decimal.Decimal] = None
    notes: Optional[decimal.Decimal] = None
    notesLong: Optional[decimal.Decimal] = None
    notesShort: Optional[decimal.Decimal] = None
    interestAccruals: Optional[decimal.Decimal] = None
    interestAccrualsLong: Optional[decimal.Decimal] = None
    interestAccrualsShort: Optional[decimal.Decimal] = None
    softDollars: Optional[decimal.Decimal] = None
    softDollarsLong: Optional[decimal.Decimal] = None
    softDollarsShort: Optional[decimal.Decimal] = None
    dividendAccruals: Optional[decimal.Decimal] = None
    dividendAccrualsLong: Optional[decimal.Decimal] = None
    dividendAccrualsShort: Optional[decimal.Decimal] = None
    total: Optional[decimal.Decimal] = None
    totalLong: Optional[decimal.Decimal] = None
    totalShort: Optional[decimal.Decimal] = None
    commodities: Optional[decimal.Decimal] = None
    commoditiesLong: Optional[decimal.Decimal] = None
    commoditiesShort: Optional[decimal.Decimal] = None
    funds: Optional[decimal.Decimal] = None
    fundsLong: Optional[decimal.Decimal] = None
    fundsShort: Optional[decimal.Decimal] = None
    forexCfdUnrealizedPl: Optional[decimal.Decimal] = None
    forexCfdUnrealizedPlLong: Optional[decimal.Decimal] = None
    forexCfdUnrealizedPlShort: Optional[decimal.Decimal] = None
    brokerInterestAccrualsComponent: Optional[decimal.Decimal] = None
    brokerCashComponent: Optional[decimal.Decimal] = None
    brokerFeesAccrualsComponent: Optional[decimal.Decimal] = None
    brokerFeesAccrualsComponentLong: Optional[decimal.Decimal] = None
    brokerFeesAccrualsComponentShort: Optional[decimal.Decimal] = None
    cfdUnrealizedPl: Optional[decimal.Decimal] = None
    fdicInsuredBankSweepAccount: Optional[decimal.Decimal] = None
    fdicInsuredBankSweepAccountLong: Optional[decimal.Decimal] = None
    fdicInsuredBankSweepAccountShort: Optional[decimal.Decimal] = None
    fdicInsuredBankSweepAccountCashComponent: Optional[decimal.Decimal] = None
    fdicInsuredBankSweepAccountCashComponentLong: Optional[decimal.Decimal] = None
    fdicInsuredBankSweepAccountCashComponentShort: Optional[decimal.Decimal] = None
    fdicInsuredAccountInterestAccruals: Optional[decimal.Decimal] = None
    fdicInsuredAccountInterestAccrualsLong: Optional[decimal.Decimal] = None
    fdicInsuredAccountInterestAccrualsShort: Optional[decimal.Decimal] = None
    fdicInsuredAccountInterestAccrualsComponent: Optional[decimal.Decimal] = None
    fdicInsuredAccountInterestAccrualsComponentLong: Optional[decimal.Decimal] = None
    fdicInsuredAccountInterestAccrualsComponentShort: Optional[decimal.Decimal] = None
    brokerCashComponentLong: Optional[decimal.Decimal] = None
    brokerCashComponentShort: Optional[decimal.Decimal] = None
    brokerInterestAccrualsComponentLong: Optional[decimal.Decimal] = None
    brokerInterestAccrualsComponentShort: Optional[decimal.Decimal] = None
    cfdUnrealizedPlLong: Optional[decimal.Decimal] = None
    cfdUnrealizedPlShort: Optional[decimal.Decimal] = None
    ipoSubscription: Optional[decimal.Decimal] = None
    ipoSubscriptionLong: Optional[decimal.Decimal] = None
    ipoSubscriptionShort: Optional[decimal.Decimal] = None
    physDel: Optional[decimal.Decimal] = None
    physDelLong: Optional[decimal.Decimal] = None
    physDelShort: Optional[decimal.Decimal] = None


@dataclass(frozen=True)
class MTDYTDPerformanceSummaryUnderlying(FlexElement):
    """Wrapped in <MTDYTDPerformanceSummary>"""

    assetCategory: Optional[enums.AssetClass] = None
    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
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
    putCall: Optional[enums.PutCall] = None
    principalAdjustFactor: Optional[Decimal] = None
    realizedPnlMTD: Optional[Decimal] = None
    realizedCapitalGainsPnlMTD: Optional[Decimal] = None
    realizedFxPnlMTD: Optional[Decimal] = None
    realizedPnlYTD: Optional[Decimal] = None
    realizedCapitalGainsPnlYTD: Optional[Decimal] = None
    realizedFxPnlYTD: Optional[Decimal] = None
    brokerFees: Optional[decimal.Decimal] = None
    brokerFeesSec: Optional[decimal.Decimal] = None
    brokerFeesCom: Optional[decimal.Decimal] = None
    brokerFeesMTD: Optional[decimal.Decimal] = None
    brokerFeesYTD: Optional[decimal.Decimal] = None
    serialNumber: Optional[str] = None
    deliveryType: Optional[str] = None
    commodityType: Optional[str] = None
    fineness: Optional[decimal.Decimal] = None
    weight: Optional[str] = None


@dataclass(frozen=True)
class CashReportCurrency(FlexElement):
    """Wrapped in <CashReport>"""

    accountId: Optional[str] = None
    currency: Optional[str] = None
    fromDate: Optional[datetime.date] = None
    toDate: Optional[datetime.date] = None
    startingCash: Optional[decimal.Decimal] = None
    startingCashSec: Optional[decimal.Decimal] = None
    startingCashCom: Optional[decimal.Decimal] = None
    clientFees: Optional[decimal.Decimal] = None
    clientFeesSec: Optional[decimal.Decimal] = None
    clientFeesCom: Optional[decimal.Decimal] = None
    commissions: Optional[decimal.Decimal] = None
    commissionsSec: Optional[decimal.Decimal] = None
    commissionsCom: Optional[decimal.Decimal] = None
    billableCommissions: Optional[decimal.Decimal] = None
    billableCommissionsSec: Optional[decimal.Decimal] = None
    billableCommissionsCom: Optional[decimal.Decimal] = None
    depositWithdrawals: Optional[decimal.Decimal] = None
    depositWithdrawalsSec: Optional[decimal.Decimal] = None
    depositWithdrawalsCom: Optional[decimal.Decimal] = None
    deposits: Optional[decimal.Decimal] = None
    depositsSec: Optional[decimal.Decimal] = None
    depositsCom: Optional[decimal.Decimal] = None
    withdrawals: Optional[decimal.Decimal] = None
    withdrawalsSec: Optional[decimal.Decimal] = None
    withdrawalsCom: Optional[decimal.Decimal] = None
    accountTransfers: Optional[decimal.Decimal] = None
    accountTransfersSec: Optional[decimal.Decimal] = None
    accountTransfersCom: Optional[decimal.Decimal] = None
    internalTransfers: Optional[decimal.Decimal] = None
    internalTransfersSec: Optional[decimal.Decimal] = None
    internalTransfersCom: Optional[decimal.Decimal] = None
    dividends: Optional[decimal.Decimal] = None
    dividendsSec: Optional[decimal.Decimal] = None
    dividendsCom: Optional[decimal.Decimal] = None
    brokerFees: Optional[decimal.Decimal] = None
    brokerFeesSec: Optional[decimal.Decimal] = None
    brokerFeesCom: Optional[decimal.Decimal] = None
    brokerFeesMTD: Optional[decimal.Decimal] = None
    brokerFeesYTD: Optional[decimal.Decimal] = None
    brokerInterest: Optional[decimal.Decimal] = None
    brokerInterestSec: Optional[decimal.Decimal] = None
    brokerInterestCom: Optional[decimal.Decimal] = None
    bondInterest: Optional[decimal.Decimal] = None
    bondInterestSec: Optional[decimal.Decimal] = None
    bondInterestCom: Optional[decimal.Decimal] = None
    cashSettlingMtm: Optional[decimal.Decimal] = None
    cashSettlingMtmSec: Optional[decimal.Decimal] = None
    cashSettlingMtmCom: Optional[decimal.Decimal] = None
    cfdCharges: Optional[decimal.Decimal] = None
    cfdChargesSec: Optional[decimal.Decimal] = None
    cfdChargesCom: Optional[decimal.Decimal] = None
    netTradesSales: Optional[decimal.Decimal] = None
    netTradesSalesSec: Optional[decimal.Decimal] = None
    netTradesSalesCom: Optional[decimal.Decimal] = None
    netTradesPurchases: Optional[decimal.Decimal] = None
    netTradesPurchasesSec: Optional[decimal.Decimal] = None
    netTradesPurchasesCom: Optional[decimal.Decimal] = None
    feesReceivables: Optional[decimal.Decimal] = None
    feesReceivablesSec: Optional[decimal.Decimal] = None
    feesReceivablesCom: Optional[decimal.Decimal] = None
    paymentInLieu: Optional[decimal.Decimal] = None
    paymentInLieuSec: Optional[decimal.Decimal] = None
    paymentInLieuCom: Optional[decimal.Decimal] = None
    transactionTax: Optional[decimal.Decimal] = None
    transactionTaxSec: Optional[decimal.Decimal] = None
    transactionTaxCom: Optional[decimal.Decimal] = None
    withholdingTax: Optional[decimal.Decimal] = None
    withholdingTaxSec: Optional[decimal.Decimal] = None
    withholdingTaxCom: Optional[decimal.Decimal] = None
    fxTranslationGainLoss: Optional[decimal.Decimal] = None
    fxTranslationGainLossSec: Optional[decimal.Decimal] = None
    fxTranslationGainLossCom: Optional[decimal.Decimal] = None
    otherFees: Optional[decimal.Decimal] = None
    otherFeesSec: Optional[decimal.Decimal] = None
    otherFeesCom: Optional[decimal.Decimal] = None
    endingCash: Optional[decimal.Decimal] = None
    endingCashSec: Optional[decimal.Decimal] = None
    endingCashCom: Optional[decimal.Decimal] = None
    endingSettledCash: Optional[decimal.Decimal] = None
    endingSettledCashSec: Optional[decimal.Decimal] = None
    endingSettledCashCom: Optional[decimal.Decimal] = None
    endingCashIBUKL: Optional[decimal.Decimal] = None
    clientFeesMTD: Optional[decimal.Decimal] = None
    clientFeesYTD: Optional[decimal.Decimal] = None
    commissionsMTD: Optional[decimal.Decimal] = None
    commissionsYTD: Optional[decimal.Decimal] = None
    billableCommissionsMTD: Optional[decimal.Decimal] = None
    billableCommissionsYTD: Optional[decimal.Decimal] = None
    depositWithdrawalsMTD: Optional[decimal.Decimal] = None
    depositWithdrawalsYTD: Optional[decimal.Decimal] = None
    depositsMTD: Optional[decimal.Decimal] = None
    depositsYTD: Optional[decimal.Decimal] = None
    withdrawalsMTD: Optional[decimal.Decimal] = None
    withdrawalsYTD: Optional[decimal.Decimal] = None
    accountTransfersMTD: Optional[decimal.Decimal] = None
    accountTransfersYTD: Optional[decimal.Decimal] = None
    internalTransfersMTD: Optional[decimal.Decimal] = None
    internalTransfersYTD: Optional[decimal.Decimal] = None
    excessFundSweep: Optional[decimal.Decimal] = None
    excessFundSweepSec: Optional[decimal.Decimal] = None
    excessFundSweepCom: Optional[decimal.Decimal] = None
    excessFundSweepMTD: Optional[decimal.Decimal] = None
    excessFundSweepYTD: Optional[decimal.Decimal] = None
    dividendsMTD: Optional[decimal.Decimal] = None
    dividendsYTD: Optional[decimal.Decimal] = None
    insuredDepositInterestMTD: Optional[decimal.Decimal] = None
    insuredDepositInterestYTD: Optional[decimal.Decimal] = None
    brokerInterestMTD: Optional[decimal.Decimal] = None
    brokerInterestYTD: Optional[decimal.Decimal] = None
    bondInterestMTD: Optional[decimal.Decimal] = None
    bondInterestYTD: Optional[decimal.Decimal] = None
    cashSettlingMtmMTD: Optional[decimal.Decimal] = None
    cashSettlingMtmYTD: Optional[decimal.Decimal] = None
    realizedVmMTD: Optional[decimal.Decimal] = None
    realizedVmYTD: Optional[decimal.Decimal] = None
    cfdChargesMTD: Optional[decimal.Decimal] = None
    cfdChargesYTD: Optional[decimal.Decimal] = None
    netTradesSalesMTD: Optional[decimal.Decimal] = None
    netTradesSalesYTD: Optional[decimal.Decimal] = None
    advisorFeesMTD: Optional[decimal.Decimal] = None
    advisorFeesYTD: Optional[decimal.Decimal] = None
    feesReceivablesMTD: Optional[decimal.Decimal] = None
    feesReceivablesYTD: Optional[decimal.Decimal] = None
    netTradesPurchasesMTD: Optional[decimal.Decimal] = None
    netTradesPurchasesYTD: Optional[decimal.Decimal] = None
    paymentInLieuMTD: Optional[decimal.Decimal] = None
    paymentInLieuYTD: Optional[decimal.Decimal] = None
    transactionTaxMTD: Optional[decimal.Decimal] = None
    transactionTaxYTD: Optional[decimal.Decimal] = None
    taxReceivablesMTD: Optional[decimal.Decimal] = None
    taxReceivablesYTD: Optional[decimal.Decimal] = None
    withholdingTaxMTD: Optional[decimal.Decimal] = None
    withholdingTaxYTD: Optional[decimal.Decimal] = None
    withholding871mMTD: Optional[decimal.Decimal] = None
    withholding871mYTD: Optional[decimal.Decimal] = None
    withholdingCollectedTaxMTD: Optional[decimal.Decimal] = None
    withholdingCollectedTaxYTD: Optional[decimal.Decimal] = None
    salesTaxMTD: Optional[decimal.Decimal] = None
    salesTaxYTD: Optional[decimal.Decimal] = None
    otherFeesMTD: Optional[decimal.Decimal] = None
    otherFeesYTD: Optional[decimal.Decimal] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    avgCreditBalance: Optional[decimal.Decimal] = None
    avgCreditBalanceSec: Optional[decimal.Decimal] = None
    avgCreditBalanceCom: Optional[decimal.Decimal] = None
    avgDebitBalance: Optional[decimal.Decimal] = None
    avgDebitBalanceSec: Optional[decimal.Decimal] = None
    avgDebitBalanceCom: Optional[decimal.Decimal] = None
    linkingAdjustments: Optional[decimal.Decimal] = None
    linkingAdjustmentsSec: Optional[decimal.Decimal] = None
    linkingAdjustmentsCom: Optional[decimal.Decimal] = None
    insuredDepositInterest: Optional[decimal.Decimal] = None
    insuredDepositInterestSec: Optional[decimal.Decimal] = None
    insuredDepositInterestCom: Optional[decimal.Decimal] = None
    realizedVm: Optional[decimal.Decimal] = None
    realizedVmSec: Optional[decimal.Decimal] = None
    realizedVmCom: Optional[decimal.Decimal] = None
    advisorFees: Optional[decimal.Decimal] = None
    advisorFeesSec: Optional[decimal.Decimal] = None
    advisorFeesCom: Optional[decimal.Decimal] = None
    taxReceivables: Optional[decimal.Decimal] = None
    taxReceivablesSec: Optional[decimal.Decimal] = None
    taxReceivablesCom: Optional[decimal.Decimal] = None
    withholding871m: Optional[decimal.Decimal] = None
    withholding871mSec: Optional[decimal.Decimal] = None
    withholding871mCom: Optional[decimal.Decimal] = None
    withholdingCollectedTax: Optional[decimal.Decimal] = None
    withholdingCollectedTaxSec: Optional[decimal.Decimal] = None
    withholdingCollectedTaxCom: Optional[decimal.Decimal] = None
    salesTax: Optional[decimal.Decimal] = None
    salesTaxSec: Optional[decimal.Decimal] = None
    salesTaxCom: Optional[decimal.Decimal] = None
    other: Optional[decimal.Decimal] = None
    otherSec: Optional[decimal.Decimal] = None
    otherCom: Optional[decimal.Decimal] = None
    levelOfDetail: Optional[str] = None
    debitCardActivity: Optional[decimal.Decimal] = None
    debitCardActivitySec: Optional[decimal.Decimal] = None
    debitCardActivityCom: Optional[decimal.Decimal] = None
    debitCardActivityMTD: Optional[decimal.Decimal] = None
    debitCardActivityYTD: Optional[decimal.Decimal] = None
    billPay: Optional[decimal.Decimal] = None
    billPaySec: Optional[decimal.Decimal] = None
    billPayCom: Optional[decimal.Decimal] = None
    billPayMTD: Optional[decimal.Decimal] = None
    billPayYTD: Optional[decimal.Decimal] = None
    realizedForexVm: Optional[decimal.Decimal] = None
    realizedForexVmSec: Optional[decimal.Decimal] = None
    realizedForexVmCom: Optional[decimal.Decimal] = None
    realizedForexVmMTD: Optional[decimal.Decimal] = None
    realizedForexVmYTD: Optional[decimal.Decimal] = None
    ipoSubscription: Optional[decimal.Decimal] = None
    ipoSubscriptionSec: Optional[decimal.Decimal] = None
    ipoSubscriptionCom: Optional[decimal.Decimal] = None
    ipoSubscriptionMTD: Optional[decimal.Decimal] = None
    ipoSubscriptionYTD: Optional[decimal.Decimal] = None
    billableSalesTax: Optional[decimal.Decimal] = None
    billableSalesTaxSec: Optional[decimal.Decimal] = None
    billableSalesTaxCom: Optional[decimal.Decimal] = None
    billableSalesTaxMTD: Optional[decimal.Decimal] = None
    billableSalesTaxYTD: Optional[decimal.Decimal] = None
    commissionCreditsRedemption: Optional[decimal.Decimal] = None
    commissionCreditsRedemptionSec: Optional[decimal.Decimal] = None
    commissionCreditsRedemptionCom: Optional[decimal.Decimal] = None
    commissionCreditsRedemptionMTD: Optional[decimal.Decimal] = None
    commissionCreditsRedemptionYTD: Optional[decimal.Decimal] = None
    referralFee: Optional[decimal.Decimal] = None
    referralFeeSec: Optional[decimal.Decimal] = None
    referralFeeCom: Optional[decimal.Decimal] = None
    referralFeeMTD: Optional[decimal.Decimal] = None
    referralFeeYTD: Optional[decimal.Decimal] = None
    carbonCredits: Optional[decimal.Decimal] = None
    carbonCreditsSec: Optional[decimal.Decimal] = None
    carbonCreditsCom: Optional[decimal.Decimal] = None
    carbonCreditsMTD: Optional[decimal.Decimal] = None
    carbonCreditsYTD: Optional[decimal.Decimal] = None
    donations: Optional[decimal.Decimal] = None
    donationsSec: Optional[decimal.Decimal] = None
    donationsCom: Optional[decimal.Decimal] = None
    donationsMTD: Optional[decimal.Decimal] = None
    donationsYTD: Optional[decimal.Decimal] = None
    paxosTransfers: Optional[decimal.Decimal] = None
    paxosTransfersSec: Optional[decimal.Decimal] = None
    paxosTransfersCom: Optional[decimal.Decimal] = None
    paxosTransfersMTD: Optional[decimal.Decimal] = None
    paxosTransfersYTD: Optional[decimal.Decimal] = None
    slbStartingCashCollateral: Optional[decimal.Decimal] = None
    slbStartingCashCollateralSec: Optional[decimal.Decimal] = None
    slbStartingCashCollateralCom: Optional[decimal.Decimal] = None
    slbNetSecuritiesLentActivity: Optional[decimal.Decimal] = None
    slbNetSecuritiesLentActivityCom: Optional[decimal.Decimal] = None
    slbNetSecuritiesLentActivitySec: Optional[decimal.Decimal] = None
    slbEndingCashCollateral: Optional[decimal.Decimal] = None
    slbEndingCashCollateralSec: Optional[decimal.Decimal] = None
    slbEndingCashCollateralCom: Optional[decimal.Decimal] = None
    slbNetCash: Optional[decimal.Decimal] = None
    slbNetCashSec: Optional[decimal.Decimal] = None
    slbNetCashCom: Optional[decimal.Decimal] = None
    slbNetSettledCash: Optional[decimal.Decimal] = None
    slbNetSettledCashSec: Optional[decimal.Decimal] = None
    slbNetSettledCashCom: Optional[decimal.Decimal] = None


@dataclass(frozen=True)
class StatementOfFundsLine(FlexElement):
    """Wrapped in <StmtFunds>"""

    assetCategory: Optional[enums.AssetClass] = None
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
    putCall: Optional[enums.PutCall] = None
    principalAdjustFactor: Optional[decimal.Decimal] = None
    fxRateToBase: Optional[Decimal] = None
    listingExchange: Optional[str] = None
    underlyingSecurityID: Optional[str] = None
    underlyingListingExchange: Optional[str] = None
    settleDate: Optional[datetime.date] = None
    activityCode: Optional[str] = None  # FIXME
    orderID: Optional[str] = None
    tradeQuantity: Optional[Decimal] = None
    tradePrice: Optional[Decimal] = None
    tradeGross: Optional[Decimal] = None
    tradeCommission: Optional[Decimal] = None
    tradeTax: Optional[Decimal] = None
    tradeCode: Optional[str] = None
    levelOfDetail: Optional[str] = None
    transactionID: Optional[str] = None
    serialNumber: Optional[str] = None
    deliveryType: Optional[str] = None
    commodityType: Optional[str] = None
    fineness: Optional[decimal.Decimal] = None
    weight: Optional[str] = None


@dataclass(frozen=True)
class ChangeInPositionValue(FlexElement):
    """Wrapped in <ChangeInPositionValues>"""

    assetCategory: Optional[enums.AssetClass] = None
    currency: Optional[str] = None
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
    """Wrapped in <OpenPositions>"""

    side: Optional[enums.LongShort] = None
    assetCategory: Optional[enums.AssetClass] = None
    accountId: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[decimal.Decimal] = None
    reportDate: Optional[datetime.date] = None
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
    code: Tuple[enums.Code, ...] = ()
    originatingOrderID: Optional[str] = None
    originatingTransactionID: Optional[str] = None
    accruedInt: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    sedol: Optional[str] = None
    percentOfNAV: Optional[decimal.Decimal] = None
    strike: Optional[decimal.Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[enums.PutCall] = None
    principalAdjustFactor: Optional[decimal.Decimal] = None
    listingExchange: Optional[str] = None
    underlyingSecurityID: Optional[str] = None
    underlyingListingExchange: Optional[str] = None
    positionValueInBase: Optional[Decimal] = None
    unrealizedCapitalGainsPnl: Optional[Decimal] = None
    unrealizedlFxPnl: Optional[Decimal] = None
    vestingDate: Optional[datetime.date] = None
    serialNumber: Optional[str] = None
    deliveryType: Optional[str] = None
    commodityType: Optional[str] = None
    fineness: Optional[decimal.Decimal] = None
    weight: Optional[str] = None


@dataclass(frozen=True)
class FxLot(FlexElement):
    """Wrapped in <FxLots>, which in turn is wrapped in <FxPositions>"""

    assetCategory: Optional[enums.AssetClass] = None
    accountId: Optional[str] = None
    reportDate: Optional[datetime.date] = None
    functionalCurrency: Optional[str] = None
    fxCurrency: Optional[str] = None
    quantity: Optional[Decimal] = None
    costPrice: Optional[Decimal] = None
    costBasis: Optional[Decimal] = None
    closePrice: Optional[Decimal] = None
    value: Optional[Decimal] = None
    unrealizedPL: Optional[Decimal] = None
    code: Tuple[enums.Code, ...] = ()
    lotDescription: Optional[str] = None
    lotOpenDateTime: Optional[datetime.datetime] = None
    levelOfDetail: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None


@dataclass(frozen=True)
class Trade(FlexElement):
    """Wrapped in <Trades>"""

    transactionType: Optional[enums.TradeType] = None
    openCloseIndicator: Optional[enums.OpenClose] = None
    buySell: Optional[enums.BuySell] = None
    orderType: Optional[enums.OrderType] = None
    assetCategory: Optional[enums.AssetClass] = None
    accountId: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    listingExchange: Optional[str] = None
    multiplier: Optional[Decimal] = None
    strike: Optional[Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[enums.PutCall] = None
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
    notes: Tuple[enums.Code, ...] = ()  # separator = ";"
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
    accruedInt: Optional[Decimal] = None
    serialNumber: Optional[str] = None
    deliveryType: Optional[str] = None
    commodityType: Optional[str] = None
    fineness: Optional[decimal.Decimal] = None
    weight: Optional[str] = None
    relatedTradeID: Optional[str] = None
    relatedTransactionID: Optional[str] = None


@dataclass(frozen=True)
class Lot(FlexElement):
    """Wrapped in <Trades>"""

    transactionType: Optional[enums.TradeType] = None
    openCloseIndicator: Optional[enums.OpenClose] = None
    buySell: Optional[enums.BuySell] = None
    orderType: Optional[enums.OrderType] = None
    assetCategory: Optional[enums.AssetClass] = None
    accountId: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    listingExchange: Optional[str] = None
    multiplier: Optional[Decimal] = None
    strike: Optional[Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[enums.PutCall] = None
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
    notes: Tuple[enums.Code, ...] = ()  # separator = ";"
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
    accruedInt: Optional[decimal.Decimal] = None
    serialNumber: Optional[str] = None
    deliveryType: Optional[str] = None
    commodityType: Optional[str] = None
    fineness: Optional[decimal.Decimal] = None
    weight: Optional[str] = None


@dataclass(frozen=True)
class UnbundledCommissionDetail(FlexElement):
    """Wrapped in <UnbundledCommissionDetails>"""

    buySell: Optional[enums.BuySell] = None
    assetCategory: Optional[enums.AssetClass] = None
    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
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
    putCall: Optional[enums.PutCall] = None
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
class SymbolSummary(FlexElement):
    """Wrapped in <TradeConfirms>"""

    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    currency: Optional[str] = None
    assetCategory: Optional[enums.AssetClass] = None
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
    putCall: Optional[enums.PutCall] = None
    principalAdjustFactor: Optional[Decimal] = None
    transactionType: Optional[enums.TradeType] = None
    tradeID: Optional[str] = None
    orderID: Optional[Decimal] = None
    execID: Optional[str] = None
    brokerageOrderID: Optional[str] = None
    orderReference: Optional[str] = None
    volatilityOrderLink: Optional[str] = None
    clearingFirmID: Optional[str] = None
    origTradePrice: Optional[Decimal] = None
    origTradeDate: Optional[datetime.date] = None
    origTradeID: Optional[str] = None
    #  Despite the name, `orderTime` actually contains date/time data.
    orderTime: Optional[datetime.datetime] = None
    dateTime: Optional[datetime.datetime] = None
    reportDate: Optional[datetime.date] = None
    settleDate: Optional[datetime.date] = None
    tradeDate: Optional[datetime.date] = None
    exchange: Optional[str] = None
    buySell: Optional[enums.BuySell] = None
    quantity: Optional[Decimal] = None
    price: Optional[Decimal] = None
    amount: Optional[Decimal] = None
    proceeds: Optional[Decimal] = None
    commission: Optional[Decimal] = None
    brokerExecutionCommission: Optional[Decimal] = None
    brokerClearingCommission: Optional[Decimal] = None
    thirdPartyExecutionCommission: Optional[Decimal] = None
    thirdPartyClearingCommission: Optional[Decimal] = None
    thirdPartyRegulatoryCommission: Optional[Decimal] = None
    otherCommission: Optional[Decimal] = None
    commissionCurrency: Optional[str] = None
    tax: Optional[Decimal] = None
    code: Tuple[enums.Code, ...] = ()
    orderType: Optional[enums.OrderType] = None
    levelOfDetail: Optional[str] = None
    traderID: Optional[str] = None
    isAPIOrder: Optional[bool] = None
    allocatedTo: Optional[str] = None
    accruedInt: Optional[Decimal] = None


@dataclass(frozen=True)
class AssetSummary(FlexElement):
    """Wrapped in <TradeConfirms>"""

    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    currency: Optional[str] = None
    assetCategory: Optional[enums.AssetClass] = None
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
    multiplier: Optional[decimal.Decimal] = None
    strike: Optional[decimal.Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[enums.PutCall] = None
    principalAdjustFactor: Optional[decimal.Decimal] = None
    transactionType: Optional[enums.TradeType] = None
    tradeID: Optional[str] = None
    orderID: Optional[decimal.Decimal] = None
    execID: Optional[str] = None
    brokerageOrderID: Optional[str] = None
    orderReference: Optional[str] = None
    volatilityOrderLink: Optional[str] = None
    clearingFirmID: Optional[str] = None
    origTradePrice: Optional[decimal.Decimal] = None
    TradePrice: Optional[decimal.Decimal] = None
    tradeMoney: Optional[decimal.Decimal] = None
    taxes: Optional[decimal.Decimal] = None
    origTradeDate: Optional[datetime.date] = None
    origTradeID: Optional[str] = None
    tradePrice: Optional[decimal.Decimal] = None
    #  Despite the name, `orderTime` actually contains date/time data.
    orderTime: Optional[datetime.datetime] = None
    exchOrderId: Optional[str] = None
    dateTime: Optional[datetime.datetime] = None
    fxRateToBase: Optional[decimal.Decimal] = None
    reportDate: Optional[datetime.date] = None
    ibExecID: Optional[str] = None
    settleDateTarget: Optional[datetime.date] = None
    cost: Optional[decimal.Decimal] = None
    extExecID: Optional[str] = None
    openDateTime: Optional[datetime.datetime] = None
    holdingPeriodDateTime: Optional[datetime.datetime] = None
    whenRealized: Optional[datetime.datetime] = None
    whenReopened: Optional[datetime.datetime] = None
    changeInPrice: Optional[decimal.Decimal] = None
    changeInQuantity: Optional[decimal.Decimal] = None
    ibOrderID: Optional[str] = None
    origOrderID: Optional[str] = None
    transactionID: Optional[str] = None
    tradeDate: Optional[datetime.date] = None
    openCloseIndicator: Optional[enums.OpenClose] = None
    notes: Optional[str] = None
    fxPnl: Optional[decimal.Decimal] = None
    mtmPnl: Optional[decimal.Decimal] = None
    fifoPnlRealized: Optional[decimal.Decimal] = None
    closePrice: Optional[decimal.Decimal] = None
    exchange: Optional[str] = None
    ibCommission: Optional[decimal.Decimal] = None
    ibCommissionCurrency: Optional[str] = None
    netCash: Optional[decimal.Decimal] = None
    buySell: Optional[enums.BuySell] = None
    quantity: Optional[decimal.Decimal] = None
    price: Optional[decimal.Decimal] = None
    amount: Optional[decimal.Decimal] = None
    proceeds: Optional[decimal.Decimal] = None
    commission: Optional[decimal.Decimal] = None
    brokerExecutionCommission: Optional[decimal.Decimal] = None
    brokerClearingCommission: Optional[decimal.Decimal] = None
    thirdPartyExecutionCommission: Optional[decimal.Decimal] = None
    thirdPartyClearingCommission: Optional[decimal.Decimal] = None
    thirdPartyRegulatoryCommission: Optional[decimal.Decimal] = None
    otherCommission: Optional[decimal.Decimal] = None
    commissionCurrency: Optional[str] = None
    tax: Optional[decimal.Decimal] = None
    code: Tuple[enums.Code, ...] = ()
    orderType: Optional[enums.OrderType] = None
    levelOfDetail: Optional[str] = None
    traderID: Optional[str] = None
    isAPIOrder: Optional[bool] = None
    allocatedTo: Optional[str] = None
    accruedInt: Optional[decimal.Decimal] = None
    deliveryType: Optional[str] = None
    serialNumber: Optional[str] = None
    commodityType: Optional[str] = None
    fineness: Optional[decimal.Decimal] = None
    weight: Optional[str] = None


@dataclass(frozen=True)
class Order(FlexElement):
    """Wrapped in <TradeConfirms>"""

    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    currency: Optional[str] = None
    assetCategory: Optional[enums.AssetClass] = None
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
    putCall: Optional[enums.PutCall] = None
    principalAdjustFactor: Optional[Decimal] = None
    transactionType: Optional[enums.TradeType] = None
    tradeID: Optional[str] = None
    orderID: Optional[Decimal] = None
    execID: Optional[str] = None
    brokerageOrderID: Optional[str] = None
    orderReference: Optional[str] = None
    volatilityOrderLink: Optional[str] = None
    clearingFirmID: Optional[str] = None
    origTradePrice: Optional[Decimal] = None
    origTradeDate: Optional[datetime.date] = None
    origTradeID: Optional[str] = None
    #  Despite the name, `orderTime` actually contains date/time data.
    orderTime: Optional[datetime.datetime] = None
    dateTime: Optional[datetime.datetime] = None
    reportDate: Optional[datetime.date] = None
    settleDate: Optional[datetime.date] = None
    tradeDate: Optional[datetime.date] = None
    exchange: Optional[str] = None
    buySell: Optional[enums.BuySell] = None
    quantity: Optional[Decimal] = None
    price: Optional[Decimal] = None
    amount: Optional[Decimal] = None
    proceeds: Optional[Decimal] = None
    commission: Optional[Decimal] = None
    brokerExecutionCommission: Optional[Decimal] = None
    brokerClearingCommission: Optional[Decimal] = None
    thirdPartyExecutionCommission: Optional[Decimal] = None
    thirdPartyClearingCommission: Optional[Decimal] = None
    thirdPartyRegulatoryCommission: Optional[Decimal] = None
    otherCommission: Optional[Decimal] = None
    commissionCurrency: Optional[str] = None
    tax: Optional[Decimal] = None
    code: Tuple[enums.Code, ...] = ()
    orderType: Optional[enums.OrderType] = None
    levelOfDetail: Optional[str] = None
    traderID: Optional[str] = None
    isAPIOrder: Optional[bool] = None
    allocatedTo: Optional[str] = None
    accruedInt: Optional[Decimal] = None
    netCash: Optional[decimal.Decimal] = None
    tradePrice: Optional[decimal.Decimal] = None
    ibCommission: Optional[decimal.Decimal] = None
    ibOrderID: Optional[str] = None
    fxRateToBase: Optional[decimal.Decimal] = None
    settleDateTarget: Optional[datetime.date] = None
    tradeMoney: Optional[decimal.Decimal] = None
    taxes: Optional[decimal.Decimal] = None
    ibCommissionCurrency: Optional[str] = None
    closePrice: Optional[decimal.Decimal] = None
    openCloseIndicator: Optional[enums.OpenClose] = None
    notes: Optional[str] = None
    cost: Optional[decimal.Decimal] = None
    fifoPnlRealized: Optional[decimal.Decimal] = None
    fxPnl: Optional[decimal.Decimal] = None
    mtmPnl: Optional[decimal.Decimal] = None
    origOrderID: Optional[str] = None
    transactionID: Optional[str] = None
    ibExecID: Optional[str] = None
    exchOrderId: Optional[str] = None
    extExecID: Optional[str] = None
    openDateTime: Optional[datetime.datetime] = None
    holdingPeriodDateTime: Optional[datetime.datetime] = None
    whenRealized: Optional[datetime.datetime] = None
    whenReopened: Optional[datetime.datetime] = None
    changeInPrice: Optional[decimal.Decimal] = None
    changeInQuantity: Optional[decimal.Decimal] = None


@dataclass(frozen=True)
class TradeConfirm(FlexElement):
    """Wrapped in <TradeConfirms>"""

    transactionType: Optional[enums.TradeType] = None
    openCloseIndicator: Optional[enums.OpenClose] = None
    buySell: Optional[enums.BuySell] = None
    orderType: Optional[enums.OrderType] = None
    assetCategory: Optional[enums.AssetClass] = None
    accountId: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
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
    putCall: Optional[enums.PutCall] = None
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
    notes: Tuple[enums.Code, ...] = ()  # separator = ";"
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
    code: Tuple[enums.Code, ...] = ()
    tax: Optional[Decimal] = None
    listingExchange: Optional[str] = None
    underlyingListingExchange: Optional[str] = None
    settleDate: Optional[datetime.date] = None
    underlyingSecurityID: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    accruedInt: Optional[Decimal] = None
    relatedTradeID: Optional[str] = None
    relatedTransactionID: Optional[str] = None


@dataclass(frozen=True)
class OptionEAE(FlexElement):
    """Option Exercise Assignment or Expiration

    Wrapped in (identically-named) <OptionEAE>
    """

    transactionType: Optional[enums.OptionAction] = None
    assetCategory: Optional[enums.AssetClass] = None
    accountId: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    securityID: Optional[str] = None
    securityIDType: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    listingExchange: Optional[str] = None
    underlyingSecurityID: Optional[str] = None
    underlyingListingExchange: Optional[str] = None
    underlyingConid: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    issuer: Optional[str] = None
    multiplier: Optional[Decimal] = None
    strike: Optional[Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[enums.PutCall] = None
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
    """Wrapped in <TradeTransfers>"""

    transactionType: Optional[enums.TradeType] = None
    openCloseIndicator: Optional[enums.OpenClose] = None
    direction: Optional[enums.ToFrom] = None
    deliveredReceived: Optional[enums.DeliveredReceived] = None
    assetCategory: Optional[enums.AssetClass] = None
    accountId: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
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
    notes: Tuple[enums.Code, ...] = ()  # separator = ";"
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
    putCall: Optional[enums.PutCall] = None
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
    """Wrapped in <InterestAccruals>"""

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
    code: Tuple[enums.Code, ...] = ()
    fromAcct: Optional[str] = None
    toAcct: Optional[str] = None


@dataclass(frozen=True)
class HardToBorrowDetail(FlexElement):
    """Wrapped in <HardToBorrowDetails>"""

    assetCategory: Optional[enums.AssetClass] = None
    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
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
    putCall: Optional[enums.PutCall] = None
    principalAdjustFactor: Optional[Decimal] = None
    valueDate: Optional[datetime.date] = None
    quantity: Optional[Decimal] = None
    price: Optional[Decimal] = None
    value: Optional[Decimal] = None
    borrowFeeRate: Optional[Decimal] = None
    borrowFee: Optional[Decimal] = None
    code: Tuple[enums.Code, ...] = ()
    fromAcct: Optional[str] = None
    toAcct: Optional[str] = None


@dataclass(frozen=True)
class SLBActivity(FlexElement):
    """Wrapped in <SLBActivities>"""

    assetCategory: Optional[enums.AssetClass] = None
    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
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
    putCall: Optional[enums.PutCall] = None
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
class SLBFee:
    """Wrapped in <SLBFees>"""

    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[str] = None
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
    putCall: Optional[enums.PutCall] = None
    principalAdjustFactor: Optional[Decimal] = None
    valueDate: Optional[datetime.date] = None
    startDate: Optional[datetime.date] = None
    type: Optional[str] = None  # FIXME
    exchange: Optional[str] = None
    quantity: Optional[Decimal] = None
    collateralAmount: Optional[Decimal] = None
    feeRate: Optional[Decimal] = None
    fee: Optional[Decimal] = None
    carryCharge: Optional[Decimal] = None
    ticketCharge: Optional[Decimal] = None
    totalCharges: Optional[Decimal] = None
    marketFeeRate: Optional[Decimal] = None
    grossLendFee: Optional[Decimal] = None
    netLendFeeRate: Optional[Decimal] = None
    netLendFee: Optional[Decimal] = None
    code: Tuple[enums.Code, ...] = ()
    fromAcct: Optional[str] = None
    toAcct: Optional[str] = None


@dataclass(frozen=True)
class Transfer(FlexElement):
    """Wrapped in <Transfers>"""

    type: Optional[enums.TransferType] = None
    direction: Optional[enums.InOut] = None
    assetCategory: Optional[enums.AssetClass] = None
    accountId: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
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
    code: Tuple[enums.Code, ...] = ()
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
    putCall: Optional[enums.PutCall] = None
    principalAdjustFactor: Optional[Decimal] = None
    company: Optional[str] = None
    accountName: Optional[str] = None
    pnlAmount: Optional[Decimal] = None
    pnlAmountInBase: Optional[Decimal] = None
    fxPnl: Optional[Decimal] = None
    transactionID: Optional[str] = None
    serialNumber: Optional[str] = None
    deliveryType: Optional[str] = None
    commodityType: Optional[str] = None
    fineness: Optional[decimal.Decimal] = None
    weight: Optional[str] = None


@dataclass(frozen=True)
class UnsettledTransfer(FlexElement):
    """Wrapped in <UnsettledTransfers>"""

    direction: Optional[enums.ToFrom] = None
    assetCategory: Optional[enums.AssetClass] = None
    accountId: Optional[str] = None
    currency: Optional[str] = None
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
    """Wrapped in <PriorPeriodPositions>"""

    assetCategory: Optional[enums.AssetClass] = None
    accountId: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
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
    putCall: Optional[enums.PutCall] = None
    principalAdjustFactor: Optional[decimal.Decimal] = None


@dataclass(frozen=True)
class CorporateAction(FlexElement):
    """Wrapped in <CorporateActions>"""

    assetCategory: Optional[enums.AssetClass] = None
    accountId: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
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
    type: Optional[enums.Reorg] = None
    code: Tuple[enums.Code, ...] = ()
    sedol: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    securityIDType: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    issuer: Optional[str] = None
    multiplier: Optional[Decimal] = None
    strike: Optional[Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[enums.PutCall] = None
    principalAdjustFactor: Optional[Decimal] = None
    reportDate: Optional[datetime.date] = None
    proceeds: Optional[Decimal] = None
    value: Optional[Decimal] = None
    transactionID: Optional[str] = None
    levelOfDetail: Optional[str] = None
    serialNumber: Optional[str] = None
    deliveryType: Optional[str] = None
    commodityType: Optional[str] = None
    fineness: Optional[decimal.Decimal] = None
    weight: Optional[str] = None


@dataclass(frozen=True)
class CashTransaction(FlexElement):
    """Wrapped in <CashTransactions>"""

    type: Optional[enums.CashAction] = None
    assetCategory: Optional[enums.AssetClass] = None
    accountId: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
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
    putCall: Optional[enums.PutCall] = None
    principalAdjustFactor: Optional[decimal.Decimal] = None
    tradeID: Optional[str] = None
    code: Tuple[enums.Code, ...] = ()
    transactionID: Optional[str] = None
    reportDate: Optional[datetime.date] = None
    clientReference: Optional[str] = None
    settleDate: Optional[datetime.date] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    levelOfDetail: Optional[str] = None
    serialNumber: Optional[str] = None
    deliveryType: Optional[str] = None
    commodityType: Optional[str] = None
    fineness: Optional[decimal.Decimal] = None
    weight: Optional[str] = None


@dataclass(frozen=True)
class DebitCardActivity(FlexElement):
    """Wrapped in <DebitCardActivities>"""

    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    assetCategory: Optional[enums.AssetClass] = None
    status: Optional[str] = None
    reportDate: Optional[datetime.date] = None
    postingDate: Optional[datetime.date] = None
    transactionDateTime: Optional[datetime.datetime] = None
    category: Optional[str] = None
    merchantNameLocation: Optional[str] = None
    amount: Optional[Decimal] = None
    model: Optional[str] = None


@dataclass(frozen=True)
class ChangeInDividendAccrual(FlexElement):
    """Wrapped in <ChangeInDividendAccruals>"""

    date: Optional[datetime.date] = None
    assetCategory: Optional[enums.AssetClass] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    accountId: Optional[str] = None
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
    code: Tuple[enums.Code, ...] = ()
    securityIDType: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    issuer: Optional[str] = None
    multiplier: Optional[Decimal] = None
    strike: Optional[Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[enums.PutCall] = None
    principalAdjustFactor: Optional[Decimal] = None
    fromAcct: Optional[str] = None
    toAcct: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None


#  Type alias to work around https://github.com/python/mypy/issues/1775
_ChangeInDividendAccrual = ChangeInDividendAccrual


@dataclass(frozen=True)
class OpenDividendAccrual(FlexElement):
    """Wrapped in <OpenDividendAccruals>"""

    assetCategory: Optional[enums.AssetClass] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    accountId: Optional[str] = None
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
    exDate: Optional[datetime.date] = None
    payDate: Optional[datetime.date] = None
    quantity: Optional[Decimal] = None
    tax: Optional[Decimal] = None
    fee: Optional[Decimal] = None
    grossRate: Optional[Decimal] = None
    grossAmount: Optional[Decimal] = None
    netAmount: Optional[Decimal] = None
    code: Tuple[enums.Code, ...] = ()
    sedol: Optional[str] = None
    securityIDType: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    issuer: Optional[str] = None
    multiplier: Optional[Decimal] = None
    strike: Optional[Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[enums.PutCall] = None
    principalAdjustFactor: Optional[Decimal] = None
    fromAcct: Optional[str] = None
    toAcct: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    serialNumber: Optional[str] = None
    deliveryType: Optional[str] = None
    commodityType: Optional[str] = None
    fineness: Optional[decimal.Decimal] = None
    weight: Optional[str] = None


@dataclass(frozen=True)
class SecurityInfo(FlexElement):
    """Wrapped in <SecuritiesInfo>"""

    assetCategory: Optional[enums.AssetClass] = None
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
    putCall: Optional[enums.PutCall] = None
    principalAdjustFactor: Optional[decimal.Decimal] = None
    code: Tuple[enums.Code, ...] = ()
    currency: Optional[str] = None
    settlementPolicyMethod: Optional[str] = None


@dataclass(frozen=True)
class ConversionRate(FlexElement):
    """Wrapped in <ConversionRates>"""

    reportDate: Optional[datetime.date] = None
    fromCurrency: Optional[str] = None
    toCurrency: Optional[str] = None
    rate: Optional[Decimal] = None


@dataclass(frozen=True)
class FIFOPerformanceSummaryUnderlying(FlexElement):
    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    listingExchange: Optional[str] = None
    assetCategory: Optional[enums.AssetClass] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    securityID: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    underlyingConid: Optional[str] = None
    underlyingSecurityID: Optional[str] = None
    underlyingListingExchange: Optional[str] = None
    realizedSTProfit: Optional[Decimal] = None
    realizedSTLoss: Optional[Decimal] = None
    realizedLTProfit: Optional[Decimal] = None
    realizedLTLoss: Optional[Decimal] = None
    totalRealizedPnl: Optional[Decimal] = None
    unrealizedProfit: Optional[Decimal] = None
    unrealizedLoss: Optional[Decimal] = None
    totalUnrealizedPnl: Optional[Decimal] = None
    totalFifoPnl: Optional[Decimal] = None
    totalRealizedCapitalGainsPnl: Optional[Decimal] = None
    totalRealizedFxPnl: Optional[Decimal] = None
    totalUnrealizedCapitalGainsPnl: Optional[Decimal] = None
    totalUnrealizedFxPnl: Optional[Decimal] = None
    totalCapitalGainsPnl: Optional[Decimal] = None
    totalFxPnl: Optional[Decimal] = None
    transferredPnl: Optional[Decimal] = None
    transferredCapitalGainsPnl: Optional[Decimal] = None
    transferredFxPnl: Optional[Decimal] = None
    sedol: Optional[str] = None
    securityIDType: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    issuer: Optional[str] = None
    multiplier: Optional[Decimal] = None
    strike: Optional[Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[enums.PutCall] = None
    principalAdjustFactor: Optional[Decimal] = None
    reportDate: Optional[datetime.date] = None
    unrealizedSTProfit: Optional[decimal.Decimal] = None
    unrealizedSTLoss: Optional[decimal.Decimal] = None
    unrealizedLTProfit: Optional[decimal.Decimal] = None
    unrealizedLTLoss: Optional[decimal.Decimal] = None
    costAdj: Optional[Decimal] = None
    code: Tuple[enums.Code, ...] = ()
    serialNumber: Optional[str] = None
    deliveryType: Optional[str] = None
    commodityType: Optional[str] = None
    fineness: Optional[decimal.Decimal] = None
    weight: Optional[str] = None


@dataclass(frozen=True)
class NetStockPosition(FlexElement):
    assetCategory: Optional[enums.AssetClass] = None
    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    currency: Optional[str] = None
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
    putCall: Optional[enums.PutCall] = None
    principalAdjustFactor: Optional[Decimal] = None
    reportDate: Optional[datetime.date] = None
    sharesAtIb: Optional[Decimal] = None
    sharesBorrowed: Optional[Decimal] = None
    sharesLent: Optional[Decimal] = None
    netShares: Optional[Decimal] = None
    serialNumber: Optional[str] = None
    deliveryType: Optional[str] = None
    commodityType: Optional[str] = None
    fineness: Optional[decimal.Decimal] = None
    weight: Optional[str] = None


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


@dataclass(frozen=True)
class TransactionTax(FlexElement):
    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    assetCategory: Optional[enums.AssetClass] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    securityID: Optional[str] = None
    securityIDType: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    listingExchange: Optional[str] = None
    underlyingConid: Optional[str] = None
    underlyingSecurityID: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    underlyingListingExchange: Optional[str] = None
    issuer: Optional[str] = None
    multiplier: Optional[Decimal] = None
    strike: Optional[Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[enums.PutCall] = None
    principalAdjustFactor: Optional[Decimal] = None
    date: Optional[datetime.datetime] = None
    taxDescription: Optional[str] = None
    quantity: Optional[Decimal] = None
    reportDate: Optional[datetime.date] = None
    taxAmount: Optional[Decimal] = None
    tradeId: Optional[str] = None
    tradePrice: Optional[Decimal] = None
    source: Optional[str] = None
    code: Tuple[enums.Code, ...] = ()
    levelOfDetail: Optional[str] = None


@dataclass(frozen=True)
class TransactionTaxDetail(FlexElement):
    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    assetCategory: Optional[enums.AssetClass] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    securityID: Optional[str] = None
    securityIDType: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    listingExchange: Optional[str] = None
    underlyingConid: Optional[str] = None
    underlyingSecurityID: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    underlyingListingExchange: Optional[str] = None
    issuer: Optional[str] = None
    multiplier: Optional[Decimal] = None
    strike: Optional[Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[enums.PutCall] = None
    principalAdjustFactor: Optional[Decimal] = None
    date: Optional[datetime.datetime] = None
    taxDescription: Optional[str] = None
    quantity: Optional[Decimal] = None
    reportDate: Optional[datetime.date] = None
    taxAmount: Optional[Decimal] = None
    tradeId: Optional[str] = None
    tradePrice: Optional[Decimal] = None
    source: Optional[str] = None
    code: Tuple[enums.Code, ...] = ()
    levelOfDetail: Optional[str] = None


@dataclass(frozen=True)
class SalesTax(FlexElement):
    accountId: Optional[str] = None
    acctAlias: Optional[str] = None
    model: Optional[str] = None
    currency: Optional[str] = None
    fxRateToBase: Optional[Decimal] = None
    assetCategory: Optional[enums.AssetClass] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    conid: Optional[str] = None
    securityID: Optional[str] = None
    securityIDType: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    listingExchange: Optional[str] = None
    underlyingConid: Optional[str] = None
    underlyingSecurityID: Optional[str] = None
    underlyingSymbol: Optional[str] = None
    underlyingListingExchange: Optional[str] = None
    issuer: Optional[str] = None
    multiplier: Optional[Decimal] = None
    strike: Optional[Decimal] = None
    expiry: Optional[datetime.date] = None
    putCall: Optional[enums.PutCall] = None
    principalAdjustFactor: Optional[Decimal] = None
    date: Optional[datetime.date] = None
    country: Optional[str] = None
    taxType: Optional[str] = None
    payer: Optional[str] = None
    taxableDescription: Optional[str] = None
    taxableAmount: Optional[Decimal] = None
    taxRate: Optional[Decimal] = None
    salesTax: Optional[Decimal] = None
    taxableTransactionID: Optional[str] = None
    transactionID: Optional[str] = None
    code: Tuple[enums.Code, ...] = ()


#  Type alias to work around https://github.com/python/mypy/issues/1775
_ClientFeesDetail = ClientFeesDetail


@dataclass(frozen=True)
class SLBContract:
    pass


@dataclass(frozen=True)
class SLBContracts:
    pass


@dataclass(frozen=True)
class SLBOpenContract:
    pass
