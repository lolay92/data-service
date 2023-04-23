import logging
import json
from datetime import datetime, date
from typing import Dict, List, Union
from dataclasses import dataclass
from pathlib import Path

from data_services.loaders.eodhd import Eodhd, EodQueryOhlcv
from data_services.loaders.tiingo import Tiingo, TiingoQueryIntraday
from data_services.utils.universe import UniverseQuery

from data_services.utils.log_utils import logging_dict
from data_services.utils.fetch_load_utils import file_dump

# Output locations
OUTPUT_BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_BASE_DIR = Path(OUTPUT_BASE_DIR, "output")
OUTPUT_MISC_DATA = Path(OUTPUT_BASE_DIR, "misc")
OUTPUT_ETF_OHLCV = Path(OUTPUT_BASE_DIR, "etf/ohlcv")
OUTPUT_CRYPTO_OHLCV = Path(OUTPUT_BASE_DIR, "crypto/ohlcv")
OUTPUT_CRYPTO_INTRADAY = Path(OUTPUT_BASE_DIR, "crypto/intraday")

OUTPUT_BASE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_MISC_DATA.mkdir(parents=True, exist_ok=True)
OUTPUT_ETF_OHLCV.mkdir(parents=True, exist_ok=True)
OUTPUT_CRYPTO_OHLCV.mkdir(parents=True, exist_ok=True)
OUTPUT_CRYPTO_INTRADAY.mkdir(parents=True, exist_ok=True)


# Initialize logger
logging.config.dictConfig(logging_dict)
_logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Service:
    """Service base class to initialize the relevant api for data services"""

    eod: Eodhd = Eodhd()
    tiingo: Tiingo = Tiingo()
    universe: UniverseQuery = UniverseQuery()


class miscData(Service):
    """Requests and load miscellaneous data"""

    def __init__(self) -> None:
        super().__init__()

    def util_search(self, query: str) -> List[Dict]:
        return self.eod.search(search_query=query)

    def get_supported_exchanges(self, api: str = "eod") -> List[Dict]:
        if api == "eod":
            json_response = self.eod.api_supported_exchanges()
        with open(f"{OUTPUT_MISC_DATA}/supported_exchanges.json", "w") as file:
            json.dump(json_response, file, indent=4)
        return json_response

    def get_exchange_traded_tickers(
        self, api: str = "eod", exchange_code: str = "US", delisted: bool = False
    ) -> List[Dict]:
        if api == "eod":
            json_response = self.eod.exchange_traded_tickers(
                exchange_code=exchange_code, delisted=delisted
            )
        with open(f"{OUTPUT_MISC_DATA}/{exchange_code}_tickers.json", "w") as file:
            json.dump(json_response, file, indent=4)
        return json_response


