import logging
import json
import asyncio
from datetime import datetime, date
from typing import Dict, List, Union, Tuple
from dataclasses import dataclass, field
from pathlib import Path

from data_services.loaders.eodhd import Eodhd, EodQueryOhlcv
from data_services.loaders.tiingo import Tiingo, TiingoQueryIntraday
from data_services.utils.universe import UniverseMap, QueryUniverse

from data_services.utils.log_utils import logging_dict
from data_services.utils.fetch_utils import file_dump

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

from enum import Enum


@dataclass(frozen=True)
class Service:
    """Service base class to initialize the relevant api for data services"""

    eod: Eodhd = Eodhd()
    tiingo: Tiingo = Tiingo()
    # universe: QueryUniverse = field(default_factory=QueryUniverse)


# -------- Miscellaneous data ----------------------------------------------------------------------------
class MiscData(Service):
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

    @file_dump
    async def _load_etf_universe_async(
        self,
        start: Union[datetime, date],
        end: Union[datetime, date],
        universe_type: UniverseMap,
    ):
        """
        Returns a list of historical Open-High-Low-Close-Volume (OHLCV) data for a defined universe,
        as specified in the global universe configuration file.
        """
        universe = QueryUniverse(universe_type)
        _logger.info(f"Ohlcv retrieval for {universe.properties.value} etfs...")
        eodquery = EodQueryOhlcv(start=start, end=end, tickers=universe.components)
        ohlcv_data = await self.eod.ohlcv(eodquery=eodquery)
        filepath_universe = f"{OUTPUT_ETF_OHLCV}/{universe.properties.value}.h5"
        _logger.info(f"Retrieval done for {universe.properties.value} etfs! ")
        return filepath_universe, eodquery.tickers, ohlcv_data

    def load_etf_universe(
        self,
        universe_type: UniverseMap,
        start: Union[datetime, date],
        end: Union[datetime, date],
        save_to_file: bool = False,
    ) -> Tuple[List[str], List[Dict]]:
        """loads a specific etf universe for a specific period"""

        if save_to_file:
            return asyncio.run(
                self._load_etf_universe_async(
                    start=start, end=end, universe_type=universe_type
                )
            )
        else:
            load_func = self._load_etf_universe_async.__wrapped__
            return asyncio.run(
                load_func(self, start=start, end=end, universe_type=universe_type)
            )

    def load_all_etf(self, start: Union[datetime, date], end: Union[datetime, date]):
        """Loads all etfs data asynchronously for a specific period."""

        async def _load_all_etf_async():
            """Create asynchronous tasks for global ETF universe retrieval."""

            tasks = [
                asyncio.create_task(
                    self._load_etf_universe_async(
                        start=start, end=end, universe_type=UniverseMap.US_EQ_SECTOR
                    )
                ),
                asyncio.create_task(
                    self._load_etf_universe_async(
                        start=start, end=end, universe_type=UniverseMap.US_EQ_INDEX
                    )
                ),
                asyncio.create_task(
                    self._load_etf_universe_async(
                        start=start, end=end, universe_type=UniverseMap.EQ_DEV_COUNTRY
                    )
                ),
                asyncio.create_task(
                    self._load_etf_universe_async(
                        start=start, end=end, universe_type=UniverseMap.EQ_EM_COUNTRY
                    )
                ),
                asyncio.create_task(
                    self._load_etf_universe_async(
                        start=start, end=end, universe_type=UniverseMap.US_FI_ETF
                    )
                ),
                asyncio.create_task(
                    self._load_etf_universe_async(
                        start=start, end=end, universe_type=UniverseMap.COMMO_ETF
                    )
                ),
            ]

            return await asyncio.gather(*tasks)

        data = asyncio.run(_load_all_etf_async())
        _logger.info(f"All OHLCV retrievals for ETFs completed!")

        return data


# -------- CRYPTO ---------------------------------------------------------------------------------------
class Crypto(Service):
    pass


# -------- FUTURES ---------------------------------------------------------------------------------------
class Futures(Service):
    pass


# -------- MACRO -----------------------------------------------------------------------------------------
class Macro(Service):
    pass
