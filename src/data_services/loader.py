import logging
from typing import Callable, Optional, Dict
from dataclasses import dataclass, field
from configparser import ConfigParser

from data_services.loaders.base import BaseLoader
from data_services.loaders.eodhd import Eodhd, EodQueryOhlcv
from data_services.loaders.tiingo import Tiingo, TiingoQueryIntraday

from data_services.utils.log_utils import logging_dict
from data_services.utils.fetch_load_utils import file_dumper


# Initialize logger
logging.config.dictConfig(logging_dict)
_logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Service:
    """Service base class to initialize the relevant api for data services"""

    eod: Eodhd = Eodhd()
    tiingo: Tiingo = Tiingo()


class ExoticData(Service):
    """Requests and load miscellaneous data that can't be associated in the other
    type of asset classes (e.g.: vol products, inflation products...etc)"""

    def __init__(self) -> None:
        super().__init__()

    def util_search(self, query: str):
        return self.eod.search(search_query=query)

    def get_supported_exchanges(self, api: "str"):
        if api == "eod":
            return self.eod.api_supported_exchanges()

    def get_supported_exchanges(
        self, api: "str", exchange_code: str, delisted: bool = False
    ):
        if api == "eod":
            return self.eod.api_supported_exchanges(
                exchange_code=exchange_code, delisted=delisted
            )


class Etf(Service):
    """Requests and load ETF data (fundamentals, index top components)"""

    def __init__(self) -> None:
        super().__init__()

    @file_dumper("Output/ETF/ohclv/commo_etfs")
    def load_ohlcv(self, eodquery: EodQueryOhlcv):
        """ohlcv ETF data"""
        return self.eod.ohlcv(eodquery=eodquery)

    def get_components(self):
        pass


class Crypto(Service):
    pass


class Futures(Service):
    pass


class Macro(Service):
    pass


# -------------- Main
if __name__ == "__main__":
    from data_services.utils.universe import UniverseQuery

    universe = UniverseQuery()
    eodquery = EodQueryOhlcv(tickers=["AAPL", "MCD"])
    EtfData = Etf()
    EtfData.load_ohlcv(eodquery=eodquery)
