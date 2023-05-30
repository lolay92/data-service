import logging
import json
import asyncio
from datetime import datetime, date
from typing import Dict, List, Union, Tuple
from dataclasses import dataclass, field
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
    universe: UniverseQuery = field(default_factory=UniverseQuery)


class miscData(Service):
    """Requests and load miscellaneous data"""

    def __init__(self) -> None:
        super().__init__()

    def util_search(self, query: str) -> List[Dict]:
        return self.eod.search(search_query=query)

    def get_supported_exchanges(self, api: str = "eod") -> List[Dict]:
        """Get supported exchanges for a specific api data provider."""
        if api == "eod":
            json_response = self.eod.api_supported_exchanges()
        with open(f"{OUTPUT_MISC_DATA}/supported_exchanges.json", "w") as file:
            json.dump(json_response, file, indent=4)
        return json_response

    def get_exchange_traded_tickers(
        self, api: str = "eod", exchange_code: str = "US", delisted: bool = False
    ) -> List[Dict]:
        """Get traded tickers for a specific exchange and an api data provider."""
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

    def load_etf_specific_universe(
        self,
        universe: str,
        save_file: bool,
        start: Union[datetime, date],
        end: Union[datetime, date],
    ) -> Tuple[List[str], List[Dict]]:
        """loads a specific etf universe for a specific period:
        universe should be one of the following:
        - us_eq_sector
        - us_eq_index
        - eq_dev_country
        - eq_em_country
        - us_fi_etf
        - commo_etf
        """
        load_func = getattr(self, f"load_{universe.lower()}")

        if save_file:
            data = asyncio.run(load_func(start=start, end=end))
        else:
            load_func = load_func.__wrapped__
            data = asyncio.run(load_func(self, start=start, end=end))
        return data

    def load_all_ohlcv(self, start: Union[datetime, date], end: Union[datetime, date]):
        """Loads all etfs data asynchronously for a specific period."""

        async def _load_data_async():
            """Create asynchronous tasks for global ETF universe retrieval."""

            tasks = [
                asyncio.create_task(self.load_us_eq_sector(start=start, end=end)),
                asyncio.create_task(self.load_us_eq_index(start=start, end=end)),
                asyncio.create_task(self.load_eq_dev_country(start=start, end=end)),
                asyncio.create_task(self.load_eq_em_country(start=start, end=end)),
                asyncio.create_task(self.load_us_fi_etf(start=start, end=end)),
                asyncio.create_task(self.load_commo_etf(start=start, end=end)),
            ]

            return await asyncio.gather(*tasks)

        data = asyncio.run(_load_data_async())
        _logger.info(f"All OHLCV retrievals for ETFs completed!")

        return data

    @file_dump(f"{OUTPUT_ETF_OHLCV}/us_eq_sector.h5")
    async def load_us_eq_sector(
        self, start: Union[datetime, date], end: Union[datetime, date]
    ) -> Tuple[List[str], List[Dict]]:
        """
        Returns a list of historical Open-High-Low-Close-Volume (OHLCV) data for us equity sector etfs,
        as specified in the global universe configuration file.
        """
        _logger.info(f"Ohlcv retrieval for us equity sector etfs...")
        # us_eq_sector_universe = self.universe.us_eq_sector
        us_eq_sector_universe = ["MCD", "AAPL"]
        eodquery = EodQueryOhlcv(start=start, end=end, tickers=us_eq_sector_universe)
        ohlcv = await self.eod.ohlcv(eodquery=eodquery)
        return eodquery.tickers, ohlcv

    @file_dump(f"{OUTPUT_ETF_OHLCV}/us_eq_index.h5")
    async def load_us_eq_index(
        self, start: Union[datetime, date], end: Union[datetime, date]
    ) -> Tuple[List[str], List[Dict]]:
        """
        Returns a list of historical Open-High-Low-Close-Volume (OHLCV) data for us equity main indices,
        as specified in the global universe configuration.
        """
        _logger.info(f"Ohlcv retrieval for us equity main indices...")
        us_eq_index_universe = self.universe.us_eq_index
        eodquery = EodQueryOhlcv(start=start, end=end, tickers=us_eq_index_universe)
        ohlcv = await self.eod.ohlcv(eodquery=eodquery)
        return eodquery.tickers, ohlcv

    @file_dump(f"{OUTPUT_ETF_OHLCV}/eq_dev_country_etf.h5")
    async def load_eq_dev_country(
        self, start: Union[datetime, date], end: Union[datetime, date]
    ) -> Tuple[List[str], List[Dict]]:
        """
        Returns a list of historical Open-High-Low-Close-Volume (OHLCV) data for developed countries equity etfs,
        as specified in the global universe configuration.
        """
        _logger.info(f"Ohlcv retrieval for developed countries equity etfs...")
        us_eq_dev_country_universe = self.universe.eq_dev_country
        eodquery = EodQueryOhlcv(
            start=start, end=end, tickers=us_eq_dev_country_universe
        )
        ohlcv = await self.eod.ohlcv(eodquery=eodquery)
        return eodquery.tickers, ohlcv

    @file_dump(f"{OUTPUT_ETF_OHLCV}/eq_em_country_etf.h5")
    async def load_eq_em_country(
        self, start: Union[datetime, date], end: Union[datetime, date]
    ) -> Tuple[List[str], List[Dict]]:
        """
        Returns a list of historical Open-High-Low-Close-Volume (OHLCV) data for emerging countries equity etfs,
        as specified in the global universe configuration.
        """
        _logger.info(f"Ohlcv retrieval for emerging countries equity etfs...")
        eq_em_country_universe = self.universe.eq_em_country
        eodquery = EodQueryOhlcv(start=start, end=end, tickers=eq_em_country_universe)
        ohlcv = await self.eod.ohlcv(eodquery=eodquery)
        return eodquery.tickers, ohlcv

    @file_dump(f"{OUTPUT_ETF_OHLCV}/us_fi_etf.h5")
    async def load_us_fi_etf(
        self, start: Union[datetime, date], end: Union[datetime, date]
    ) -> Tuple[List[str], List[Dict]]:
        """
        Returns a list of historical Open-High-Low-Close-Volume (OHLCV) data for us fixed income etfs,
        as specified in the global universe configuration.
        """
        _logger.info(f"Ohlcv retrieval for us fixed income etfs...")
        us_fi_etf_universe = self.universe.us_fi_etf
        eodquery = EodQueryOhlcv(start=start, end=end, tickers=us_fi_etf_universe)
        ohlcv = await self.eod.ohlcv(eodquery=eodquery)
        return eodquery.tickers, ohlcv

    @file_dump(f"{OUTPUT_ETF_OHLCV}/commo_etf.h5")
    async def load_commo_etf(
        self, start: Union[datetime, date], end: Union[datetime, date]
    ) -> Tuple[List[str], List[Dict]]:
        """
        Loads historical Open-High-Low-Close-Volume (OHLCV) data for commodity etfs as specified in the
        global universe configuration.
        """
        _logger.info(f"Ohlcv retrieval for commodity etfs...")
        commo_etf_universe = self.universe.commo_etf
        eodquery = EodQueryOhlcv(start=start, end=end, tickers=commo_etf_universe)
        ohlcv = await self.eod.ohlcv(eodquery=eodquery)
        return eodquery.tickers, ohlcv


# -------- CRYPTO ---------------------------------------------------------------------------------------
class Crypto(Service):
    pass


# -------- FUTURES ---------------------------------------------------------------------------------------
class Futures(Service):
    pass


# -------- MACRO -----------------------------------------------------------------------------------------
class Macro(Service):
    pass
