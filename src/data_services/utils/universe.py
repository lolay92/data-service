from pprint import pprint
from typing import List
from dataclasses import dataclass, field
from configparser import ConfigParser

UNIVERSE_FILEPATH = "src/data_services/utils/constants/universe.ini"


@dataclass
class UniverseQuery:
    global_universe: ConfigParser = field(init=False, default_factory=ConfigParser)
    # ----ETF----
    us_eq_sector: List[str] = field(init=False)
    us_eq_index: List[str] = field(init=False)
    eq_dev_country: List[str] = field(init=False)
    eq_em_country: List[str] = field(init=False)
    us_fi_etf: List[str] = field(init=False)
    commo_etf: List[str] = field(init=False)
    # ----FUTURES----
    us_eq_idx_fut: List[str] = field(init=False)
    fi_fut: List[str] = field(init=False)
    pm_fut: List[str] = field(init=False)
    energy_fut: List[str] = field(init=False)
    # ----FX PAIRS----
    fx_major_pairs: List[str] = field(init=False)

    def __post_init__(self) -> None:
        self.global_universe.read(UNIVERSE_FILEPATH)
        # ----ETF----
        self.us_eq_sector = self.global_universe["ETF"]["US_EQ_SECTOR"].split(".")
        self.us_eq_index = self.global_universe["ETF"]["US_EQ_INDEX"].split(".")
        self.eq_dev_country = self.global_universe["ETF"]["EQ_DEV_COUNTRY"].split(".")
        self.eq_em_country = self.global_universe["ETF"]["EQ_EM_COUNTRY"].split(".")
        self.us_fi_etf = self.global_universe["ETF"]["US_FI_ETF"].split(".")
        self.commo_etf = self.global_universe["ETF"]["COMMO_ETF"].split(".")
        # ----FUTURES----
        self.us_eq_idx_fut = self.global_universe["FUT"]["US_EQ_IDX_FUT"].split(".")
        self.fi_fut = self.global_universe["FUT"]["FI_FUT"].split(".")
        self.pm_fut = self.global_universe["FUT"]["PM_FUT"].split(".")
        self.energy_fut = self.global_universe["FUT"]["ENERGY_FUT"].split(".")
        # ----FX PAIRS----
        self.fx_major_pairs = self.global_universe["FX"]["FX_MAJOR_PAIRS"].split(".")
        # ----CRYPTO----
        # To implement

    def print_global_universe(self):
        pprint(self.global_universe._sections)

    def build_Universe(self):
        pass
