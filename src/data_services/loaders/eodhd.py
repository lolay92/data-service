import platform
import requests
import asyncio
import aiohttp
import logging
import json

from typing import List, Union, Dict
from dataclasses import dataclass, field
from datetime import datetime, date

from data_services.loaders.base import BaseLoader
from data_services.utils.log_utils import logging_dict

# Initialize logger
logging.config.dictConfig(logging_dict)
_logger = logging.getLogger(__name__)

# Work around solution to avoid RuntimeError from event loop policy
# that can appear for windows systems when working with asyncio
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@dataclass
class EodQueryOhclv:
    """
    Build tand returns a list of async
    Currently, queries for multiple tickers is possible only for same exchange
    """

    exchange: str = "US"
    start: Union[datetime, date] = field(default=(date(2001, 1, 1)))
    end: Union[datetime, date] = date.today()
    tickers: List[str] = field(default_factory=List)

    @staticmethod
    def get_urls_queries(eodquery: "EodQueryOhclv", root_url: str) -> List[str]:
        """
        Returns a list of all urls to be requested
        """
        tickers = eodquery.tickers
        urls = [f"{root_url}/eod/{ticker}.{eodquery.exchange}" for ticker in tickers]
        return urls


class EodhdError(Exception):
    pass


class InvalidEodKeyError(EodhdError):
    pass


class Eodhd(BaseLoader):
    API_KEYS_SECTION_NAME = "API_KEYS"
    API_KEY_NAME = "eodhd_api_key"
    ROOT_URL = "https://eodhistoricaldata.com/api"

    def __init__(self) -> None:
        super().__init__()
        try:
            if self.api_key is None:
                raise InvalidEodKeyError(f"{Eodhd.API_KEY_NAME} cannot be None!")
            self.params = {
                "api_token": "demo",
                "fmt": "json",
            }
        except InvalidEodKeyError as e:
            _logger.exception(e)
            raise

    def search(self, search_query: str, limit: int = 50) -> requests.models.Response:
        """
        Returns all elements relative to the query from eod search api
        """
        self.params.update({"limit": limit})
        url = f"{Eodhd.ROOT_URL}/search/{search_query}"
        with requests.Session() as requests_session:
            response = requests_session.get(url=url, params=self.params)
        return response

    def get_api_supported_exchanges(self) -> requests.models.Response:
        """
        api supported exchanges in json fmt
        """
        url = f"{Eodhd.ROOT_URL}/exchanges-list/"
        with requests.Session() as requests_session:
            response = requests_session.get(url=url, params=self.params)
        return response

    def get_exchange_traded_tickers(
        self, exchange_code: str, delisted: bool = False
    ) -> requests.models.Response:
        """
        Get traded tickers from api
        """
        if delisted:
            self.params.update({"delisted": 1})
        url = f"{Eodhd.ROOT_URL}/exchange-symbol-list/{exchange_code}"
        with requests.Session() as requests_session:
            response = requests_session.get(url=url, params=self.params)
        return response

    def get_exchanges_holidays(self):
        pass

    async def _fetch_json(self, response):
        json_response = await response.json()
        return json_response

    async def _fetch_ohlcv_async_mode(self, eodquery: EodQueryOhclv) -> List[Dict]:
        """
        fetch ohclv data asynchronously
        """
        # Updating http request parameters
        self.params.update(
            {
                "from": eodquery.start.strftime("%Y-%m-%d"),
                "to": eodquery.end.strftime("%Y-%m-%d"),
            }
        )
        # Asynchronous requests
        async with aiohttp.ClientSession() as aiohttp_session:
            urls = EodQueryOhclv.get_urls_queries(
                eodquery=eodquery, root_url=Eodhd.ROOT_URL
            )

            tasks = [aiohttp_session.get(url, params=self.params) for url in urls]

            responses = await asyncio.gather(*tasks)
            responses_json = await asyncio.gather(
                *[self._fetch_json(response) for response in responses]
            )
        return responses_json

    def _fetch_ohlcv_bulk_mode(self):
        pass

    def fetch_ohlcv(
        self, eodquery: EodQueryOhclv, bulk_mode: bool = False
    ) -> List[Dict]:
        """
        Returns ohclv JSON data
        """
        if bulk_mode:
            _logger.error("_fetch_ohlcv_bulk_mode function not implemented yet!")
        else:
            _logger.info("Fetching data...")
            responses = asyncio.run(self._fetch_ohlcv_async_mode(eodquery=eodquery))
            _logger.info("Fetching Completed!")
        return responses
