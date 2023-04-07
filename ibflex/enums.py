# coding: utf-8
"""Enumerated values (Python enum.Enum subclasses) used to define ibflex.Types.

Values are the text sent by IB in XML element attribute.
Names keep the convention of using UPPERCASE for Enums.

When creating a new Enum subclass, be sure to add it to ENUMS
and EnumType (as Optional type) at the end of the file.
"""

__all__ = [
    "CashAction",
    "Code",
    "AssetClass",
    "TradeType",
    "BuySell",
    "OpenClose",
    "OrderType",
    "Reorg",
    "OptionAction",
    "LongShort",
    "TransferType",
    "ToFrom",
    "InOut",
    "DeliveredReceived",
    "ENUMS",
    "EnumType",
]

import enum
import typing


@enum.unique
class CashAction(str, enum.Enum):
    DEPOSITWITHDRAW = "Deposits & Withdrawals"
    BROKERINTPAID = "Broker Interest Paid"
    BROKERINTRCVD = "Broker Interest Received"
    WHTAX = "Withholding Tax"
    BONDINTRCVD = "Bond Interest Received"
    BONDINTPAID = "Bond Interest Paid"
    FEES = "Other Fees"
    DIVIDEND = "Dividends"
    PAYMENTINLIEU = "Payment In Lieu Of Dividends"
    COMMADJ = "Commission Adjustments"


@enum.unique
class Code(str, enum.Enum):
    """Used for both `code` and `notes` attributes.
    """
    ASSIGNMENT = "A"
    AUTOEXERCISE = "AEx"  # Automatic exercise for dividend-related recommendation
    ADJUSTMENT = "Adj"  # Adjustment
    ALLOCATION = "Al"  # Allocation
    AWAY = "Aw"  # Away Trade
    BUYIN = "B"  # Automatic Buy-in
    BORROW = "Bo"  # Direct Borrow
    CLOSING = "C"  # Closing Trade
    CASHDELIVERY = "CD"  # Cash Delivery
    COMPLEX = "CP"  # Complex Position
    CANCEL = "Ca"  # Cancelled
    CORRECT = "Co"  # Corrected Trade
    CROSSING = "Cx"  # Part or all of this transaction was a Crossing executed as dual agent by IB for two IB customers
    DUAL = "D"  # IB acted as Dual Agent, UNIQUE TO TRADE CONFIRM REPORT
    ETF = "ETF"  # ETF Creation/Redemption
    EXPIRED = "Ep"  # Resulted from an Expired Position
    EXERCISE = "Ex"  # Exercise
    GUARANTEED = "G"  # Trade in Guaranteed Account Segment
    HIGHESTCOST = "HC"  # Highest Cost tax lot-matching method
    HFINVESTMENT = "HFI"  # Investment Transferred to Hedge Fund
    HFREDEMPTION = "HFR"  # Redemption from Hedge Fund
    INTERNAL = "I"  # Internal Transfer
    AFFILIATE = "IA"  # This transaction was executed against an IB affiliate
    INVESTOR = "INV"  # Investment Transfer from Investor
    MARGINLOW = "L"  # Ordered by IB (Margin Violation)
    WASHSALE = "LD"  # Adjusted by Loss Disallowed from Wash Sale
    LIFO = "LI"  # Last In, First Out (LIFO) tax lot-matching method
    LTCG = "LT"  # Long-term P/L
    LOAN = "Lo"  # Direct Loan
    MANUAL = "M"  # Entered manually by IB
    MANUALEXERCISE = "MEx"  # Manual exercise for dividend-related recommendation
    MAXLOSS = "ML"  # Maximize Losses tax basis election
    MAXLTCG = "MLG"  # Maximize Long-Term Gain tax lot-matching method
    MINLTCG = "MLL"  # Maximize Long-Term Loss tax lot-matching method
    MAXSTCG = "MSG"  # Maximize Short-Term Gain tax lot-matching method
    MINSTCG = "MSL"  # Maximize Short-Term Loss tax lot-matching method
    OPENING = "O"  # Opening Trade
    PARTIAL = "P"  # Partial Execution
    FRACRISKLESSPRINCIPAL = "RP"  # IB acted as riskless principal for the fractional share portion of this trade
    FRACPRINCIPAL = "FP"  # IB acted as principal for the fractional share portion of this trade
    PRICEIMPROVEMENT = "PI"  # Price Improvement
    POSTACCRUAL = "Po"  # Interest or Dividend Accrual Posting
    PRINCIPAL = "Pr"  # Part or all of this transaction was executed by the Exchange as a Crossing by IB against an IB affiliate and is therefore classified as a Principal and not an agency trade
    REINVESTMENT = "R"  # Dividend Reinvestment
    REDEMPTION = "RED"  # Redemption to Investor
    REVERSE = "Re"  # Interest or Dividend Accrual Reversal
    REIMBURSEMENT = "Ri"  # Reimbursement
    SOLICITEDIB = "SI"  # This order was solicited by Interactive Brokers
    SPECIFICLOT = "SL"  # Specific Lot tax lot-matching method
    SOLICITEDOTHER = "SO"  # This order was marked as solicited by your Introducing Broker
    SHORTENEDSETTLEMENT = "SS"  # Customer designated this trade for shortened settlement and so is subject to execution at prices above the prevailing market
    STCG = "ST"  # Short-term P/L
    STOCKYIELD = "SY"  # Positions that may be eligible for Stock Yield.
    TRANSFER = "T"  # Transfer