# -------- ETF ---------------------------------------------------------------------------------------
class Etf(Service):
    """Requests and load ETF data"""

    def __init__(self) -> None:
        super().__init__()

    def get_etf_components(self):
        pass

    # later, to be optimized (concurrently/parallel...)
    # if execution time is too long, otherwise let's keep it simple
    def load_ohlcv_all(self, start: Union[datetime, date], end: Union[datetime, date]):
        """Loads ohlcv ETF data for global ETF universe."""

        self.load_us_eq_sector(start=start, end=end)
        _logger.info(f"Ohlcv retrieval for us equity sector etfs is done!")
        self.load_us_eq_index(start=start, end=end)
        _logger.info(f"Ohlcv retrieval for us equity main indices is done!")
        self.load_eq_dev_country(start=start, end=end)
        _logger.info(f"Ohlcv retrieval for developed countries equity etfs is done!")
        self.load_eq_em_country(start=start, end=end)
        _logger.info(f"Ohlcv retrieval for emerging countries equity etfs is done!")
        self.load_us_fi_etf(start=start, end=end)
        _logger.info(f"Ohlcv retrieval for us fixed income etfs is done!")
        self.load_commo_etf(start=start, end=end)
        _logger.info(f"Ohlcv retrieval for commodity etfs is done!")

    @file_dump(f"{OUTPUT_ETF_OHLCV}/us_eq_sector.h5")
    def load_us_eq_sector(
        self,
        start: Union[datetime, date],
        end: Union[datetime, date],
        exchange: str = "US",
    ) -> List[Dict]:
        """
        Returns a list of historical Open-High-Low-Close-Volume (OHLCV) data for us equity sector etfs,
        as specified in the global universe configuration file.
        """
        us_eq_sector_universe = self.universe.us_eq_sector
        eodquery = EodQueryOhlcv(
            exchange=exchange, start=start, end=end, tickers=us_eq_sector_universe
        )
        return self.eod.ohlcv(eodquery=eodquery)

    @file_dump(f"{OUTPUT_ETF_OHLCV}/us_eq_index.h5")
    def load_us_eq_index(
        self,
        start: Union[datetime, date],
        end: Union[datetime, date],
        exchange: str = "US",
    ) -> List[Dict]:
        """
        Returns a list of historical Open-High-Low-Close-Volume (OHLCV) data for us equity main indices,
        as specified in the global universe configuration.
        """
        us_eq_index_universe = self.universe.us_eq_index
        eodquery = EodQueryOhlcv(
            exchange=exchange, start=start, end=end, tickers=us_eq_index_universe
        )
        return self.eod.ohlcv(eodquery=eodquery)

    @file_dump(f"{OUTPUT_ETF_OHLCV}/eq_dev_country_etf.h5")
    def load_eq_dev_country(
        self,
        start: Union[datetime, date],
        end: Union[datetime, date],
        exchange: str = "US",
    ) -> List[Dict]:
        """
        Returns a list of historical Open-High-Low-Close-Volume (OHLCV) data for developed countries equity etfs,
        as specified in the global universe configuration.
        """
        us_eq_dev_country_universe = self.universe.eq_dev_country
        eodquery = EodQueryOhlcv(
            exchange=exchange, start=start, end=end, tickers=us_eq_dev_country_universe
        )
        return self.eod.ohlcv(eodquery=eodquery)

    @file_dump(f"{OUTPUT_ETF_OHLCV}/eq_em_country_etf.h5")
    def load_eq_em_country(
        self,
        start: Union[datetime, date],
        end: Union[datetime, date],
        exchange: str = "US",
    ) -> List[Dict]:
        """
        Returns a list of historical Open-High-Low-Close-Volume (OHLCV) data for emerging countries equity etfs,
        as specified in the global universe configuration.
        """
        eq_em_country_universe = self.universe.eq_em_country
        eodquery = EodQueryOhlcv(
            exchange=exchange, start=start, end=end, tickers=eq_em_country_universe
        )
        return self.eod.ohlcv(eodquery=eodquery)

    @file_dump(f"{OUTPUT_ETF_OHLCV}/us_fi_etf.h5")
    def load_us_fi_etf(
        self,
        start: Union[datetime, date],
        end: Union[datetime, date],
        exchange: str = "US",
    ) -> List[Dict]:
        """
        Returns a list of historical Open-High-Low-Close-Volume (OHLCV) data for us fixed income etfs,
        as specified in the global universe configuration.
        """
        us_fi_etf_universe = self.universe.us_fi_etf
        eodquery = EodQueryOhlcv(
            exchange=exchange, start=start, end=end, tickers=us_fi_etf_universe
        )
        return self.eod.ohlcv(eodquery=eodquery)

    @file_dump(f"{OUTPUT_ETF_OHLCV}/commo_etf.h5")
    def load_commo_etf(
        self,
        start: Union[datetime, date],
        end: Union[datetime, date],
        exchange: str = "US",
    ) -> List[Dict]:
        """
        Loads historical Open-High-Low-Close-Volume (OHLCV) data for commodity etfs as specified in the
        global universe configuration.
        """
        commo_etf_universe = self.universe.commo_etf
        eodquery = EodQueryOhlcv(
            exchange=exchange, start=start, end=end, tickers=commo_etf_universe
        )
        return self.eod.ohlcv(eodquery=eodquery)


# -------- CRYPTO ---------------------------------------------------------------------------------------
class Crypto(Service):
    pass


# -------- FUTURES ---------------------------------------------------------------------------------------
class Futures(Service):
    pass


# -------- MACRO -----------------------------------------------------------------------------------------
class Macro(Service):
    pass


# -------------- Main
if __name__ == "__main__":
    # eodquery = EodQueryOhlcv(tickers=["AAPL", "MCD"])
    # EtfData = Etf()
    # EtfData.load_ohlcv(eodquery=eodquery)

    miscData = miscData()
    print(miscData.get_supported_exchanges())
