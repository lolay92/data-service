from pprint import pprint
from typing import List
from dataclasses import dataclass, field
from configparser import ConfigParser

UNIVERSE_FILEPATH = "src/data_services/utils/constants/universe.ini"


@dataclass
class UniverseQuery:
    global_universe: ConfigParser = field(init=False, default_factory=ConfigParser)
    # ----ETFS----
    us_eq_sector: List[str] = field(init=False)
    us_eq_index: List[str] = field(init=False)
    eq_dev_country: List[str] = field(init=False)
    eq_em_country: List[str] = field(init=False)
    us_fi_etfs: List[str] = field(init=False)
    commo_etfs: List[str] = field(init=False)
    # ----FUTURES----
    us_eq_idx_futs: List[str] = field(init=False)
    fx_futs: List[str] = field(init=False)
    fi_futs: List[str] = field(init=False)
    pm_futs: List[str] = field(init=False)
    energy_futs: List[str] = field(init=False)
    # ----FX PAIRS----
    fx_major_pairs: List[str] = field(init=False)

    def __post_init__(self) -> None:
        self.global_universe.read(UNIVERSE_FILEPATH)
        # ----ETFS----
        self.us_eq_sector = self.global_universe["ETFS"]["US_EQ_SECTORS"].split(".")
        self.us_eq_index = self.global_universe["ETFS"]["US_EQ_INDEX"].split(".")
        self.eq_dev_country = self.global_universe["ETFS"]["EQ_DEV_COUNTRY"].split(".")
        self.eq_em_country = self.global_universe["ETFS"]["EQ_EM_COUNTRY"].split(".")
        self.us_fi_etfs = self.global_universe["ETFS"]["US_FI_ETFS"].split(".")
        self.commo_etfs = self.global_universe["ETFS"]["COMMO_ETFS"].split(".")
        # ----FUTURES----
        self.us_eq_idx_futs = self.global_universe["FUTS"]["US_EQ_IDX_FUTS"].split(".")
        self.fx_futs = self.global_universe["FUTS"]["FX_FUTS"].split(".")
        self.fi_futs = self.global_universe["FUTS"]["FI_FUTS"].split(".")
        self.pm_futs = self.global_universe["FUTS"]["PM_FUTS"].split(".")
        self.energy_futs = self.global_universe["FUTS"]["ENERGY_FUTS"].split(".")
        # ----FX PAIRS----
        self.fx_major_pairs = self.global_universe["FX"]["FX_MAJOR_PAIRS"].split(".")
        # ----CRYPTO----
        # To implement

    def print_global_universe(self):
        pprint(self.global_universe._sections)
