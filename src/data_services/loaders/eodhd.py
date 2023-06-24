import requests
import asyncio
import aiohttp
import logging

from typing import List, Dict

from data_services.loaders.base import BaseLoader, Api, DataQuery
from data_services.utils.log_utils import logging_dict

# Initialize logger
logging.config.dictConfig(logging_dict)
_logger = logging.getLogger(__name__)


class EodhdError(Exception):
    pass


class InvalidEodKeyError(EodhdError):
    pass


class Eodhd(BaseLoader):
    API = Api.EODHISTORICALDATA
    ROOT_URL = "https://eodhistoricaldata.com/api"

    def __init__(self) -> None:
        super().__init__()
        try:
            if self.api_key is None:
                raise InvalidEodKeyError(f"{Eodhd.API.name} api_key cannot be None!")
            self.params = {
                "api_token": self.api_key,
                "fmt": "json",
            }
        except InvalidEodKeyError as e:
            _logger.exception(e)
            raise

    def supported_exchanges(self) -> List[Dict]:
        """
        api supported exchanges in json fmt
        """
        url = f"{Eodhd.ROOT_URL}/exchanges-list/"
        with requests.Session() as requests_session:
            response = requests_session.get(url=url, params=self.params)
        return response.json()

    def exchange_traded_tickers(
        self, exchange_code: str, delisted: bool = False
    ) -> List[Dict]:
        """
        Get traded tickers from api
        """
        if delisted:
            self.params.update({"delisted": 1})
        url = f"{Eodhd.ROOT_URL}/exchange-symbol-list/{exchange_code}"
        with requests.Session() as requests_session:
            response = requests_session.get(url=url, params=self.params)
        return response.json()

    def search(self, search_query: str, limit: int = 50) -> List[Dict]:
        """
        Returns all elements relative to the query from eod search api
        """
        self.params.update({"limit": limit})
        url = f"{Eodhd.ROOT_URL}/search/{search_query}"
        with requests.Session() as requests_session:
            response = requests_session.get(url=url, params=self.params)
        return response.json()

    async def ohlcv(
        self,
        ohlcv_query: DataQuery,
    ) -> List[Dict]:
        """
        fetch ohlcv data asynchronously
        """
        # Updating http request parameters
        self.params.update(
            {
                "from": ohlcv_query.start.strftime("%Y-%m-%d"),
                "to": ohlcv_query.end.strftime("%Y-%m-%d"),
            }
        )

        # Get json data asynchronously
        async def _fetch_json(response):
            json_response = await response.json()
            return json_response

        # Asynchronous requests
        async with aiohttp.ClientSession() as aiohttp_session:
            urls = [
                f"{Eodhd.ROOT_URL}/eod/{ticker}.{ohlcv_query.exchange}"
                for ticker in ohlcv_query.tickers
            ]

            tasks = [aiohttp_session.get(url, params=self.params) for url in urls]

            responses = await asyncio.gather(*tasks)
            responses_json = await asyncio.gather(
                *[_fetch_json(response) for response in responses]
            )
        return responses_json
