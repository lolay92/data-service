from typing import List
from dataclasses import dataclass, field
from configparser import ConfigParser

UNIVERSE_FILEPATH = "src/data_services/utils/constants/universe.ini"


@dataclass
class Universe:
    global_universe: ConfigParser = field(init=True, default_factory=ConfigParser)
    us_eq_sector: str = field(init=False)
    us_eq_index: str = field(init=False)
    eq_dev_country: str = field(init=False)
    eq_em_country: str = field(init=False)
    us_fi_etfs: str = field(init=False)
    commo_etfs: str = field(init=False)

    def __post_init__(self):
        self.global_universe.read(UNIVERSE_FILEPATH)
        # ------------------------ETFS-----------------------------------------------
        self.us_eq_sector = self.global_universe["ETFS"]["US_EQ_SECTORS"].split(".")
        self.us_eq_index = self.global_universe["ETFS"]["US_EQ_INDEX"].split(".")
        self.eq_dev_country = self.global_universe["ETFS"]["EQ_DEV_COUNTRY"].split(".")
        self.eq_em_country = self.global_universe["ETFS"]["EQ_EM_COUNTRY"].split(".")
        self.us_fi_etfs = self.global_universe["ETFS"]["US_FI_ETFS"].split(".")
        self.commo_etfs = self.global_universe["ETFS"]["COMMO_ETFS"].split(".")

    def print_global_universe(self):
        for section in self.global_universe.sections():
            print(f"\n[{section}]")
            for key, value in self.global_universe.items(section):
                print(f"{key} = {value}")

    # def add_ticker_to_universe(self, universe: List):
    #  pass


# METHODS
# print global universe
# add element to universe
# delete element in universe

# Build: I could return one of defined universe or
#   concat multiples universe
#

# Then I would be able to create with factory pattern something like this:
#


# def universe_components(self, universe) -> List:
#     pass

# def build(self) -> List:
#     pass


# @dataclass
# class UniverseFactory(Universe):
#     # create universe depending on the universe name
#     pass


if __name__ == "__main__":
    universe = Universe()
    print(universe.print_global_universe())
    # pm_futs = universe.global_universe["FUTURES"]["PM_FUTURES"].split(".")
    # print(pm_futs.split("."))
    # print(universe.us_fi_etfs)
    # print(universe.commo_etfs)
    # print(universe.us_eq_index)

    # print(universe.us_eq_sectors)