@enum.unique
class AssetClass(str, enum.Enum):
    CASH = "CASH"
    BILL = "BILL"
    BOND = "BOND"
    STOCK = "STK"
    OPTION = "OPT"
    WARRANT = "WAR"
    FUTURE = "FUT"
    FUTUREOPTION = "FOP"
    CFD = "CFD"
    FOREXCFD = "FXCFD"
    CRYPTOCURRENCY = "CRYPTO"
    STRUCTUREDPRODUCTS = "IOPT"
    METALS = "CMDTY"
    OPTIONSONFUTURES = "FSFOP"
    OPTIONSFUTURESSTYLE = "FSOPT"
    MUTUALFUND = "FUND"


@enum.unique
class TradeType(str, enum.Enum):
    EXCHTRADE = "ExchTrade"
    TRADECANCEL = "TradeCancel"
    FRACSHARE = "FracShare"
    FRACSHARECANCEL = "FracShareCancel"
    TRADECORRECT = "TradeCorrect"
    BOOKTRADE = "BookTrade"
    DVPTRADE = "DvpTrade"


@enum.unique
class BuySell(str, enum.Enum):
    BUY = "BUY"
    CANCELBUY = "BUY (Ca.)"
    SELL = "SELL"
    CANCELSELL = "SELL (Ca.)"


@enum.unique
class OpenClose(str, enum.Enum):
    OPEN = "O"
    CLOSE = "C"
    OPENCLOSE = "C;O"
    UNKNOWN = "-"


@enum.unique
class OrderType(str, enum.Enum):
    LIMIT = "LMT"
    MARKET = "MKT"
    STOP = "STP"
    STOPLIMIT = "STPLMT"
    MARKETONCLOSE = "MOC"
    LIMITONCLOSE = "LOC"
    # MULTIPLE is not an actual IB order type. It is a catch-all value to use when an Order has an orderType like "LMT;MKT".
    # This way OrderType can remian a enum and not be a Tuple.
    MULTIPLE = "MULTIPLE"


@enum.unique
class Reorg(str, enum.Enum):
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
class OptionAction(str, enum.Enum):
    ASSIGN = "Assignment"
    EXERCISE = "Exercise"
    EXPIRE = "Expiration"
    SELL = "Sell"
    BUY = "Buy"
    CASHSETTLEMENT = "Cash Settlement"


@enum.unique
class LongShort(str, enum.Enum):
    LONG = "Long"
    SHORT = "Short"


@enum.unique
class ToFrom(str, enum.Enum):
    TO = "To"
    FROM = "From"


@enum.unique
class TransferType(str, enum.Enum):
    INTERNAL = "INTERNAL"
    ACATS = "ACATS"
    ATON = "ATON"


@enum.unique
class InOut(str, enum.Enum):
    IN = "IN"
    OUT = "OUT"


@enum.unique
class DeliveredReceived(str, enum.Enum):
    DELIVERED = "Delivered"
    RECEIVED = "Received"


@enum.unique
class PutCall(str, enum.Enum):
    PUT = "P"
    CALL = "C"


ENUMS = [
    CashAction,
    Code,
    AssetClass,
    TradeType,
    BuySell,
    OpenClose,
    OrderType,
    Reorg,
    OptionAction,
    LongShort,
    ToFrom,
    TransferType,
    InOut,
    DeliveredReceived,
    PutCall,
]
"""Used by ibflex.parser.ATTRIB_CONVERTERS"""

EnumType = typing.Union[
    typing.Optional[CashAction],
    typing.Optional[Code],
    typing.Optional[AssetClass],
    typing.Optional[TradeType],
    typing.Optional[BuySell],
    typing.Optional[OpenClose],
    typing.Optional[OrderType],
    typing.Optional[Reorg],
    typing.Optional[OptionAction],
    typing.Optional[LongShort],
    typing.Optional[ToFrom],
    typing.Optional[TransferType],
    typing.Optional[InOut],
    typing.Optional[DeliveredReceived],
    typing.Optional[PutCall],
]
"""Used by ibflex.parser.DataType"""
