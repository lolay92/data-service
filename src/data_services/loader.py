import logging

from src.data_services.loaders.api import ApiServiceInitializer
from src.data_services.loaders.tiingo import Tiingo
from src.data_services.utils.log_utils import logging_dict

from typing import Optional, Dict
from dataclasses import dataclass
from configparser import ConfigParser

# Initialize logger
logging.config.dictConfig(logging_dict)
_logger = logging.getLogger(__name__)


class MiscellaneousData:
    def __init__(self) -> None:
        ApiService = ApiServiceInitializer()
        self.eod = ApiService.eod

        # self.eod.

    def search_security(self, search_query: str):
        return self.eod.search(query_str=search_query)
        # return self.eod

    def get_supported_exchanges(self):
        return self.eod.get_api_supported_exchanges()

    def get_traded_tickers(self, exchange_code: str):
        return self.eod.get_exchange_traded_tickers(exchange_code=exchange_code)

    def get_delisted_tickers(self, exchange_code: str):
        return self.eod.get_exchange_traded_tickers(
            exchange_code=exchange_code, delisted=True
        )


# class ExchangeTradedFunds():
#     # integrate etfs_basket_universe
#     # def fetch_universe by calling fetch universe from eod
#     def __post__init():
#         pass

#     def get_eod_ohclv_ficc():
#         pass

#     def get_eod_ohclv_us_equities():
#         pass

#     def get_eod_ohclv_country_etfs():
#         pass


# class Crypto():
#     pass


# class Macro():
#     pass


# --> format expected


# datahandler = datahandler.MiscData()


# main.EtfBasket().get_crypto_ohclv()


#   for macro data --> eod:
#       create a universe map/config tha looks like:
#       empoloyment = "list of indicators"
#       Growth sector = "list of component"
#       main precious metals = "list of tickers"
#       inflation = "list of inflation indicaors"

# if __name__ == "__main__":
#     miscdata = MiscellaneousData()
#     response = miscdata.search_security(search_query=data)
#     print(response.json())
