from typing import List, Dict
from dataclasses import dataclass
from configparser import ConfigParser
from enum import Enum

UNIVERSE_FILEPATH = "src/data_services/utils/constants/universe.ini"


class UniverseMap(Enum):
    US_EQ_SECTOR = ("us_eq_sector", "ETF")
    US_EQ_INDEX = ("us_eq_index", "ETF")
    EQ_DEV_COUNTRY = ("eq_dev_country", "ETF")
    EQ_EM_COUNTRY = ("eq_em_country", "ETF")
    US_FI_ETF = ("us_fi_etf", "ETF")
    COMMO_ETF = ("commo_etf", "ETF")
    US_EQ_IDX_FUT = ("us_eq_idx_fut", "FUT")
    FI_FUT = ("fi_fut", "FUT")
    PM_FUT = ("pm_fut", "FUT")
    ENERGY_FUT = ("energy_fut", "FUT")
    FX_MAJOR_PAIRS = ("fx_major_pairs", "FX")

    def __new__(cls, value, category):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.category = category
        return obj


@dataclass
class QueryUniverse:
    """Allows querying universe properties and components.
    E.g.:
    universe = QueryUniverse(UniverseMap.ENERGY_FUT)
    universe.global_universe
    print(universe.universe_properties.name)
    print(universe.universe_properties.value)
    print(universe.universe_properties.category)
    print(universe.components)

    universe has properties, global universe and constituents as attributes
    universe.properties has value, name and category as attributes

    So we should be able to do something like this:

    universe.properties.name ==> 'ENERGY_FUT'
    universe.properties.value ==> 'energy_fut'
    universe.properties.category ==> 'FUT'
    print(universe.print_global_universe())"""

    properties: UniverseMap

    def __post_init__(self):
        _global_universe: ConfigParser = ConfigParser()
        _global_universe.read(UNIVERSE_FILEPATH)
        self.global_universe: Dict[str, Dict[str, str]] = _global_universe._sections
        self.components: List[str] = _global_universe[self.properties.category][
            self.properties.name
        ].split(".")
