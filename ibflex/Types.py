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
"""
# PEP 563 compliance
# https://www.python.org/dev/peps/pep-0563/#resolving-type-hints-at-runtime
from __future__ import annotations

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
    "FxTransaction",
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
    "AssetSummary",
    "Order",
]

import datetime
import decimal
from dataclasses import dataclass

from ibflex import enums


@dataclass(frozen=True)
class FlexElement:
    """Base class for data element types"""


@dataclass(frozen=True)
class FlexQueryResponse(FlexElement):
    """Root element"""

    queryName: str
    type: str
    FlexStatements: tuple["FlexStatement", ...]
    Message: str | None = None

    def __repr__(self):
        repr = (
            f"{type(self).__name__}("
            f"queryName={self.queryName!r}, "
            f"type={self.type!r}, "
            f"len(FlexStatements)={len(self.FlexStatements)}"
            f"Message={self.Message!r}"
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
    AccountInformation: "_AccountInformation" | None = None
    ChangeInNAV: "_ChangeInNAV" | None = None
    CashReport: tuple["CashReportCurrency", ...] = ()
    MTDYTDPerformanceSummary: tuple["MTDYTDPerformanceSummaryUnderlying", ...] = ()
    MTMPerformanceSummaryInBase: tuple["MTMPerformanceSummaryUnderlying", ...] = ()
    EquitySummaryInBase: tuple["EquitySummaryByReportDateInBase", ...] = ()
    FIFOPerformanceSummaryInBase: tuple["FIFOPerformanceSummaryUnderlying", ...] = ()
    FdicInsuredDepositsByBank: tuple = ()  # TODO
    StmtFunds: tuple["StatementOfFundsLine", ...] = ()
    ChangeInPositionValues: tuple["ChangeInPositionValue", ...] = ()
    OpenPositions: tuple["OpenPosition", ...] = ()
    NetStockPositionSummary: tuple["NetStockPosition", ...] = ()
    ComplexPositions: tuple = ()  # TODO
    FxPositions: tuple["FxLot", ...] = ()  # N.B. FXLot wrapped in FxLots
    Trades: tuple["Trade", ...] = ()
    HKIPOSubscriptionActivity: tuple = ()  # TODO
    TradeConfirms: tuple["TradeConfirm", ...] = ()
    TransactionTaxes: tuple = ()
    OptionEAE: tuple["_OptionEAE", ...] = ()
    # Not a typo - they really spell it "Excercises"
    PendingExcercises: tuple = ()  # TODO
    TradeTransfers: tuple["TradeTransfer", ...] = ()
    FxTransactions: tuple["FxTransaction", ...] = ()
    UnbookedTrades: tuple = ()  # TODO
    RoutingCommissions: tuple = ()  # TODO
    IBGNoteTransactions: tuple = ()  # TODO
    UnsettledTransfers: tuple["UnsettledTransfer", ...] = ()
    UnbundledCommissionDetails: tuple["UnbundledCommissionDetail", ...] = ()
    Adjustments: tuple = ()  # TODO
    PriorPeriodPositions: tuple["PriorPeriodPosition", ...] = ()
    CorporateActions: tuple["CorporateAction", ...] = ()
    ClientFees: tuple["ClientFee", ...] = ()
    ClientFeesDetail: tuple["_ClientFeesDetail", ...] = ()
    DebitCardActivities: tuple["DebitCardActivity", ...] = ()
    SoftDollars: tuple = ()  # TODO
    CashTransactions: tuple["CashTransaction", ...] = ()
    SalesTaxes: tuple["SalesTax", ...] = ()
    CFDCharges: tuple = ()  # TODO
    InterestAccruals: tuple["InterestAccrualsCurrency", ...] = ()
    TierInterestDetails: tuple["TierInterestDetail", ...] = ()
    HardToBorrowDetails: tuple["HardToBorrowDetail", ...] = ()
    HardToBorrowMarkupDetails: tuple = ()
    SLBOpenContracts: tuple["SLBOpenContract", ...] = ()
    SLBActivities: tuple["SLBActivity", ...] = ()
    SLBFees: tuple["SLBFee", ...] = ()
    Transfers: tuple["Transfer", ...] = ()
    ChangeInDividendAccruals: tuple["_ChangeInDividendAccrual", ...] = ()
    OpenDividendAccruals: tuple["OpenDividendAccrual", ...] = ()
    SecuritiesInfo: tuple["SecurityInfo", ...] = ()
    ConversionRates: tuple["ConversionRate", ...] = ()
    HKIPOOpenSubscriptions: tuple = ()  # TODO
    CommissionCredits: tuple = ()  # TODO
    StockGrantActivities: tuple = ()  # TODO
    SLBCollaterals: tuple = ()  # TODO
    IncentiveCouponAccrualDetails: tuple = ()  # TODO
    DepositsOnHold: tuple = ()  # TODO

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

    accountId: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    currency: str | None = None
    name: str | None = None
    accountType: str | None = None
    customerType: str | None = None
    accountCapabilities: tuple[str, ...] = ()
    tradingPermissions: tuple[str, ...] = ()
    registeredRepName: str | None = None
    registeredRepPhone: str | None = None
    dateOpened: datetime.date | None = None
    dateFunded: datetime.date | None = None
    dateClosed: datetime.date | None = None
    street: str | None = None
    street2: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postalCode: str | None = None
    streetResidentialAddress: str | None = None
    street2ResidentialAddress: str | None = None
    cityResidentialAddress: str | None = None
    stateResidentialAddress: str | None = None
    countryResidentialAddress: str | None = None
    postalCodeResidentialAddress: str | None = None
    masterName: str | None = None
    ibEntity: str | None = None
    primaryEmail: str | None = None
    accountRepName: str | None = None
    accountRepPhone: str | None = None
    lastTradedDate: datetime.date | None = None


#  Type alias to work around https://github.com/python/mypy/issues/1775
_AccountInformation = AccountInformation


@dataclass(frozen=True)
class ChangeInNAV(FlexElement):
    """Child of <FlexStatement>"""

    accountId: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    fromDate: datetime.date | None = None
    toDate: datetime.date | None = None
    startingValue: decimal.Decimal | None = None
    mtm: decimal.Decimal | None = None
    realized: decimal.Decimal | None = None
    changeInUnrealized: decimal.Decimal | None = None
    costAdjustments: decimal.Decimal | None = None
    transferredPnlAdjustments: decimal.Decimal | None = None
    depositsWithdrawals: decimal.Decimal | None = None
    internalCashTransfers: decimal.Decimal | None = None
    assetTransfers: decimal.Decimal | None = None
    debitCardActivity: decimal.Decimal | None = None
    billPay: decimal.Decimal | None = None
    dividends: decimal.Decimal | None = None
    withholdingTax: decimal.Decimal | None = None
    withholding871m: decimal.Decimal | None = None
    withholdingTaxCollected: decimal.Decimal | None = None
    changeInDividendAccruals: decimal.Decimal | None = None
    interest: decimal.Decimal | None = None
    changeInInterestAccruals: decimal.Decimal | None = None
    advisorFees: decimal.Decimal | None = None
    brokerFees: decimal.Decimal | None = None
    changeInBrokerFeeAccruals: decimal.Decimal | None = None
    clientFees: decimal.Decimal | None = None
    otherFees: decimal.Decimal | None = None
    feesReceivables: decimal.Decimal | None = None
    commissions: decimal.Decimal | None = None
    commissionReceivables: decimal.Decimal | None = None
    forexCommissions: decimal.Decimal | None = None
    transactionTax: decimal.Decimal | None = None
    taxReceivables: decimal.Decimal | None = None
    salesTax: decimal.Decimal | None = None
    softDollars: decimal.Decimal | None = None
    netFxTrading: decimal.Decimal | None = None
    fxTranslation: decimal.Decimal | None = None
    linkingAdjustments: decimal.Decimal | None = None
    other: decimal.Decimal | None = None
    endingValue: decimal.Decimal | None = None
    twr: decimal.Decimal | None = None
    corporateActionProceeds: decimal.Decimal | None = None
    commissionCreditsRedemption: decimal.Decimal | None = None
    grantActivity: decimal.Decimal | None = None
    excessFundSweep: decimal.Decimal | None = None
    billableSalesTax: decimal.Decimal | None = None
    mtmAtPaxos: decimal.Decimal | None = None
    carbonCredits: decimal.Decimal | None = None
    donations: decimal.Decimal | None = None
    paxosTransfers: decimal.Decimal | None = None
    commissionsAtPaxos: decimal.Decimal | None = None
    referralFee: decimal.Decimal | None = None
    currency: str | None = None
    changeInIncentiveCouponAccruals: decimal.Decimal | None = None
    otherIncome: decimal.Decimal | None = None

#  Type alias to work around https://github.com/python/mypy/issues/1775
_ChangeInNAV = ChangeInNAV


@dataclass(frozen=True)
class MTMPerformanceSummaryUnderlying(FlexElement):
    """Wrapped in <MTMPerformanceSummaryInBase>"""

    assetCategory: enums.AssetClass | None = None
    accountId: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    securityIDType: str | None = None
    cusip: str | None = None
    isin: str | None = None
    sedol: str | None = None
    listingExchange: str | None = None
    underlyingConid: str | None = None
    underlyingSymbol: str | None = None
    underlyingSecurityID: str | None = None
    underlyingListingExchange: str | None = None
    issuer: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    reportDate: datetime.date | None = None
    prevCloseQuantity: decimal.Decimal | None = None
    prevClosePrice: decimal.Decimal | None = None
    closeQuantity: decimal.Decimal | None = None
    closePrice: decimal.Decimal | None = None
    transactionMtm: decimal.Decimal | None = None
    priorOpenMtm: decimal.Decimal | None = None
    commissions: decimal.Decimal | None = None
    other: decimal.Decimal | None = None
    total: decimal.Decimal | None = None
    code: tuple[enums.Code, ...] = ()
    corpActionMtm: decimal.Decimal | None = None
    dividends: decimal.Decimal | None = None
    serialNumber: str | None = None
    deliveryType: str | None = None
    commodityType: str | None = None
    fineness: decimal.Decimal | None = None
    weight: str | None = None
    otherWithAccruals: decimal.Decimal | None = None
    totalWithAccruals: decimal.Decimal | None = None
    subCategory: str | None = None
    figi: str | None = None
    issuerCountryCode: str | None = None

@dataclass(frozen=True)
class EquitySummaryByReportDateInBase(FlexElement):
    """Wrapped in <EquitySummaryInBase>"""

    accountId: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    currency: str | None = None
    reportDate: datetime.date | None = None
    cash: decimal.Decimal | None = None
    cashLong: decimal.Decimal | None = None
    cashShort: decimal.Decimal | None = None
    slbCashCollateral: decimal.Decimal | None = None
    slbCashCollateralLong: decimal.Decimal | None = None
    slbCashCollateralShort: decimal.Decimal | None = None
    stock: decimal.Decimal | None = None
    stockLong: decimal.Decimal | None = None
    stockShort: decimal.Decimal | None = None
    slbDirectSecuritiesBorrowed: decimal.Decimal | None = None
    slbDirectSecuritiesBorrowedLong: decimal.Decimal | None = None
    slbDirectSecuritiesBorrowedShort: decimal.Decimal | None = None
    slbDirectSecuritiesLent: decimal.Decimal | None = None
    slbDirectSecuritiesLentLong: decimal.Decimal | None = None
    slbDirectSecuritiesLentShort: decimal.Decimal | None = None
    options: decimal.Decimal | None = None
    optionsLong: decimal.Decimal | None = None
    optionsShort: decimal.Decimal | None = None
    bonds: decimal.Decimal | None = None
    bondsLong: decimal.Decimal | None = None
    bondsShort: decimal.Decimal | None = None
    bondInterestAccrualsComponent: decimal.Decimal | None = None
    bondInterestAccrualsComponentLong: decimal.Decimal | None = None
    bondInterestAccrualsComponentShort: decimal.Decimal | None = None
    notes: decimal.Decimal | None = None
    notesLong: decimal.Decimal | None = None
    notesShort: decimal.Decimal | None = None
    incentiveCouponAccruals: decimal.Decimal | None = None
    interestAccruals: decimal.Decimal | None = None
    interestAccrualsLong: decimal.Decimal | None = None
    interestAccrualsShort: decimal.Decimal | None = None
    softDollars: decimal.Decimal | None = None
    softDollarsLong: decimal.Decimal | None = None
    softDollarsShort: decimal.Decimal | None = None
    dividendAccruals: decimal.Decimal | None = None
    dividendAccrualsLong: decimal.Decimal | None = None
    dividendAccrualsShort: decimal.Decimal | None = None
    total: decimal.Decimal | None = None
    totalLong: decimal.Decimal | None = None
    totalShort: decimal.Decimal | None = None
    commodities: decimal.Decimal | None = None
    commoditiesLong: decimal.Decimal | None = None
    commoditiesShort: decimal.Decimal | None = None
    funds: decimal.Decimal | None = None
    fundsLong: decimal.Decimal | None = None
    fundsShort: decimal.Decimal | None = None
    forexCfdUnrealizedPl: decimal.Decimal | None = None
    forexCfdUnrealizedPlLong: decimal.Decimal | None = None
    forexCfdUnrealizedPlShort: decimal.Decimal | None = None
    brokerInterestAccrualsComponent: decimal.Decimal | None = None
    brokerCashComponent: decimal.Decimal | None = None
    brokerFeesAccrualsComponent: decimal.Decimal | None = None
    brokerFeesAccrualsComponentLong: decimal.Decimal | None = None
    brokerFeesAccrualsComponentShort: decimal.Decimal | None = None
    eventContractInterestAccruals: decimal.Decimal | None = None
    marginFinancingChargeAccruals: decimal.Decimal | None = None
    cfdUnrealizedPl: decimal.Decimal | None = None
    insuredBankDepositRedemptionCashComponent: decimal.Decimal | None = None
    fdicInsuredBankSweepAccount: decimal.Decimal | None = None
    fdicInsuredBankSweepAccountLong: decimal.Decimal | None = None
    fdicInsuredBankSweepAccountShort: decimal.Decimal | None = None
    fdicInsuredBankSweepAccountCashComponent: decimal.Decimal | None = None
    fdicInsuredBankSweepAccountCashComponentLong: decimal.Decimal | None = None
    fdicInsuredBankSweepAccountCashComponentShort: decimal.Decimal | None = None
    fdicInsuredAccountInterestAccruals: decimal.Decimal | None = None
    fdicInsuredAccountInterestAccrualsLong: decimal.Decimal | None = None
    fdicInsuredAccountInterestAccrualsShort: decimal.Decimal | None = None
    fdicInsuredAccountInterestAccrualsComponent: decimal.Decimal | None = None
    fdicInsuredAccountInterestAccrualsComponentLong: decimal.Decimal | None = None
    fdicInsuredAccountInterestAccrualsComponentShort: decimal.Decimal | None = None
    brokerCashComponentLong: decimal.Decimal | None = None
    brokerCashComponentShort: decimal.Decimal | None = None
    brokerInterestAccrualsComponentLong: decimal.Decimal | None = None
    brokerInterestAccrualsComponentShort: decimal.Decimal | None = None
    cfdUnrealizedPlLong: decimal.Decimal | None = None
    cfdUnrealizedPlShort: decimal.Decimal | None = None
    ipoSubscription: decimal.Decimal | None = None
    ipoSubscriptionLong: decimal.Decimal | None = None
    ipoSubscriptionShort: decimal.Decimal | None = None
    crypto: decimal.Decimal | None = None
    physDel: decimal.Decimal | None = None
    physDelLong: decimal.Decimal | None = None
    physDelShort: decimal.Decimal | None = None
    insuredBankDepositRedemptionCashComponentLong: decimal.Decimal | None = None
    insuredBankDepositRedemptionCashComponentShort: decimal.Decimal | None = None
    incentiveCouponAccrualsLong: decimal.Decimal | None = None
    incentiveCouponAccrualsShort: decimal.Decimal | None = None
    eventContractInterestAccrualsLong: decimal.Decimal | None = None
    eventContractInterestAccrualsShort: decimal.Decimal | None = None
    marginFinancingChargeAccrualsLong: decimal.Decimal | None = None
    marginFinancingChargeAccrualsShort: decimal.Decimal | None = None
    cryptoLong: decimal.Decimal | None = None
    cryptoShort: decimal.Decimal | None = None
    liteSurchargeAccruals: decimal.Decimal | None = None


@dataclass(frozen=True)
class MTDYTDPerformanceSummaryUnderlying(FlexElement):
    """Wrapped in <MTDYTDPerformanceSummary>"""

    assetCategory: enums.AssetClass | None = None
    accountId: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    cusip: str | None = None
    isin: str | None = None
    listingExchange: str | None = None
    underlyingConid: str | None = None
    underlyingSecurityID: str | None = None
    underlyingListingExchange: str | None = None
    mtmMTD: decimal.Decimal | None = None
    mtmYTD: decimal.Decimal | None = None
    realSTMTD: decimal.Decimal | None = None
    realSTYTD: decimal.Decimal | None = None
    realLTMTD: decimal.Decimal | None = None
    realLTYTD: decimal.Decimal | None = None
    securityIDType: str | None = None
    underlyingSymbol: str | None = None
    issuer: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    realizedPnlMTD: decimal.Decimal | None = None
    realizedCapitalGainsPnlMTD: decimal.Decimal | None = None
    realizedFxPnlMTD: decimal.Decimal | None = None
    realizedPnlYTD: decimal.Decimal | None = None
    realizedCapitalGainsPnlYTD: decimal.Decimal | None = None
    realizedFxPnlYTD: decimal.Decimal | None = None
    brokerFees: decimal.Decimal | None = None
    brokerFeesSec: decimal.Decimal | None = None
    brokerFeesCom: decimal.Decimal | None = None
    brokerFeesMTD: decimal.Decimal | None = None
    brokerFeesYTD: decimal.Decimal | None = None
    serialNumber: str | None = None
    deliveryType: str | None = None
    commodityType: str | None = None
    fineness: decimal.Decimal | None = None
    weight: str | None = None


@dataclass(frozen=True)
class CashReportCurrency(FlexElement):
    """Wrapped in <CashReport>"""

    accountId: str | None = None
    currency: str | None = None
    fromDate: datetime.date | None = None
    toDate: datetime.date | None = None
    startingCash: decimal.Decimal | None = None
    startingCashPaxos: decimal.Decimal | None = None
    startingCashSec: decimal.Decimal | None = None
    startingCashCom: decimal.Decimal | None = None
    clientFees: decimal.Decimal | None = None
    clientFeesSec: decimal.Decimal | None = None
    clientFeesCom: decimal.Decimal | None = None
    commissions: decimal.Decimal | None = None
    commissionsSec: decimal.Decimal | None = None
    commissionsCom: decimal.Decimal | None = None
    billableCommissions: decimal.Decimal | None = None
    billableCommissionsSec: decimal.Decimal | None = None
    billableCommissionsCom: decimal.Decimal | None = None
    billableSalesTaxIBUKL: decimal.Decimal | None = None
    depositWithdrawals: decimal.Decimal | None = None
    depositWithdrawalsSec: decimal.Decimal | None = None
    depositWithdrawalsCom: decimal.Decimal | None = None
    deposits: decimal.Decimal | None = None
    depositsSec: decimal.Decimal | None = None
    depositsCom: decimal.Decimal | None = None
    withdrawals: decimal.Decimal | None = None
    withdrawalsSec: decimal.Decimal | None = None
    withdrawalsCom: decimal.Decimal | None = None
    accountTransfers: decimal.Decimal | None = None
    accountTransfersSec: decimal.Decimal | None = None
    accountTransfersCom: decimal.Decimal | None = None
    internalTransfers: decimal.Decimal | None = None
    internalTransfersSec: decimal.Decimal | None = None
    internalTransfersCom: decimal.Decimal | None = None
    dividends: decimal.Decimal | None = None
    dividendsSec: decimal.Decimal | None = None
    dividendsCom: decimal.Decimal | None = None
    brokerFees: decimal.Decimal | None = None
    brokerFeesSec: decimal.Decimal | None = None
    brokerFeesCom: decimal.Decimal | None = None
    brokerFeesMTD: decimal.Decimal | None = None
    brokerFeesYTD: decimal.Decimal | None = None
    brokerFeesPaxos: decimal.Decimal | None = None
    brokerInterest: decimal.Decimal | None = None
    brokerInterestSec: decimal.Decimal | None = None
    brokerInterestCom: decimal.Decimal | None = None
    bondInterest: decimal.Decimal | None = None
    bondInterestSec: decimal.Decimal | None = None
    bondInterestCom: decimal.Decimal | None = None
    bondInterestPaxos: decimal.Decimal | None = None
    cashSettlingMtm: decimal.Decimal | None = None
    cashSettlingMtmSec: decimal.Decimal | None = None
    cashSettlingMtmCom: decimal.Decimal | None = None
    cfdCharges: decimal.Decimal | None = None
    cfdChargesSec: decimal.Decimal | None = None
    cfdChargesCom: decimal.Decimal | None = None
    netTradesSales: decimal.Decimal | None = None
    netTradesSalesSec: decimal.Decimal | None = None
    netTradesSalesCom: decimal.Decimal | None = None
    netTradesPurchases: decimal.Decimal | None = None
    netTradesPurchasesSec: decimal.Decimal | None = None
    netTradesPurchasesCom: decimal.Decimal | None = None
    feesReceivables: decimal.Decimal | None = None
    feesReceivablesSec: decimal.Decimal | None = None
    feesReceivablesCom: decimal.Decimal | None = None
    paymentInLieu: decimal.Decimal | None = None
    paymentInLieuSec: decimal.Decimal | None = None
    paymentInLieuCom: decimal.Decimal | None = None
    paymentInLieuIBUKL: decimal.Decimal | None = None
    transactionTax: decimal.Decimal | None = None
    transactionTaxSec: decimal.Decimal | None = None
    transactionTaxCom: decimal.Decimal | None = None
    withholdingTax: decimal.Decimal | None = None
    withholdingTaxSec: decimal.Decimal | None = None
    withholdingTaxCom: decimal.Decimal | None = None
    fxTranslationGainLoss: decimal.Decimal | None = None
    fxTranslationGainLossSec: decimal.Decimal | None = None
    fxTranslationGainLossCom: decimal.Decimal | None = None
    fxTranslationGainLossPaxos: decimal.Decimal | None = None
    otherFees: decimal.Decimal | None = None
    otherFeesSec: decimal.Decimal | None = None
    otherFeesCom: decimal.Decimal | None = None
    endingCash: decimal.Decimal | None = None
    endingCashSec: decimal.Decimal | None = None
    endingCashCom: decimal.Decimal | None = None
    endingCashPaxos: decimal.Decimal | None = None
    endingSettledCash: decimal.Decimal | None = None
    endingSettledCashSec: decimal.Decimal | None = None
    endingSettledCashCom: decimal.Decimal | None = None
    endingSettledCashPaxos: decimal.Decimal | None = None
    endingCashIBUKL: decimal.Decimal | None = None
    clientFeesMTD: decimal.Decimal | None = None
    clientFeesYTD: decimal.Decimal | None = None
    clientFeesPaxos: decimal.Decimal | None = None
    commissionsMTD: decimal.Decimal | None = None
    commissionsYTD: decimal.Decimal | None = None
    commissionsPaxos: decimal.Decimal | None = None
    billableCommissionsMTD: decimal.Decimal | None = None
    billableCommissionsYTD: decimal.Decimal | None = None
    billableCommissionsPaxos: decimal.Decimal | None = None
    depositWithdrawalsMTD: decimal.Decimal | None = None
    depositWithdrawalsYTD: decimal.Decimal | None = None
    depositWithdrawalsPaxos: decimal.Decimal | None = None
    depositsMTD: decimal.Decimal | None = None
    depositsYTD: decimal.Decimal | None = None
    depositsPaxos: decimal.Decimal | None = None
    withdrawalsMTD: decimal.Decimal | None = None
    withdrawalsYTD: decimal.Decimal | None = None
    withdrawalsPaxos: decimal.Decimal | None = None
    accountTransfersMTD: decimal.Decimal | None = None
    accountTransfersYTD: decimal.Decimal | None = None
    accountTransfersPaxos: decimal.Decimal | None = None
    internalTransfersMTD: decimal.Decimal | None = None
    internalTransfersYTD: decimal.Decimal | None = None
    internalTransfersPaxos: decimal.Decimal | None = None
    paxosTransfersPaxos: decimal.Decimal | None = None
    excessFundSweep: decimal.Decimal | None = None
    excessFundSweepSec: decimal.Decimal | None = None
    excessFundSweepCom: decimal.Decimal | None = None
    excessFundSweepMTD: decimal.Decimal | None = None
    excessFundSweepYTD: decimal.Decimal | None = None
    excessFundSweepPaxos: decimal.Decimal | None = None
    dividendsMTD: decimal.Decimal | None = None
    dividendsYTD: decimal.Decimal | None = None
    dividendsPaxos: decimal.Decimal | None = None
    insuredDepositInterestMTD: decimal.Decimal | None = None
    insuredDepositInterestYTD: decimal.Decimal | None = None
    insuredDepositInteresPaxos: decimal.Decimal | None = None
    brokerInterestMTD: decimal.Decimal | None = None
    brokerInterestYTD: decimal.Decimal | None = None
    brokerInterestPaxos: decimal.Decimal | None = None
    bondInterestMTD: decimal.Decimal | None = None
    bondInterestYTD: decimal.Decimal | None = None
    cashSettlingMtmMTD: decimal.Decimal | None = None
    cashSettlingMtmYTD: decimal.Decimal | None = None
    cashSettlingMtmPaxos: decimal.Decimal | None = None
    realizedVmMTD: decimal.Decimal | None = None
    realizedVmYTD: decimal.Decimal | None = None
    realizedVmPaxos: decimal.Decimal | None = None
    cfdChargesMTD: decimal.Decimal | None = None
    cfdChargesYTD: decimal.Decimal | None = None
    cfdChargesPaxos: decimal.Decimal | None = None
    netTradesSalesMTD: decimal.Decimal | None = None
    netTradesSalesYTD: decimal.Decimal | None = None
    netTradesSalesPaxos: decimal.Decimal | None = None
    advisorFeesMTD: decimal.Decimal | None = None
    advisorFeesYTD: decimal.Decimal | None = None
    advisorFeePaxos: decimal.Decimal | None = None
    feesReceivablesMTD: decimal.Decimal | None = None
    feesReceivablesYTD: decimal.Decimal | None = None
    feesReceivablesPaxos: decimal.Decimal | None = None
    netTradesPurchasesMTD: decimal.Decimal | None = None
    netTradesPurchasesYTD: decimal.Decimal | None = None
    netTradesPurchasesPaxos: decimal.Decimal | None = None
    paymentInLieuMTD: decimal.Decimal | None = None
    paymentInLieuYTD: decimal.Decimal | None = None
    paymentInLieuPaxos: decimal.Decimal | None = None
    transactionTaxMTD: decimal.Decimal | None = None
    transactionTaxYTD: decimal.Decimal | None = None
    transactionTaxPaxos: decimal.Decimal | None = None
    taxReceivablesMTD: decimal.Decimal | None = None
    taxReceivablesYTD: decimal.Decimal | None = None
    taxReceivablesPaxos: decimal.Decimal | None = None
    withholdingTaxMTD: decimal.Decimal | None = None
    withholdingTaxYTD: decimal.Decimal | None = None
    withholdingTaxPaxos: decimal.Decimal | None = None
    withholding871mMTD: decimal.Decimal | None = None
    withholding871mYTD: decimal.Decimal | None = None
    withholding871mPaxos: decimal.Decimal | None = None
    withholdingCollectedTaxMTD: decimal.Decimal | None = None
    withholdingCollectedTaxYTD: decimal.Decimal | None = None
    withholdingCollectedTaxPaxos: decimal.Decimal | None = None
    salesTaxMTD: decimal.Decimal | None = None
    salesTaxYTD: decimal.Decimal | None = None
    salesTaxPaxos: decimal.Decimal | None = None
    otherIncome: decimal.Decimal | None = None
    otherIncomeMTD: decimal.Decimal | None = None
    otherIncomeYTD: decimal.Decimal | None = None
    otherIncomeSec: decimal.Decimal | None = None
    otherIncomeCom: decimal.Decimal | None = None
    otherFeesMTD: decimal.Decimal | None = None
    otherFeesYTD: decimal.Decimal | None = None
    otherFeesPaxos: decimal.Decimal | None = None
    acctAlias: str | None = None
    model: str | None = None
    avgCreditBalance: decimal.Decimal | None = None
    avgCreditBalanceSec: decimal.Decimal | None = None
    avgCreditBalanceCom: decimal.Decimal | None = None
    avgDebitBalance: decimal.Decimal | None = None
    avgDebitBalanceSec: decimal.Decimal | None = None
    avgDebitBalanceCom: decimal.Decimal | None = None
    linkingAdjustments: decimal.Decimal | None = None
    linkingAdjustmentsSec: decimal.Decimal | None = None
    linkingAdjustmentsCom: decimal.Decimal | None = None
    linkingAdjustmentsPaxos: decimal.Decimal | None = None
    insuredDepositInterest: decimal.Decimal | None = None
    insuredDepositInterestSec: decimal.Decimal | None = None
    insuredDepositInterestCom: decimal.Decimal | None = None
    insuredDepositInterestPaxos: decimal.Decimal | None = None
    realizedVm: decimal.Decimal | None = None
    realizedVmSec: decimal.Decimal | None = None
    realizedVmCom: decimal.Decimal | None = None
    advisorFees: decimal.Decimal | None = None
    advisorFeesSec: decimal.Decimal | None = None
    advisorFeesCom: decimal.Decimal | None = None
    advisorFeesPaxos: decimal.Decimal | None = None
    taxReceivables: decimal.Decimal | None = None
    taxReceivablesSec: decimal.Decimal | None = None
    taxReceivablesCom: decimal.Decimal | None = None
    withholding871m: decimal.Decimal | None = None
    withholding871mSec: decimal.Decimal | None = None
    withholding871mCom: decimal.Decimal | None = None
    withholdingCollectedTax: decimal.Decimal | None = None
    withholdingCollectedTaxSec: decimal.Decimal | None = None
    withholdingCollectedTaxCom: decimal.Decimal | None = None
    salesTax: decimal.Decimal | None = None
    salesTaxSec: decimal.Decimal | None = None
    salesTaxCom: decimal.Decimal | None = None
    other: decimal.Decimal | None = None
    otherSec: decimal.Decimal | None = None
    otherCom: decimal.Decimal | None = None
    otherPaxos: decimal.Decimal | None = None
    levelOfDetail: str | None = None
    debitCardActivity: decimal.Decimal | None = None
    debitCardActivitySec: decimal.Decimal | None = None
    debitCardActivityCom: decimal.Decimal | None = None
    debitCardActivityMTD: decimal.Decimal | None = None
    debitCardActivityYTD: decimal.Decimal | None = None
    debitCardActivityPaxos: decimal.Decimal | None = None
    billPay: decimal.Decimal | None = None
    billPaySec: decimal.Decimal | None = None
    billPayCom: decimal.Decimal | None = None
    billPayMTD: decimal.Decimal | None = None
    billPayYTD: decimal.Decimal | None = None
    billPayPaxos: decimal.Decimal | None = None
    realizedForexVm: decimal.Decimal | None = None
    realizedForexVmSec: decimal.Decimal | None = None
    realizedForexVmCom: decimal.Decimal | None = None
    realizedForexVmMTD: decimal.Decimal | None = None
    realizedForexVmYTD: decimal.Decimal | None = None
    realizedForexVmPaxos: decimal.Decimal | None = None
    ipoSubscription: decimal.Decimal | None = None
    ipoSubscriptionSec: decimal.Decimal | None = None
    ipoSubscriptionCom: decimal.Decimal | None = None
    ipoSubscriptionMTD: decimal.Decimal | None = None
    ipoSubscriptionYTD: decimal.Decimal | None = None
    ipoSubscriptionPaxos: decimal.Decimal | None = None
    billableSalesTax: decimal.Decimal | None = None
    billableSalesTaxSec: decimal.Decimal | None = None
    billableSalesTaxCom: decimal.Decimal | None = None
    billableSalesTaxMTD: decimal.Decimal | None = None
    billableSalesTaxYTD: decimal.Decimal | None = None
    billableSalesTaxPaxos: decimal.Decimal | None = None
    commissionCreditsRedemption: decimal.Decimal | None = None
    commissionCreditsRedemptionSec: decimal.Decimal | None = None
    commissionCreditsRedemptionCom: decimal.Decimal | None = None
    commissionCreditsRedemptionMTD: decimal.Decimal | None = None
    commissionCreditsRedemptionYTD: decimal.Decimal | None = None
    commissionCreditsRedemptionPaxos: decimal.Decimal | None = None
    referralFee: decimal.Decimal | None = None
    referralFeePaxos: decimal.Decimal | None = None
    referralFeeSec: decimal.Decimal | None = None
    referralFeeCom: decimal.Decimal | None = None
    referralFeeMTD: decimal.Decimal | None = None
    referralFeeYTD: decimal.Decimal | None = None
    carbonCredits: decimal.Decimal | None = None
    carbonCreditsSec: decimal.Decimal | None = None
    carbonCreditsCom: decimal.Decimal | None = None
    carbonCreditsMTD: decimal.Decimal | None = None
    carbonCreditsYTD: decimal.Decimal | None = None
    carbonCreditsPaxos: decimal.Decimal | None = None
    donations: decimal.Decimal | None = None
    donationsSec: decimal.Decimal | None = None
    donationsCom: decimal.Decimal | None = None
    donationsMTD: decimal.Decimal | None = None
    donationsYTD: decimal.Decimal | None = None
    donationsPaxos: decimal.Decimal | None = None
    paxosTransfers: decimal.Decimal | None = None
    paxosTransfersSec: decimal.Decimal | None = None
    paxosTransfersCom: decimal.Decimal | None = None
    paxosTransfersMTD: decimal.Decimal | None = None
    paxosTransfersYTD: decimal.Decimal | None = None
    slbStartingCashCollateral: decimal.Decimal | None = None
    slbStartingCashCollateralSec: decimal.Decimal | None = None
    slbStartingCashCollateralCom: decimal.Decimal | None = None
    slbStartingCashCollateralPaxos: decimal.Decimal | None = None
    slbNetSecuritiesLentActivity: decimal.Decimal | None = None
    slbNetSecuritiesLentActivityCom: decimal.Decimal | None = None
    slbNetSecuritiesLentActivitySec: decimal.Decimal | None = None
    slbNetSecuritiesLentActivityPaxos: decimal.Decimal | None = None
    slbEndingCashCollateral: decimal.Decimal | None = None
    slbEndingCashCollateralSec: decimal.Decimal | None = None
    slbEndingCashCollateralCom: decimal.Decimal | None = None
    slbEndingCashCollateralPaxos: decimal.Decimal | None = None
    slbNetCash: decimal.Decimal | None = None
    slbNetCashSec: decimal.Decimal | None = None
    slbNetCashCom: decimal.Decimal | None = None
    slbNetCashPaxos: decimal.Decimal | None = None
    slbNetSettledCash: decimal.Decimal | None = None
    slbNetSettledCashSec: decimal.Decimal | None = None
    slbNetSettledCashCom: decimal.Decimal | None = None
    slbNetSettledCashPaxos: decimal.Decimal | None = None


@dataclass(frozen=True)
class CFDCharge(FlexElement):
    """Wrapped in <CFDCharge>"""

    assetCategory: enums.AssetClass | None = None
    accountId: str | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    cusip: str | None = None
    isin: str | None = None
    listingExchange: str | None = None
    underlyingConid: str | None = None
    underlyingSecurityID: str | None = None
    underlyingListingExchange: str | None = None
    amount: decimal.Decimal | None = None
    dateTime: datetime.datetime | None = None
    sedol: str | None = None
    symbol: str | None = None
    securityIDType: str | None = None
    underlyingSymbol: str | None = None
    issuer: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    tradeID: str | None = None
    code: tuple[enums.Code, ...] = ()
    transactionID: str | None = None
    reportDate: datetime.date | None = None
    date: datetime.date | None = None
    received: decimal.Decimal | None = None
    paid: decimal.Decimal | None = None
    total: decimal.Decimal | None = None
    transactionId: str | None = None
    activityDescription: str | None = None
    clientReference: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    levelOfDetail: str | None = None


@dataclass(frozen=True)
class StatementOfFundsLine(FlexElement):
    """Wrapped in <StmtFunds>"""

    assetCategory: enums.AssetClass | None = None
    accountId: str | None = None
    balance: decimal.Decimal | None = None
    debit: decimal.Decimal | None = None
    credit: decimal.Decimal | None = None
    currency: str | None = None
    tradeID: str | None = None
    # Despite the name, `date` actually contains date/time data.
    date: datetime.datetime | None = None
    reportDate: datetime.date | None = None
    activityDescription: str | None = None
    amount: decimal.Decimal | None = None
    buySell: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    securityIDType: str | None = None
    cusip: str | None = None
    isin: str | None = None
    underlyingConid: str | None = None
    underlyingSymbol: str | None = None
    issuer: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    fxRateToBase: decimal.Decimal | None = None
    listingExchange: str | None = None
    underlyingSecurityID: str | None = None
    underlyingListingExchange: str | None = None
    settleDate: datetime.date | None = None
    activityCode: str | None = None  # FIXME
    orderID: str | None = None
    tradeQuantity: decimal.Decimal | None = None
    tradePrice: decimal.Decimal | None = None
    tradeGross: decimal.Decimal | None = None
    tradeCommission: decimal.Decimal | None = None
    tradeTax: decimal.Decimal | None = None
    tradeCode: str | None = None
    levelOfDetail: str | None = None
    transactionID: str | None = None
    serialNumber: str | None = None
    deliveryType: str | None = None
    commodityType: str | None = None
    fineness: decimal.Decimal | None = None
    weight: str | None = None
    actionID: str | None = None
    subCategory: str | None = None
    figi: str | None = None
    issuerCountryCode: str | None = None
    relatedTradeID: str | None = None
    origTransactionID: str | None = None
    relatedTransactionID: str | None = None


@dataclass(frozen=True)
class ChangeInPositionValue(FlexElement):
    """Wrapped in <ChangeInPositionValues>"""

    assetCategory: enums.AssetClass | None = None
    currency: str | None = None
    priorPeriodValue: decimal.Decimal | None = None
    transactions: decimal.Decimal | None = None
    mtmPriorPeriodPositions: decimal.Decimal | None = None
    mtmTransactions: decimal.Decimal | None = None
    corporateActions: decimal.Decimal | None = None
    accountTransfers: decimal.Decimal | None = None
    fxTranslationPnl: decimal.Decimal | None = None
    futurePriceAdjustments: decimal.Decimal | None = None
    settledCash: decimal.Decimal | None = None
    endOfPeriodValue: decimal.Decimal | None = None
    accountId: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    other: decimal.Decimal | None = None
    linkingAdjustments: decimal.Decimal | None = None


@dataclass(frozen=True)
class OpenPosition(FlexElement):
    """Wrapped in <OpenPositions>"""

    side: enums.LongShort | None = None
    assetCategory: enums.AssetClass | None = None
    subCategory: str | None = None
    accountId: str | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    reportDate: datetime.date | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    cusip: str | None = None
    isin: str | None = None
    figi: str | None = None
    multiplier: decimal.Decimal | None = None
    position: decimal.Decimal | None = None
    markPrice: decimal.Decimal | None = None
    positionValue: decimal.Decimal | None = None
    openPrice: decimal.Decimal | None = None
    costBasisPrice: decimal.Decimal | None = None
    costBasisMoney: decimal.Decimal | None = None
    fifoPnlUnrealized: decimal.Decimal | None = None
    levelOfDetail: str | None = None
    openDateTime: datetime.datetime | None = None
    holdingPeriodDateTime: datetime.datetime | None = None
    securityIDType: str | None = None
    issuer: str | None = None
    issuerCountryCode: str | None = None
    underlyingConid: str | None = None
    underlyingSymbol: str | None = None
    code: tuple[enums.Code, ...] = ()
    originatingOrderID: str | None = None
    originatingTransactionID: str | None = None
    accruedInt: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    sedol: str | None = None
    percentOfNAV: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    listingExchange: str | None = None
    underlyingSecurityID: str | None = None
    underlyingListingExchange: str | None = None
    positionValueInBase: decimal.Decimal | None = None
    unrealizedCapitalGainsPnl: decimal.Decimal | None = None
    unrealizedlFxPnl: decimal.Decimal | None = None
    vestingDate: datetime.date | None = None
    serialNumber: str | None = None
    deliveryType: str | None = None
    commodityType: str | None = None
    fineness: decimal.Decimal | None = None
    weight: str | None = None


@dataclass(frozen=True)
class FxLot(FlexElement):
    """Wrapped in <FxLots>, which in turn is wrapped in <FxPositions>"""

    assetCategory: enums.AssetClass | None = None
    accountId: str | None = None
    reportDate: datetime.date | None = None
    functionalCurrency: str | None = None
    fxCurrency: str | None = None
    quantity: decimal.Decimal | None = None
    costPrice: decimal.Decimal | None = None
    costBasis: decimal.Decimal | None = None
    closePrice: decimal.Decimal | None = None
    value: decimal.Decimal | None = None
    unrealizedPL: decimal.Decimal | None = None
    code: tuple[enums.Code, ...] = ()
    lotDescription: str | None = None
    lotOpenDateTime: datetime.datetime | None = None
    levelOfDetail: str | None = None
    acctAlias: str | None = None
    model: str | None = None


@dataclass(frozen=True)
class Trade(FlexElement):
    """Wrapped in <Trades>"""

    transactionType: enums.TradeType | None = None
    openCloseIndicator: enums.OpenClose | None = None
    buySell: enums.BuySell | None = None
    orderType: enums.OrderType | None = None
    assetCategory: enums.AssetClass | None = None
    accountId: str | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    symbol: str | None = None                            # symbol of instrument traded, e.g. AAPL, not unique in IBKR as it can exist on different exchanges: (symbol, Exchange, Currency, Asset Type) is unique
    conid: str | None = None                             # IBKR identifier of instrument, unique key within IBKR
    cusip: str | None = None                             # S&P instrument ID, not unique as it is used on different exchanges
    isin: str | None = None                              # instrument ISIN (ISO standardized instrument ID)
    figi: str | None = None                              # instrument FIGI (Bloomberg ID - comparable to ISIN)
    description: str | None = None                       # instrument name, e.g. "Apple Inc."
    listingExchange: str | None = None                   # exchange, e.g. "NASDAQ"
    multiplier: decimal.Decimal | None = None            # multiplier of contract traded
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    tradeID: str | None = None
    reportDate: datetime.date | None = None              # when the trade was included in IBKR's reporting system (e.g. corrections)
    tradeDate: datetime.date | None = None               # date of the trade
    tradeTime: datetime.time | None = None               # timestamp of the trade
    settleDateTarget: datetime.date | None = None        # expected date of ownership transfer
    exchange: str | None = None
    quantity: decimal.Decimal | None = None
    tradePrice: decimal.Decimal | None = None
    tradeMoney: decimal.Decimal | None = None            # TradeMoney = Proceeds + Fees + Commissions
    proceeds: decimal.Decimal | None = None              # Proceeds = Quantity * TradePrice * Multiplier
    netCash: decimal.Decimal | None = None               # netCash = TradeMoney - Adjustments (e.g. fees in physical execution of options, or taxes)
    netCashInBase: decimal.Decimal | None = None         # = NetCash × FX Rate
    taxes: decimal.Decimal | None = None
    ibCommission: decimal.Decimal | None = None
    ibCommissionCurrency: str | None = None
    closePrice: decimal.Decimal | None = None           # closing market price of the asset on the trade date
    notes: tuple[enums.Code, ...] = ()  # separator = ";"
    cost: decimal.Decimal | None = None
    mtmPnl: decimal.Decimal | None = None               # PnL at the time of reportins
    origTradePrice: decimal.Decimal | None = None
    origTradeDate: datetime.date | None = None
    origTradeID: str | None = None
    origOrderID: str | None = None
    openDateTime: datetime.datetime | None = None
    fifoPnlRealized: decimal.Decimal | None = None
    capitalGainsPnl: decimal.Decimal | None = None
    levelOfDetail: str | None = None
    ibOrderID: str | None = None
    # Despite the name, `orderTime` actually contains date/time data.
    orderTime: datetime.datetime | None = None
    changeInPrice: decimal.Decimal | None = None
    changeInQuantity: decimal.Decimal | None = None
    fxPnl: decimal.Decimal | None = None
    clearingFirmID: str | None = None
    #  Effective 2013, every Trade has a `transactionID` attribute that can't
    #  be deselected in the Flex query template.
    transactionID: str | None = None
    holdingPeriodDateTime: datetime.datetime | None = None
    ibExecID: str | None = None
    brokerageOrderID: str | None = None
    orderReference: str | None = None
    volatilityOrderLink: str | None = None
    exchOrderId: str | None = None
    extExecID: str | None = None
    traderID: str | None = None
    isAPIOrder: bool | None = None
    acctAlias: str | None = None
    model: str | None = None                   # some clients use model portfolios in account, i.e. virtual sub-accounts
    securityID: str | None = None
    securityIDType: str | None = None
    principalAdjustFactor: decimal.Decimal | None = None   # relevant e.g. in stock splits
    dateTime: datetime.datetime | None = None
    underlyingConid: str | None = None
    underlyingSecurityID: str | None = None
    underlyingSymbol: str | None = None
    underlyingListingExchange: str | None = None
    issuer: str | None = None
    sedol: str | None = None
    whenRealized: datetime.datetime | None = None
    whenReopened: datetime.datetime | None = None
    accruedInt: decimal.Decimal | None = None
    serialNumber: str | None = None
    deliveryType: str | None = None
    commodityType: str | None = None
    fineness: decimal.Decimal | None = None
    weight: str | None = None
    relatedTradeID: str | None = None
    relatedTransactionID: str | None = None
    origTransactionID: str | None = None
    subCategory: str | None = None
    issuerCountryCode: str | None = None
    rtn: str | None = None
    initialInvestment: bool | None = None
    positionActionID: str | None = None


@dataclass(frozen=True)
class TransferLot(FlexElement):
    """Wrapped in <Transfers>"""

    accountId: str | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    assetCategory: enums.AssetClass | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    securityIDType: str | None = None
    cusip: str | None = None
    isin: str | None = None
    listingExchange: str | None = None
    multiplier: decimal.Decimal | None = None
    reportDate: datetime.date | None = None
    date: datetime.date | None = None
    dateTime: datetime.datetime | None = None
    type: enums.TransferType | None = None
    direction: enums.InOut | None = None
    company: str | None = None
    account: str | None = None
    deliveringBroker: str | None = None
    quantity: decimal.Decimal | None = None
    transferPrice: decimal.Decimal | None = None
    pnlAmount: decimal.Decimal | None = None
    pnlAmountInBase: decimal.Decimal | None = None
    code: tuple[enums.Code, ...] = ()
    acctAlias: str | None = None
    model: str | None = None
    underlyingConid: str | None = None
    underlyingSymbol: str | None = None
    underlyingSecurityID: str | None = None
    underlyingListingExchange: str | None = None
    issuer: str | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    accountName: str | None = None
    positionAmount: decimal.Decimal | None = None
    positionAmountInBase: decimal.Decimal | None = None
    cashTransfer: decimal.Decimal | None = None
    clientReference: str | None = None
    transactionID: str | None = None
    serialNumber: str | None = None
    deliveryType: str | None = None
    commodityType: str | None = None
    fineness: decimal.Decimal | None = None
    weight: str | None = None


@dataclass(frozen=True)
class Lot(FlexElement):
    """Wrapped in <Trades>"""

    transactionType: enums.TradeType | None = None
    openCloseIndicator: enums.OpenClose | None = None
    buySell: enums.BuySell | None = None
    orderType: enums.OrderType | None = None
    assetCategory: enums.AssetClass | None = None
    accountId: str | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    cusip: str | None = None
    isin: str | None = None
    listingExchange: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    tradeID: str | None = None
    reportDate: datetime.date | None = None
    tradeDate: datetime.date | None = None
    tradeTime: datetime.time | None = None
    settleDateTarget: datetime.date | None = None
    exchange: str | None = None
    quantity: decimal.Decimal | None = None
    tradePrice: decimal.Decimal | None = None
    tradeMoney: decimal.Decimal | None = None
    taxes: decimal.Decimal | None = None
    ibCommission: decimal.Decimal | None = None
    ibCommissionCurrency: str | None = None
    netCash: decimal.Decimal | None = None
    netCashInBase: decimal.Decimal | None = None
    closePrice: decimal.Decimal | None = None
    notes: tuple[enums.Code, ...] = ()  # separator = ";"
    cost: decimal.Decimal | None = None
    mtmPnl: decimal.Decimal | None = None
    origTradePrice: decimal.Decimal | None = None
    origTradeDate: datetime.date | None = None
    origTradeID: str | None = None
    origOrderID: str | None = None
    openDateTime: datetime.datetime | None = None
    fifoPnlRealized: decimal.Decimal | None = None
    capitalGainsPnl: decimal.Decimal | None = None
    levelOfDetail: str | None = None
    ibOrderID: str | None = None
    # Despite the name, `orderTime` actually contains date/time data.
    orderTime: datetime.datetime | None = None
    changeInPrice: decimal.Decimal | None = None
    changeInQuantity: decimal.Decimal | None = None
    proceeds: decimal.Decimal | None = None
    fxPnl: decimal.Decimal | None = None
    clearingFirmID: str | None = None
    #  Effective 2013, every Trade has a `transactionID` attribute that can't
    #  be deselected in the Flex query template.
    transactionID: str | None = None
    holdingPeriodDateTime: datetime.datetime | None = None
    ibExecID: str | None = None
    brokerageOrderID: str | None = None
    orderReference: str | None = None
    volatilityOrderLink: str | None = None
    exchOrderId: str | None = None
    extExecID: str | None = None
    traderID: str | None = None
    isAPIOrder: bool | None = None
    acctAlias: str | None = None
    model: str | None = None
    securityID: str | None = None
    securityIDType: str | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    dateTime: datetime.datetime | None = None
    underlyingConid: str | None = None
    underlyingSecurityID: str | None = None
    underlyingSymbol: str | None = None
    underlyingListingExchange: str | None = None
    issuer: str | None = None
    sedol: str | None = None
    whenRealized: datetime.datetime | None = None
    whenReopened: datetime.datetime | None = None
    accruedInt: decimal.Decimal | None = None
    serialNumber: str | None = None
    deliveryType: str | None = None
    commodityType: str | None = None
    fineness: decimal.Decimal | None = None
    weight: str | None = None
    origTransactionID: str | None = None
    relatedTransactionID: str | None = None
    subCategory: str | None = None
    figi: str | None = None
    issuerCountryCode: str | None = None
    relatedTradeID: str | None = None
    rtn: str | None = None
    initialInvestment: bool | None = None
    positionActionID: str | None = None


@dataclass(frozen=True)
class UnbundledCommissionDetail(FlexElement):
    """Wrapped in <UnbundledCommissionDetails>"""

    buySell: enums.BuySell | None = None
    assetCategory: enums.AssetClass | None = None
    accountId: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    securityIDType: str | None = None
    cusip: str | None = None
    isin: str | None = None
    sedol: str | None = None
    listingExchange: str | None = None
    underlyingConid: str | None = None
    underlyingSymbol: str | None = None
    underlyingSecurityID: str | None = None
    underlyingListingExchange: str | None = None
    issuer: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    dateTime: datetime.datetime | None = None
    exchange: str | None = None
    quantity: decimal.Decimal | None = None
    price: decimal.Decimal | None = None
    tradeID: str | None = None
    orderReference: str | None = None
    totalCommission: decimal.Decimal | None = None
    brokerExecutionCharge: decimal.Decimal | None = None
    brokerClearingCharge: decimal.Decimal | None = None
    thirdPartyExecutionCharge: decimal.Decimal | None = None
    thirdPartyClearingCharge: decimal.Decimal | None = None
    thirdPartyRegulatoryCharge: decimal.Decimal | None = None
    regFINRATradingActivityFee: decimal.Decimal | None = None
    regSection31TransactionFee: decimal.Decimal | None = None
    regOther: decimal.Decimal | None = None
    other: decimal.Decimal | None = None
    subCategory: str | None = None
    figi: str | None = None
    issuerCountryCode: str | None = None
    serialNumber: decimal.Decimal | None = None
    deliveryType: decimal.Decimal | None = None     # 0: Cash settlement, 1: physical settlement
    commodityType: str | None = None                # z.B. "STK"=Aktie, "BND"=Anleihe, etc.
    fineness: decimal.Decimal | None = None         # Reinheitsgrad bei Edelmetallen, z.B. 925 für 925 Sterling Silber
    weight: decimal.Decimal | None = None           # Gewicht - Einheit ist Rohstoffabhängig

@dataclass(frozen=True)
class SymbolSummary(FlexElement):
    """Wrapped in <TradeConfirms>"""

    accountId: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    currency: str | None = None
    assetCategory: enums.AssetClass | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    securityIDType: str | None = None
    cusip: str | None = None
    isin: str | None = None
    listingExchange: str | None = None
    underlyingConid: str | None = None
    underlyingSymbol: str | None = None
    underlyingSecurityID: str | None = None
    underlyingListingExchange: str | None = None
    issuer: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    transactionType: enums.TradeType | None = None
    tradeID: str | None = None
    orderID: decimal.Decimal | None = None
    execID: str | None = None
    brokerageOrderID: str | None = None
    orderReference: str | None = None
    volatilityOrderLink: str | None = None
    clearingFirmID: str | None = None
    origTradePrice: decimal.Decimal | None = None
    origTradeDate: datetime.date | None = None
    origTradeID: str | None = None
    #  Despite the name, `orderTime` actually contains date/time data.
    orderTime: datetime.datetime | None = None
    dateTime: datetime.datetime | None = None
    reportDate: datetime.date | None = None
    settleDate: datetime.date | None = None
    tradeDate: datetime.date | None = None
    exchange: str | None = None
    buySell: enums.BuySell | None = None
    quantity: decimal.Decimal | None = None
    price: decimal.Decimal | None = None
    amount: decimal.Decimal | None = None
    proceeds: decimal.Decimal | None = None
    commission: decimal.Decimal | None = None
    brokerExecutionCommission: decimal.Decimal | None = None
    brokerClearingCommission: decimal.Decimal | None = None
    thirdPartyExecutionCommission: decimal.Decimal | None = None
    thirdPartyClearingCommission: decimal.Decimal | None = None
    thirdPartyRegulatoryCommission: decimal.Decimal | None = None
    otherCommission: decimal.Decimal | None = None
    commissionCurrency: str | None = None
    tax: decimal.Decimal | None = None
    code: tuple[enums.Code, ...] = ()
    orderType: enums.OrderType | None = None
    levelOfDetail: str | None = None
    traderID: str | None = None
    isAPIOrder: bool | None = None
    allocatedTo: str | None = None
    accruedInt: decimal.Decimal | None = None
    fxRateToBase: decimal.Decimal | None = None
    subCategory: str | None = None
    figi: str | None = None
    issuerCountryCode: str | None = None
    relatedTradeID: str | None = None
    origTransactionID: str | None = None
    relatedTransactionID: str | None = None
    positionActionID: str | None = None
    ibExecID: str | None = None
    extExecID: str | None = None
    exchOrderId: str | None = None
    transactionID: str | None = None
    openDateTime: datetime.datetime | None = None
    holdingPeriodDateTime: datetime.datetime | None = None
    settleDateTarget: datetime.date | None = None
    taxes: decimal.Decimal | None = None
    tradePrice: decimal.Decimal | None = None
    tradeMoney: decimal.Decimal | None = None
    changeInPrice: decimal.Decimal | None = None
    changeInQuantity: decimal.Decimal | None = None
    closePrice: decimal.Decimal | None = None
    commodityType: str | None = None
    cost: decimal.Decimal | None = None
    deliveryType: str | None = None
    fifoPnlRealized: decimal.Decimal | None = None
    fineness: decimal.Decimal | None = None
    ibCommission: decimal.Decimal | None = None
    ibCommissionCurrency: str | None = None
    ibOrderID: str | None = None
    initialInvestment: bool | None = None
    mtmPnl: decimal.Decimal | None = None
    netCash: decimal.Decimal | None = None
    netCashInBase: decimal.Decimal | None = None
    notes: str | None = None
    openCloseIndicator: enums.OpenClose | None = None
    origOrderID: str | None = None
    rtn: str | None = None
    serialNumber: str | None = None
    weight: str | None = None
    whenRealized: datetime.datetime | None = None
    whenReopened: datetime.datetime | None = None


@dataclass(frozen=True)
class AssetSummary(FlexElement):
    """Wrapped in <TradeConfirms>"""

    accountId: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    currency: str | None = None
    assetCategory: enums.AssetClass | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    securityIDType: str | None = None
    cusip: str | None = None
    isin: str | None = None
    listingExchange: str | None = None
    underlyingConid: str | None = None
    underlyingSymbol: str | None = None
    underlyingSecurityID: str | None = None
    underlyingListingExchange: str | None = None
    issuer: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    transactionType: enums.TradeType | None = None
    tradeID: str | None = None
    orderID: decimal.Decimal | None = None
    execID: str | None = None
    brokerageOrderID: str | None = None
    orderReference: str | None = None
    volatilityOrderLink: str | None = None
    clearingFirmID: str | None = None
    origTradePrice: decimal.Decimal | None = None
    TradePrice: decimal.Decimal | None = None
    tradeMoney: decimal.Decimal | None = None
    taxes: decimal.Decimal | None = None
    origTradeDate: datetime.date | None = None
    origTradeID: str | None = None
    tradePrice: decimal.Decimal | None = None
    #  Despite the name, `orderTime` actually contains date/time data.
    orderTime: datetime.datetime | None = None
    exchOrderId: str | None = None
    dateTime: datetime.datetime | None = None
    fxRateToBase: decimal.Decimal | None = None
    reportDate: datetime.date | None = None
    ibExecID: str | None = None
    settleDateTarget: datetime.date | None = None
    cost: decimal.Decimal | None = None
    extExecID: str | None = None
    openDateTime: datetime.datetime | None = None
    holdingPeriodDateTime: datetime.datetime | None = None
    whenRealized: datetime.datetime | None = None
    whenReopened: datetime.datetime | None = None
    changeInPrice: decimal.Decimal | None = None
    changeInQuantity: decimal.Decimal | None = None
    ibOrderID: str | None = None
    origOrderID: str | None = None
    transactionID: str | None = None
    tradeDate: datetime.date | None = None
    openCloseIndicator: enums.OpenClose | None = None
    notes: str | None = None
    fxPnl: decimal.Decimal | None = None
    mtmPnl: decimal.Decimal | None = None
    fifoPnlRealized: decimal.Decimal | None = None
    closePrice: decimal.Decimal | None = None
    exchange: str | None = None
    ibCommission: decimal.Decimal | None = None
    ibCommissionCurrency: str | None = None
    netCash: decimal.Decimal | None = None
    netCashInBase: decimal.Decimal | None = None
    buySell: enums.BuySell | None = None
    quantity: decimal.Decimal | None = None
    price: decimal.Decimal | None = None
    amount: decimal.Decimal | None = None
    proceeds: decimal.Decimal | None = None
    commission: decimal.Decimal | None = None
    brokerExecutionCommission: decimal.Decimal | None = None
    brokerClearingCommission: decimal.Decimal | None = None
    thirdPartyExecutionCommission: decimal.Decimal | None = None
    thirdPartyClearingCommission: decimal.Decimal | None = None
    thirdPartyRegulatoryCommission: decimal.Decimal | None = None
    otherCommission: decimal.Decimal | None = None
    commissionCurrency: str | None = None
    tax: decimal.Decimal | None = None
    code: tuple[enums.Code, ...] = ()
    orderType: enums.OrderType | None = None
    levelOfDetail: str | None = None
    traderID: str | None = None
    isAPIOrder: bool | None = None
    allocatedTo: str | None = None
    accruedInt: decimal.Decimal | None = None
    deliveryType: str | None = None
    serialNumber: str | None = None
    commodityType: str | None = None
    fineness: decimal.Decimal | None = None
    weight: str | None = None
    subCategory: str | None = None
    figi: str | None = None
    issuerCountryCode: str | None = None
    relatedTradeID: str | None = None
    origTransactionID: str | None = None
    relatedTransactionID: str | None = None
    rtn: str | None = None
    initialInvestment: bool | None = None
    positionActionID: str | None = None


@dataclass(frozen=True)
class Order(FlexElement):
    """Wrapped in <TradeConfirms> or <Trades>"""

    accountId: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    currency: str | None = None
    assetCategory: enums.AssetClass | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    securityIDType: str | None = None
    cusip: str | None = None
    isin: str | None = None
    listingExchange: str | None = None
    underlyingConid: str | None = None
    underlyingSymbol: str | None = None
    underlyingSecurityID: str | None = None
    underlyingListingExchange: str | None = None
    issuer: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    transactionType: enums.TradeType | None = None
    tradeID: str | None = None
    orderID: decimal.Decimal | None = None
    execID: str | None = None
    brokerageOrderID: str | None = None
    orderReference: str | None = None
    volatilityOrderLink: str | None = None
    clearingFirmID: str | None = None
    origTradePrice: decimal.Decimal | None = None
    origTradeDate: datetime.date | None = None
    origTradeID: str | None = None
    #  Despite the name, `orderTime` actually contains date/time data.
    orderTime: datetime.datetime | None = None
    dateTime: datetime.datetime | None = None
    reportDate: datetime.date | None = None
    settleDate: datetime.date | None = None
    tradeDate: datetime.date | None = None
    exchange: str | None = None
    buySell: enums.BuySell | None = None
    quantity: decimal.Decimal | None = None
    price: decimal.Decimal | None = None
    amount: decimal.Decimal | None = None
    proceeds: decimal.Decimal | None = None
    commission: decimal.Decimal | None = None
    brokerExecutionCommission: decimal.Decimal | None = None
    brokerClearingCommission: decimal.Decimal | None = None
    thirdPartyExecutionCommission: decimal.Decimal | None = None
    thirdPartyClearingCommission: decimal.Decimal | None = None
    thirdPartyRegulatoryCommission: decimal.Decimal | None = None
    otherCommission: decimal.Decimal | None = None
    commissionCurrency: str | None = None
    tax: decimal.Decimal | None = None
    code: tuple[enums.Code, ...] = ()
    orderType: enums.OrderType | None = None
    levelOfDetail: str | None = None
    traderID: str | None = None
    isAPIOrder: bool | None = None
    allocatedTo: str | None = None
    accruedInt: decimal.Decimal | None = None
    netCash: decimal.Decimal | None = None
    tradePrice: decimal.Decimal | None = None
    ibCommission: decimal.Decimal | None = None
    ibOrderID: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    settleDateTarget: datetime.date | None = None
    tradeMoney: decimal.Decimal | None = None
    taxes: decimal.Decimal | None = None
    ibCommissionCurrency: str | None = None
    closePrice: decimal.Decimal | None = None
    openCloseIndicator: enums.OpenClose | None = None
    notes: str | None = None
    cost: decimal.Decimal | None = None
    fifoPnlRealized: decimal.Decimal | None = None
    fxPnl: decimal.Decimal | None = None
    mtmPnl: decimal.Decimal | None = None
    origOrderID: str | None = None
    transactionID: str | None = None
    ibExecID: str | None = None
    exchOrderId: str | None = None
    extExecID: str | None = None
    openDateTime: datetime.datetime | None = None
    holdingPeriodDateTime: datetime.datetime | None = None
    whenRealized: datetime.datetime | None = None
    whenReopened: datetime.datetime | None = None
    changeInPrice: decimal.Decimal | None = None
    changeInQuantity: decimal.Decimal | None = None
    subCategory: str | None = None
    figi: str | None = None
    issuerCountryCode: str | None = None
    relatedTradeID: str | None = None
    origTransactionID: str | None = None
    relatedTransactionID: str | None = None
    rtn: str | None = None
    initialInvestment: bool | None = None
    serialNumber: str | None = None
    deliveryType: str | None = None
    commodityType: str | None = None
    fineness: decimal.Decimal | None = None
    weight: str | None = None
    positionActionID: str | None = None


@dataclass(frozen=True)
class TradeConfirm(FlexElement):
    """Wrapped in <TradeConfirms>"""

    transactionType: enums.TradeType | None = None
    openCloseIndicator: enums.OpenClose | None = None
    buySell: enums.BuySell | None = None
    orderType: enums.OrderType | None = None
    assetCategory: enums.AssetClass | None = None
    accountId: str | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    rfqID: str | None = None
    securityIDType: str | None = None
    cusip: str | None = None
    isin: str | None = None
    underlyingConid: str | None = None
    underlyingSymbol: str | None = None
    issuer: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    tradeID: str | None = None
    reportDate: datetime.date | None = None
    tradeDate: datetime.date | None = None
    tradeTime: datetime.time | None = None
    settleDateTarget: datetime.date | None = None
    exchange: str | None = None
    quantity: decimal.Decimal | None = None
    tradePrice: decimal.Decimal | None = None
    tradeMoney: decimal.Decimal | None = None
    proceeds: decimal.Decimal | None = None
    taxes: decimal.Decimal | None = None
    ibCommission: decimal.Decimal | None = None
    ibCommissionCurrency: str | None = None
    netCash: decimal.Decimal | None = None
    closePrice: decimal.Decimal | None = None
    notes: tuple[enums.Code, ...] = ()  # separator = ";"
    cost: decimal.Decimal | None = None
    fifoPnlRealized: decimal.Decimal | None = None
    fxPnl: decimal.Decimal | None = None
    mtmPnl: decimal.Decimal | None = None
    origTradePrice: decimal.Decimal | None = None
    origTradeDate: datetime.date | None = None
    origTradeID: str | None = None
    origOrderID: str | None = None
    clearingFirmID: str | None = None
    transactionID: str | None = None
    openDateTime: datetime.datetime | None = None
    holdingPeriodDateTime: datetime.datetime | None = None
    whenRealized: datetime.datetime | None = None
    whenReopened: datetime.datetime | None = None
    levelOfDetail: str | None = None
    commissionCurrency: str | None = None
    price: decimal.Decimal | None = None
    thirdPartyClearingCommission: decimal.Decimal | None = None
    orderID: decimal.Decimal | None = None
    allocatedTo: str | None = None
    thirdPartyRegulatoryCommission: decimal.Decimal | None = None
    dateTime: datetime.datetime | None = None
    brokerExecutionCommission: decimal.Decimal | None = None
    thirdPartyExecutionCommission: decimal.Decimal | None = None
    amount: decimal.Decimal | None = None
    otherCommission: decimal.Decimal | None = None
    commission: decimal.Decimal | None = None
    brokerClearingCommission: decimal.Decimal | None = None
    ibOrderID: str | None = None
    ibExecID: str | None = None
    execID: str | None = None
    brokerageOrderID: str | None = None
    orderReference: str | None = None
    volatilityOrderLink: str | None = None
    exchOrderId: str | None = None
    extExecID: str | None = None
    #  Despite the name, `orderTime` actually contains date/time data.
    orderTime: datetime.datetime | None = None
    changeInPrice: decimal.Decimal | None = None
    changeInQuantity: decimal.Decimal | None = None
    traderID: str | None = None
    isAPIOrder: bool | None = None
    code: tuple[enums.Code, ...] = ()
    tax: decimal.Decimal | None = None
    listingExchange: str | None = None
    underlyingListingExchange: str | None = None
    settleDate: datetime.date | None = None
    underlyingSecurityID: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    accruedInt: decimal.Decimal | None = None
    relatedTradeID: str | None = None
    relatedTransactionID: str | None = None
    blockID: str | None = None


@dataclass(frozen=True)
class OptionEAE(FlexElement):
    """Option Exercise Assignment or Expiration

    Wrapped in (identically-named) <OptionEAE>
    """

    transactionType: enums.OptionAction | None = None
    assetCategory: enums.AssetClass | None = None
    accountId: str | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    securityIDType: str | None = None
    cusip: str | None = None
    isin: str | None = None
    listingExchange: str | None = None
    underlyingSecurityID: str | None = None
    underlyingListingExchange: str | None = None
    underlyingConid: str | None = None
    underlyingSymbol: str | None = None
    issuer: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    date: datetime.date | None = None
    quantity: decimal.Decimal | None = None
    tradePrice: decimal.Decimal | None = None
    markPrice: decimal.Decimal | None = None
    proceeds: decimal.Decimal | None = None
    commisionsAndTax: decimal.Decimal | None = None
    costBasis: decimal.Decimal | None = None
    realizedPnl: decimal.Decimal | None = None
    capitalGainsPnl: decimal.Decimal | None = None
    fxPnl: decimal.Decimal | None = None
    mtmPnl: decimal.Decimal | None = None
    tradeID: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    relatedTradeID: str | None = None
    subCategory: str | None = None
    figi: str | None = None
    issuerCountryCode: str | None = None
    origTransactionID: str | None = None
    relatedTransactionID: str | None = None
    rtn: str | None = None
    initialInvestment: bool | None = None
    serialNumber: str | None = None
    deliveryType: str | None = None
    commodityType: str | None = None
    fineness: decimal.Decimal | None = None
    weight: str | None = None


#  Type alias to work around https://github.com/python/mypy/issues/1775
_OptionEAE = OptionEAE


@dataclass(frozen=True)
class TradeTransfer(FlexElement):
    """Wrapped in <TradeTransfers>"""

    transactionType: enums.TradeType | None = None
    openCloseIndicator: enums.OpenClose | None = None
    direction: enums.ToFrom | None = None
    deliveredReceived: enums.DeliveredReceived | None = None
    assetCategory: enums.AssetClass | None = None
    accountId: str | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    cusip: str | None = None
    isin: str | None = None
    underlyingConid: str | None = None
    tradeID: str | None = None
    reportDate: datetime.date | None = None
    tradeDate: datetime.date | None = None
    tradeTime: datetime.time | None = None
    settleDateTarget: datetime.date | None = None
    exchange: str | None = None
    quantity: decimal.Decimal | None = None
    tradePrice: decimal.Decimal | None = None
    tradeMoney: decimal.Decimal | None = None
    taxes: decimal.Decimal | None = None
    ibCommission: decimal.Decimal | None = None
    ibCommissionCurrency: str | None = None
    closePrice: decimal.Decimal | None = None
    notes: tuple[enums.Code, ...] = ()  # separator = ";"
    cost: decimal.Decimal | None = None
    fifoPnlRealized: decimal.Decimal | None = None
    mtmPnl: decimal.Decimal | None = None
    brokerName: str | None = None
    brokerAccount: str | None = None
    awayBrokerCommission: decimal.Decimal | None = None
    regulatoryFee: decimal.Decimal | None = None
    netTradeMoney: decimal.Decimal | None = None
    netTradeMoneyInBase: decimal.Decimal | None = None
    netTradePrice: decimal.Decimal | None = None
    multiplier: decimal.Decimal | None = None
    acctAlias: str | None = None
    model: str | None = None
    sedol: str | None = None
    securityID: str | None = None
    underlyingSymbol: str | None = None
    issuer: str | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    proceeds: decimal.Decimal | None = None
    fxPnl: decimal.Decimal | None = None
    netCash: decimal.Decimal | None = None
    origTradePrice: decimal.Decimal | None = None
    # Oddly, `origTradeDate` appears to have hard-coded YYYYMMDD format
    # instead of the date format from the report configuration.
    origTradeDate: datetime.date | None = None
    origTradeID: str | None = None
    origOrderID: str | None = None
    clearingFirmID: str | None = None
    transactionID: str | None = None
    openDateTime: datetime.datetime | None = None
    holdingPeriodDateTime: datetime.datetime | None = None
    whenRealized: datetime.datetime | None = None
    whenReopened: datetime.datetime | None = None
    levelOfDetail: str | None = None
    securityIDType: str | None = None


@dataclass(frozen=True)
class InterestAccrualsCurrency(FlexElement):
    """Wrapped in <InterestAccruals>"""

    accountId: str | None = None
    currency: str | None = None
    fromDate: datetime.date | None = None
    toDate: datetime.date | None = None
    startingAccrualBalance: decimal.Decimal | None = None
    interestAccrued: decimal.Decimal | None = None
    accrualReversal: decimal.Decimal | None = None
    endingAccrualBalance: decimal.Decimal | None = None
    acctAlias: str | None = None
    model: str | None = None
    fxTranslation: decimal.Decimal | None = None


@dataclass(frozen=True)
class TierInterestDetail(FlexElement):
    accountId: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    interestType: str | None = None
    valueDate: datetime.date | None = None
    tierBreak: str | None = None
    balanceThreshold: decimal.Decimal | None = None
    securitiesPrincipal: decimal.Decimal | None = None
    commoditiesPrincipal: decimal.Decimal | None = None
    ibuklPrincipal: decimal.Decimal | None = None
    totalPrincipal: decimal.Decimal | None = None
    rate: decimal.Decimal | None = None
    securitiesInterest: decimal.Decimal | None = None
    commoditiesInterest: decimal.Decimal | None = None
    ibuklInterest: decimal.Decimal | None = None
    totalInterest: decimal.Decimal | None = None
    code: tuple[enums.Code, ...] = ()
    fromAcct: str | None = None
    toAcct: str | None = None
    reportDate: datetime.date | None = None
    marginBalance: decimal.Decimal | None = None

@dataclass(frozen=True)
class HardToBorrowDetail(FlexElement):
    """Wrapped in <HardToBorrowDetails>"""

    assetCategory: enums.AssetClass | None = None
    accountId: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    securityIDType: str | None = None
    cusip: str | None = None
    isin: str | None = None
    listingExchange: str | None = None
    underlyingConid: str | None = None
    underlyingSymbol: str | None = None
    underlyingSecurityID: str | None = None
    underlyingListingExchange: str | None = None
    issuer: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    valueDate: datetime.date | None = None
    quantity: decimal.Decimal | None = None
    price: decimal.Decimal | None = None
    value: decimal.Decimal | None = None
    borrowFeeRate: decimal.Decimal | None = None
    borrowFee: decimal.Decimal | None = None
    code: tuple[enums.Code, ...] = ()
    fromAcct: str | None = None
    toAcct: str | None = None


@dataclass(frozen=True)
class SLBActivity(FlexElement):
    """Wrapped in <SLBActivities>"""

    assetCategory: enums.AssetClass | None = None
    accountId: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    securityIDType: str | None = None
    cusip: str | None = None
    isin: str | None = None
    underlyingConid: str | None = None
    underlyingSymbol: str | None = None
    issuer: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    date: datetime.date | None = None
    slbTransactionId: str | None = None
    activityDescription: str | None = None
    type: str | None = None
    exchange: str | None = None
    quantity: decimal.Decimal | None = None
    feeRate: decimal.Decimal | None = None
    collateralAmount: decimal.Decimal | None = None
    markQuantity: decimal.Decimal | None = None
    markPriorPrice: decimal.Decimal | None = None
    markCurrentPrice: decimal.Decimal | None = None
    subCategory: str | None = None
    figi: str | None = None
    listingExchange: str | None = None
    underlyingSecurityID: str | None = None
    underlyingListingExchange: str | None = None
    issuerCountryCode: str | None = None
    serialNumber: decimal.Decimal | None = None
    deliveryType: decimal.Decimal | None = None
    commodityType: str | None = None
    fineness: decimal.Decimal | None = None
    weight: decimal.Decimal | None = None

@dataclass(frozen=True)
class SLBFee:
    """Wrapped in <SLBFees>"""

    accountId: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    currency: str | None = None
    fxRateToBase: str | None = None
    assetCategory: str | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    securityIDType: str | None = None
    cusip: str | None = None
    isin: str | None = None
    listingExchange: str | None = None
    underlyingConid: str | None = None
    underlyingSymbol: str | None = None
    underlyingSecurityID: str | None = None
    underlyingListingExchange: str | None = None
    issuer: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    valueDate: datetime.date | None = None
    startDate: datetime.date | None = None
    type: str | None = None  # FIXME
    exchange: str | None = None
    quantity: decimal.Decimal | None = None
    collateralAmount: decimal.Decimal | None = None
    feeRate: decimal.Decimal | None = None
    fee: decimal.Decimal | None = None
    carryCharge: decimal.Decimal | None = None
    ticketCharge: decimal.Decimal | None = None
    totalCharges: decimal.Decimal | None = None
    marketFeeRate: decimal.Decimal | None = None
    grossLendFee: decimal.Decimal | None = None
    netLendFeeRate: decimal.Decimal | None = None
    netLendFee: decimal.Decimal | None = None
    code: tuple[enums.Code, ...] = ()
    fromAcct: str | None = None
    toAcct: str | None = None
    subCategory: str | None = None
    figi: str | None = None
    issuerCountryCode: str | None = None
    uniqueID: str | None = None
    serialNumber: decimal.Decimal | None = None
    deliveryType: decimal.Decimal | None = None
    commodityType: str | None = None
    fineness: decimal.Decimal | None = None
    weight: decimal.Decimal | None = None

@dataclass(frozen=True)
class Transfer(FlexElement):
    """Wrapped in <Transfers>"""

    type: enums.TransferType | None = None
    direction: enums.InOut | None = None
    assetCategory: enums.AssetClass | None = None
    subCategory: str | None = None
    accountId: str | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    cusip: str | None = None
    isin: str | None = None
    listingExchange: str | None = None
    underlyingSecurityID: str | None = None
    underlyingListingExchange: str | None = None
    reportDate: datetime.date | None = None
    underlyingConid: str | None = None
    date: datetime.date | None = None
    dateTime: datetime.datetime | None = None
    account: str | None = None
    deliveringBroker: str | None = None
    quantity: decimal.Decimal | None = None
    transferPrice: decimal.Decimal | None = None
    positionAmount: decimal.Decimal | None = None
    positionAmountInBase: decimal.Decimal | None = None
    capitalGainsPnl: decimal.Decimal | None = None
    cashTransfer: decimal.Decimal | None = None
    code: tuple[enums.Code, ...] = ()
    clientReference: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    sedol: str | None = None
    securityIDType: str | None = None
    underlyingSymbol: str | None = None
    issuer: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    company: str | None = None
    accountName: str | None = None
    pnlAmount: decimal.Decimal | None = None
    pnlAmountInBase: decimal.Decimal | None = None
    fxPnl: decimal.Decimal | None = None
    transactionID: str | None = None
    serialNumber: str | None = None
    deliveryType: str | None = None
    commodityType: str | None = None
    fineness: decimal.Decimal | None = None
    weight: str | None = None
    figi: str | None = None
    settleDate: datetime.date | None = None
    issuerCountryCode: str | None = None
    levelOfDetail: str | None = None
    positionInstructionID: str | None = None
    positionInstructionSetID: str | None = None


@dataclass(frozen=True)
class UnsettledTransfer(FlexElement):
    """Wrapped in <UnsettledTransfers>"""

    direction: enums.ToFrom | None = None
    assetCategory: enums.AssetClass | None = None
    accountId: str | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    cusip: str | None = None
    isin: str | None = None
    sedol: str | None = None
    underlyingConid: str | None = None
    stage: str | None = None
    tradeDate: datetime.date | None = None
    targetSettlement: datetime.date | None = None
    contra: str | None = None
    quantity: decimal.Decimal | None = None
    tradePrice: decimal.Decimal | None = None
    tradeAmount: decimal.Decimal | None = None
    tradeAmountInBase: decimal.Decimal | None = None
    transactionID: str | None = None


@dataclass(frozen=True)
class PriorPeriodPosition(FlexElement):
    """Wrapped in <PriorPeriodPositions>"""

    assetCategory: enums.AssetClass | None = None
    accountId: str | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    cusip: str | None = None
    isin: str | None = None
    listingExchange: str | None = None
    underlyingConid: str | None = None
    underlyingSecurityID: str | None = None
    underlyingListingExchange: str | None = None
    priorMtmPnl: decimal.Decimal | None = None
    date: datetime.date | None = None
    price: decimal.Decimal | None = None
    acctAlias: str | None = None
    model: str | None = None
    sedol: str | None = None
    securityIDType: str | None = None
    underlyingSymbol: str | None = None
    issuer: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    subCategory: str | None = None
    figi: str | None = None
    issuerCountryCode: str | None = None
    serialNumber: decimal.Decimal | None = None
    deliveryType: decimal.Decimal | None = None
    commodityType: str | None = None
    fineness: decimal.Decimal | None = None
    weight: decimal.Decimal | None = None

@dataclass(frozen=True)
class CorporateAction(FlexElement):
    """Wrapped in <CorporateActions>"""

    assetCategory: enums.AssetClass | None = None
    subCategory: str | None = None
    accountId: str | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    cusip: str | None = None
    isin: str | None = None
    listingExchange: str | None = None
    underlyingConid: str | None = None
    underlyingSecurityID: str | None = None
    underlyingListingExchange: str | None = None
    actionID: str | None = None
    actionDescription: str | None = None
    dateTime: datetime.datetime | None = None
    amount: decimal.Decimal | None = None
    quantity: decimal.Decimal | None = None
    fifoPnlRealized: decimal.Decimal | None = None
    capitalGainsPnl: decimal.Decimal | None = None
    fxPnl: decimal.Decimal | None = None
    mtmPnl: decimal.Decimal | None = None
    #  Effective 2010, CorporateAction has a `type` attribute
    type: enums.Reorg | None = None
    code: tuple[enums.Code, ...] = ()
    sedol: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    securityIDType: str | None = None
    underlyingSymbol: str | None = None
    issuer: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    reportDate: datetime.date | None = None
    proceeds: decimal.Decimal | None = None
    value: decimal.Decimal | None = None
    transactionID: str | None = None
    levelOfDetail: str | None = None
    serialNumber: str | None = None
    deliveryType: str | None = None
    commodityType: str | None = None
    fineness: decimal.Decimal | None = None
    weight: str | None = None
    figi: str | None = None
    issuerCountryCode: str | None = None
    costBasis: decimal.Decimal | None = None


@dataclass(frozen=True)
class FxTransaction(FlexElement):
    """Wrapped in <FxTransactions>"""

    assetCategory: enums.AssetClass | None = None
    accountId: str | None = None
    functionalCurrency: str | None = None
    fxCurrency: str | None = None
    quantity: decimal.Decimal | None = None
    proceeds: decimal.Decimal | None = None
    cost: decimal.Decimal | None = None
    realizedPL: decimal.Decimal | None = None
    activityDescription: str | None = None
    dateTime: datetime.datetime | None = None
    code: tuple[enums.Code, ...] = ()
    reportDate: datetime.date | None = None
    acctAlias: str | None = None
    model: str | None = None
    levelOfDetail: str | None = None


@dataclass(frozen=True)
class CashTransaction(FlexElement):
    """Wrapped in <CashTransactions>"""

    type: enums.CashAction | None = None
    assetCategory: enums.AssetClass | None = None
    subCategory: str | None = None
    accountId: str | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    cusip: str | None = None
    isin: str | None = None
    listingExchange: str | None = None
    underlyingConid: str | None = None
    underlyingSecurityID: str | None = None
    underlyingListingExchange: str | None = None
    amount: decimal.Decimal | None = None
    dateTime: datetime.datetime | None = None
    sedol: str | None = None
    symbol: str | None = None
    securityIDType: str | None = None
    underlyingSymbol: str | None = None
    issuer: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    tradeID: str | None = None
    code: tuple[enums.Code, ...] = ()
    transactionID: str | None = None
    reportDate: datetime.date | None = None
    clientReference: str | None = None
    settleDate: datetime.date | None = None
    acctAlias: str | None = None
    actionID: str | None = None
    model: str | None = None
    levelOfDetail: str | None = None
    serialNumber: str | None = None
    deliveryType: str | None = None
    commodityType: str | None = None
    fineness: decimal.Decimal | None = None
    weight: str | None = None
    figi: str | None = None
    issuerCountryCode: str | None = None
    availableForTradingDate: datetime.datetime | None = None
    exDate: datetime.datetime | None = None

@dataclass(frozen=True)
class DebitCardActivity(FlexElement):
    """Wrapped in <DebitCardActivities>"""

    accountId: str | None = None
    acctAlias: str | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    assetCategory: enums.AssetClass | None = None
    status: str | None = None
    reportDate: datetime.date | None = None
    postingDate: datetime.date | None = None
    transactionDateTime: datetime.datetime | None = None
    category: str | None = None
    merchantNameLocation: str | None = None
    amount: decimal.Decimal | None = None
    model: str | None = None


@dataclass(frozen=True)
class ChangeInDividendAccrual(FlexElement):
    """Wrapped in <ChangeInDividendAccruals>"""

    date: datetime.date | None = None
    assetCategory: enums.AssetClass | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    accountId: str | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    cusip: str | None = None
    isin: str | None = None
    sedol: str | None = None
    listingExchange: str | None = None
    underlyingSecurityID: str | None = None
    underlyingListingExchange: str | None = None
    reportDate: datetime.date | None = None
    underlyingConid: str | None = None
    exDate: datetime.date | None = None
    payDate: datetime.date | None = None
    quantity: decimal.Decimal | None = None
    tax: decimal.Decimal | None = None
    fee: decimal.Decimal | None = None
    grossRate: decimal.Decimal | None = None
    grossAmount: decimal.Decimal | None = None
    netAmount: decimal.Decimal | None = None
    code: tuple[enums.Code, ...] = ()
    securityIDType: str | None = None
    underlyingSymbol: str | None = None
    issuer: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    fromAcct: str | None = None
    toAcct: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    subCategory: str | None = None
    figi: str | None = None
    issuerCountryCode: str | None = None
    actionID: decimal.Decimal | None = None  #unique numerical ID
    levelOfDetail: str | None = None
    serialNumber: decimal.Decimal | None = None
    deliveryType: decimal.Decimal | None = None
    commodityType: str | None = None
    fineness: decimal.Decimal | None = None
    weight: decimal.Decimal | None = None

#  Type alias to work around https://github.com/python/mypy/issues/1775
_ChangeInDividendAccrual = ChangeInDividendAccrual


@dataclass(frozen=True)
class OpenDividendAccrual(FlexElement):
    """Wrapped in <OpenDividendAccruals>"""

    assetCategory: enums.AssetClass | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    accountId: str | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    cusip: str | None = None
    isin: str | None = None
    listingExchange: str | None = None
    underlyingConid: str | None = None
    underlyingSecurityID: str | None = None
    underlyingListingExchange: str | None = None
    exDate: datetime.date | None = None
    payDate: datetime.date | None = None
    quantity: decimal.Decimal | None = None
    tax: decimal.Decimal | None = None
    fee: decimal.Decimal | None = None
    grossRate: decimal.Decimal | None = None
    grossAmount: decimal.Decimal | None = None
    netAmount: decimal.Decimal | None = None
    code: tuple[enums.Code, ...] = ()
    sedol: str | None = None
    securityIDType: str | None = None
    underlyingSymbol: str | None = None
    issuer: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    fromAcct: str | None = None
    toAcct: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    serialNumber: str | None = None
    deliveryType: str | None = None
    commodityType: str | None = None
    fineness: decimal.Decimal | None = None
    weight: str | None = None


@dataclass(frozen=True)
class SecurityInfo(FlexElement):
    """Wrapped in <SecuritiesInfo>"""

    assetCategory: enums.AssetClass | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    cusip: str | None = None
    isin: str | None = None
    listingExchange: str | None = None
    underlyingSecurityID: str | None = None
    underlyingListingExchange: str | None = None
    underlyingConid: str | None = None
    underlyingCategory: str | None = None
    subCategory: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    maturity: str | None = None
    issueDate: datetime.date | None = None
    type: str | None = None
    sedol: str | None = None
    securityIDType: str | None = None
    underlyingSymbol: str | None = None
    issuer: str | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    code: tuple[enums.Code, ...] = ()
    currency: str | None = None
    settlementPolicyMethod: str | None = None
    figi: str | None = None
    issuerCountryCode: str | None = None
    relatedTradeID: str | None = None
    origTransactionID: str | None = None
    relatedTransactionID: str | None = None
    rtn: str | None = None
    initialInvestment: bool | None = None
    serialNumber: str | None = None
    deliveryType: str | None = None
    commodityType: str | None = None
    fineness: decimal.Decimal | None = None
    weight: str | None = None


@dataclass(frozen=True)
class ConversionRate(FlexElement):
    """Wrapped in <ConversionRates>"""

    reportDate: datetime.date | None = None
    fromCurrency: str | None = None
    toCurrency: str | None = None
    rate: decimal.Decimal | None = None


@dataclass(frozen=True)
class FIFOPerformanceSummaryUnderlying(FlexElement):
    accountId: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    listingExchange: str | None = None
    assetCategory: enums.AssetClass | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    cusip: str | None = None
    isin: str | None = None
    underlyingConid: str | None = None
    underlyingSecurityID: str | None = None
    underlyingListingExchange: str | None = None
    realizedSTProfit: decimal.Decimal | None = None
    realizedSTLoss: decimal.Decimal | None = None
    realizedLTProfit: decimal.Decimal | None = None
    realizedLTLoss: decimal.Decimal | None = None
    totalRealizedPnl: decimal.Decimal | None = None
    unrealizedProfit: decimal.Decimal | None = None
    unrealizedLoss: decimal.Decimal | None = None
    totalUnrealizedPnl: decimal.Decimal | None = None
    totalFifoPnl: decimal.Decimal | None = None
    totalRealizedCapitalGainsPnl: decimal.Decimal | None = None
    totalRealizedFxPnl: decimal.Decimal | None = None
    totalUnrealizedCapitalGainsPnl: decimal.Decimal | None = None
    totalUnrealizedFxPnl: decimal.Decimal | None = None
    totalCapitalGainsPnl: decimal.Decimal | None = None
    totalFxPnl: decimal.Decimal | None = None
    transferredPnl: decimal.Decimal | None = None
    transferredCapitalGainsPnl: decimal.Decimal | None = None
    transferredFxPnl: decimal.Decimal | None = None
    sedol: str | None = None
    securityIDType: str | None = None
    underlyingSymbol: str | None = None
    issuer: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    reportDate: datetime.date | None = None
    unrealizedSTProfit: decimal.Decimal | None = None
    unrealizedSTLoss: decimal.Decimal | None = None
    unrealizedLTProfit: decimal.Decimal | None = None
    unrealizedLTLoss: decimal.Decimal | None = None
    costAdj: decimal.Decimal | None = None
    code: tuple[enums.Code, ...] = ()
    serialNumber: str | None = None
    deliveryType: str | None = None
    commodityType: str | None = None
    fineness: decimal.Decimal | None = None
    weight: str | None = None
    subCategory: str | None = None
    figi: str | None = None
    issuerCountryCode: str | None = None

@dataclass(frozen=True)
class NetStockPosition(FlexElement):
    assetCategory: enums.AssetClass | None = None
    accountId: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    currency: str | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    securityIDType: str | None = None
    cusip: str | None = None
    isin: str | None = None
    sedol: str | None = None
    listingExchange: str | None = None
    underlyingConid: str | None = None
    underlyingSymbol: str | None = None
    underlyingSecurityID: str | None = None
    underlyingListingExchange: str | None = None
    issuer: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    reportDate: datetime.date | None = None
    sharesAtIb: decimal.Decimal | None = None
    sharesBorrowed: decimal.Decimal | None = None
    sharesLent: decimal.Decimal | None = None
    netShares: decimal.Decimal | None = None
    serialNumber: str | None = None
    deliveryType: str | None = None
    commodityType: str | None = None
    fineness: decimal.Decimal | None = None
    weight: str | None = None
    subCategory: str | None = None
    figi: str | None = None
    issuerCountryCode: str | None = None

@dataclass(frozen=True)
class ClientFee(FlexElement):
    accountId: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    feeType: str | None = None
    date: datetime.datetime | None = None
    description: str | None = None
    expenseIndicator: str | None = None
    revenue: decimal.Decimal | None = None
    expense: decimal.Decimal | None = None
    net: decimal.Decimal | None = None
    revenueInBase: decimal.Decimal | None = None
    expenseInBase: decimal.Decimal | None = None
    netInBase: decimal.Decimal | None = None
    tradeID: str | None = None
    execID: str | None = None
    levelOfDetail: str | None = None
    assetCategory: str | None = None
    settleDate: str | None = None
    buySell: str | None = None
    quantity: str | None = None
    tradePrice: str | None = None
    proceeds: str | None = None
    symbol: str | None = None
    underlyingSymbol: str | None = None
    multiplier: str | None = None
    underlyingSecurityID: str | None = None


@dataclass(frozen=True)
class ClientFeesDetail(FlexElement):
    accountId: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    date: datetime.datetime | None = None
    tradeID: str | None = None
    execID: str | None = None
    totalRevenue: decimal.Decimal | None = None
    totalCommission: decimal.Decimal | None = None
    brokerExecutionCharge: decimal.Decimal | None = None
    clearingCharge: decimal.Decimal | None = None
    thirdPartyExecutionCharge: decimal.Decimal | None = None
    thirdPartyRegulatoryCharge: decimal.Decimal | None = None
    regFINRATradingActivityFee: decimal.Decimal | None = None
    regSection31TransactionFee: decimal.Decimal | None = None
    regOther: decimal.Decimal | None = None
    totalNet: decimal.Decimal | None = None
    totalNetInBase: decimal.Decimal | None = None
    levelOfDetail: str | None = None
    other: decimal.Decimal | None = None


@dataclass(frozen=True)
class TransactionTax(FlexElement):
    accountId: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    assetCategory: enums.AssetClass | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    securityIDType: str | None = None
    cusip: str | None = None
    isin: str | None = None
    listingExchange: str | None = None
    underlyingConid: str | None = None
    underlyingSecurityID: str | None = None
    underlyingSymbol: str | None = None
    underlyingListingExchange: str | None = None
    issuer: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    date: datetime.datetime | None = None
    taxDescription: str | None = None
    quantity: decimal.Decimal | None = None
    reportDate: datetime.date | None = None
    taxAmount: decimal.Decimal | None = None
    tradeId: str | None = None
    tradePrice: decimal.Decimal | None = None
    source: str | None = None
    code: tuple[enums.Code, ...] = ()
    levelOfDetail: str | None = None


@dataclass(frozen=True)
class TransactionTaxDetail(FlexElement):
    accountId: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    assetCategory: enums.AssetClass | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    securityIDType: str | None = None
    cusip: str | None = None
    isin: str | None = None
    listingExchange: str | None = None
    underlyingConid: str | None = None
    underlyingSecurityID: str | None = None
    underlyingSymbol: str | None = None
    underlyingListingExchange: str | None = None
    issuer: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    date: datetime.datetime | None = None
    taxDescription: str | None = None
    quantity: decimal.Decimal | None = None
    reportDate: datetime.date | None = None
    taxAmount: decimal.Decimal | None = None
    tradeId: str | None = None
    tradePrice: decimal.Decimal | None = None
    source: str | None = None
    code: tuple[enums.Code, ...] = ()
    levelOfDetail: str | None = None


@dataclass(frozen=True)
class SalesTax(FlexElement):
    accountId: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    assetCategory: enums.AssetClass | None = None
    subCategory: str | None = None
    symbol: str | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    securityIDType: str | None = None
    cusip: str | None = None
    isin: str | None = None
    listingExchange: str | None = None
    underlyingConid: str | None = None
    underlyingSecurityID: str | None = None
    underlyingSymbol: str | None = None
    underlyingListingExchange: str | None = None
    issuer: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    date: datetime.date | None = None
    country: str | None = None
    taxType: str | None = None
    payer: str | None = None
    taxableDescription: str | None = None
    taxableAmount: decimal.Decimal | None = None
    taxRate: decimal.Decimal | None = None
    salesTax: decimal.Decimal | None = None
    taxableTransactionID: str | None = None
    transactionID: str | None = None
    serialNumber: str | None = None
    deliveryType: str | None = None
    commodityType: str | None = None
    fineness: decimal.Decimal | None = None
    weight: str | None = None
    code: tuple[enums.Code, ...] = ()


@dataclass(frozen=True)
class SLBOpenContract(FlexElement):
    accountId: str | None = None
    acctAlias: str | None = None
    model: str | None = None
    currency: str | None = None
    fxRateToBase: decimal.Decimal | None = None
    description: str | None = None
    conid: str | None = None
    securityID: str | None = None
    cusip: str | None = None
    isin: str | None = None
    assetCategory: str | None = None
    subCategory: str | None = None
    symbol: str | None = None
    securityIDType: str | None = None
    figi: str | None = None
    listingExchange: str | None = None
    underlyingConid: str | None = None
    underlyingSymbol: str | None = None
    underlyingSecurityID: str | None = None
    underlyingListingExchange: str | None = None
    issuer: str | None = None
    issuerCountryCode: str | None = None
    multiplier: decimal.Decimal | None = None
    strike: decimal.Decimal | None = None
    expiry: datetime.date | None = None
    putCall: enums.PutCall | None = None
    principalAdjustFactor: decimal.Decimal | None = None
    date: datetime.date | None = None
    type: str | None = None
    slbTransactionId: str | None = None
    exchange: str | None = None
    quantity: decimal.Decimal | None = None
    excessQuantity: decimal.Decimal | None = None
    feeRate: decimal.Decimal | None = None
    collateralAmount: decimal.Decimal | None = None
    levelOfDetail: str | None = None
    serialNumber: decimal.Decimal | None = None
    deliveryType: decimal.Decimal | None = None
    commodityType: str | None = None
    fineness: decimal.Decimal | None = None
    weight: decimal.Decimal | None = None

#  Type alias to work around https://github.com/python/mypy/issues/1775
_ClientFeesDetail = ClientFeesDetail
