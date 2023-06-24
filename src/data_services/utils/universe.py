from enum import Enum

"""
Fixed-Income US ETFs
BIL: Short-term US Treasury bills ETF
SHY: 1-3 year US Treasury bonds ETF
IEI: 3-7 year US Treasury bonds ETF
IEF: 7-10 year US Treasury bonds ETF
TLT: 20+ YR US Treasury bonds ETF
MBB: iShares MBS ETF
LQD: iShares iBoxx Investment Grade Corporate Bond ETF
HYG: iShares iBoxx High Yield Corporate Bond ETF
JNK: SPDR Bloomberg Barclays High Yield Bond ETF
PCY: Invesco Emerging Markets Sovereign Debt ETF
BOND: PIMCO Total Return Bond ETF

EQ EMERGING MARKETS ETFS
FXI: iShares China Large-Cap ETF
KWEB: KraneShares CSI China Internet ETF
EWZ: iShares MSCI Brazil ETF
EWW: iShares MSCI Mexico ETF
EWS: iShares MSCI Singapore ETF
EWY: iShares MSCI South Korea ETF
EWT: iShares MSCI Taiwan ETF
INDA: iShares MSCI India ETF
EWH: iShares MSCI Hong Kong ETF
EZA: iShares MSCI South Africa ETF

EQ DEVELOPED COUNTRIES ETFS
EWA: iShares MSCI Australia ETF
EWC: iShares MSCI Canada ETF
EWQ: iShares MSCI France ETF
EWG: iShares MSCI Germany ETF
EWI: iShares MSCI Italy ETF
EWJ: iShares MSCI Japan ETF
EWP: iShares MSCI Spain ETF
EWU: iShares MSCI United Kingdom ETF
EUFN: iShares MSCI Europe Financials ETF
EWL: iShares MSCI Switzerland ETF

EQ US SECTORS ETFS
XLY: Consumer Discretionary ETF
XLP: Consumer Staples ETF
XLE: Energy ETF
XLF: Financials ETF
XLV: Healthcare ETF
XLI: Industrial ETF
XLB: Materials ETF
XLK: Technology ETF
XBI: Biotech ETF
SMH: Semiconductor ETF
XLC: Communication Services ETF
XLU: Utilities ETF
XME: Metals & Mining ETF
GDX: Gold Miners ETF
XOP: Oil & Gas Exploration & Production ETF
XHB: Homebuilders ETF
XLRE: Real Estate ETF
XRT: Retail ETF

EQ INDICES ETFS
SPY: S&P 500 ETF
QQQ: Nasdaq-100 ETF
DIA: Dow Jones Industrial Average ETF
IWM: Russell 2000 ETF

Fixed-Income Futures (100K$ face value traded on CBOT)
ZT1: 2-3 year Treasury note futures
ZF1: 4.5-5.5 year Treasury bond futures
ZN1: 9-10 year Treasury note futures
ZB1: 15-25 year Treasury bond futures

Precious Metals futures
GC1: Gold futures contract traded on the Tokyo Commodity Exchange (Tocom).
SI1: Silver futures contract traded on the Tocom.
PL1: Platinum futures contract traded on the Tocom.
PA1: Palladium futures contract traded on the Tocom.

Energy futures
CL1: Crude oil futures contract traded on the New York Mercantile Exchange (NYMEX).
NG1: Natural gas futures contract traded on the NYMEX.
HO1: Heating oil futures contract traded on the NYMEX.
BZ1: Brent crude oil futures contract traded on the Intercontinental Exchange (ICE).
RB1: RBOB gasoline futures contract traded on the NYMEX.

US EQ IDX FUTURES
ES1: E-mini S&P 500 futures contract traded on the Chicago Mercantile Exchange (CME).
YM1: E-mini Dow Jones Industrial Average futures contract traded on the CME.
NQ1: E-mini Nasdaq 100 futures contract traded on the CME.
RTY1: E-mini Russell 2000 futures contract traded on the CME.

"""


class Universe(Enum):
    US_EQ_SECTOR = (
        "us_eq_sector",
        "ETF",
        "XLY.XLP.XLE.XLF.XLV.XLI.XLB.XLK.XBI.SMH.XLC.XLU.XME.GDX.XOP.XHB.XLRE.XRT",
    )
    US_EQ_INDEX = ("us_eq_index", "ETF", "SPY.QQQ.DIA.IWM")
    EQ_DEV_COUNTRY = (
        "eq_dev_country",
        "ETF",
        "EWA.EWC.EWQ.EWG.EWI.EWJ.EWP.EWU.EUFN.EWL",
    )
    EQ_EM_COUNTRY = (
        "eq_em_country",
        "ETF",
        "FXI.KWEB.EWZ.EWW.EWS.EWY.EWT.INDA.EWH.EZA",
    )
    US_FI_ETF = ("us_fi_etf", "ETF", "BIL.SHY.IEI.IEF.TLT.MBB.LQD.HYG.JNK.PCY.BOND")
    COMMO_ETF = ("commo_etf", "ETF", "GLD.SLV.USO.UNG.DBA.DBC")
    US_EQ_IDX_FUT = ("us_eq_idx_fut", "FUT", "ES1.YM1.NQ1.RTY1")
    FI_FUT = ("fi_fut", "FUT", "ZT1.ZF1.ZN1.ZB1")
    PM_FUT = ("pm_fut", "FUT", "GC1.SI1.PL1.PA1")
    ENERGY_FUT = ("energy_fut", "FUT", "CL1.NG1.HO1.BZ1.RB1")
    FX_MAJOR_PAIRS = (
        "fx_major_pairs",
        "FX",
        "EURUSD.USDJPY.GBPUSD.AUDUSD.USDCAD.USDCHF.NZDUSD.USDMXN",
    )

    def __new__(cls, value, category, components):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.category = category
        obj.components = components.split(".")
        return obj
