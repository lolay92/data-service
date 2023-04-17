import logging
from typing import Callable, Optional, Dict
from dataclasses import dataclass, field
from configparser import ConfigParser

from data_services.loaders.eodhd import EodQueryOhclv
from data_services.loaders.api import Service
from data_services.utils.universe import UniverseQuery
from data_services.utils.log_utils import logging_dict
from data_services.utils.fetch_load_utils import file_dumper

from data_services.loaders.eodhd import Eodhd


# Initialize logger
logging.config.dictConfig(logging_dict)
_logger = logging.getLogger(__name__)

# Initialize universe of tickers
universe = UniverseQuery()


class EtfData:
    def __init__(self) -> None:
        ApiService = Service()
        self.api = ApiService.api

    @file_dumper("Output/ETF/ohclv/commo_etfs")
    def load_ohlcv(self, eodquery):
        return self.api.ohlcv(eodquery=eodquery)


class MiscellaneousData:
    def __init__(self) -> None:
        ApiService = Service()
        self.api = ApiService.api
        self.api2 = ApiService.api2

    def search_security(self, search_query: str):
        return self.api.search(search_query=search_query)
        # return self.eod

    def get_supported_exchanges(self):
        return self.api.get_api_supported_exchanges()

    def get_traded_tickers(self, exchange_code: str):
        return self.api.get_exchange_traded_tickers(exchange_code=exchange_code)

    def get_delisted_tickers(self, exchange_code: str):
        return self.api.get_exchange_traded_tickers(
            exchange_code=exchange_code, delisted=True
        )


if __name__ == "__main__":
    eodquery = EodQueryOhclv(tickers=["AAPL", "MCD"])
    print(eodquery.tickers)
    EtfData = EtfData()
    EtfData.load_ohlcv(eodquery=eodquery)


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


# misc = datahandler.MiscData()
# etf = datahandler.EtfData()


# main.EtfBasket().get_crypto_ohclv()


#   for macro data --> eod:
#       create a universe map/config tha looks like:
#       empoloyment = "list of indicators"
#       Growth sector = "list of component"
#       main precious metals = "list of tickers"
#       inflation = "list of inflation indicaors"

# if __name__ == "__main__":
#     miscdata = MiscellaneousData()
#     miscdata.api
#     data = miscdata.get_supported_exchanges()
#     print(data)
# response = miscdata.search_security(search_query="Goldman")
# print(response.json())
