import platform
import requests
import asyncio
import aiohttp
import logging

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
class TiingoQueryIntraday:
    """
    Build and returns a query datamodel for tiingo requets
    """

    # exchange: str = "US"
    # start: Union[datetime, date] = field(default=(date(2023, 4, 11)))
    # end: Union[datetime, date] = date(2023, 4, 12)
    # tickers: List[str] = field(default_factory=List)

    @staticmethod
    def get_urls_queries(
        Tiingoquery: "TiingoQueryIntraday", root_url: str
    ) -> List[str]:
        """
        Returns a list of all urls to be requested
        """
        pass


class TiingoError(Exception):
    pass


class InvalidTiingoKeyError(TiingoError):
    pass


class Tiingo(BaseLoader):
    API_KEYS_SECTION_NAME = "API_KEYS"
    API_KEY_NAME = "tiingo_api_key"
    # ROOT_URL = "https://eodhistoricaldata.com/api"

    def __init__(self) -> None:
        super().__init__()
        try:
            if self.api_key is None:
                raise InvalidTiingoKeyError(f"{Tiingo.API_KEY_NAME} cannot be None!")
            self.params = {
                "api_token": "demo",
                "fmt": "json",
            }
        except InvalidTiingoKeyError as e:
            _logger.exception(e)
            raise

    def api_supported_exchanges(self):
        pass

    def exchange_traded_tickers(self):
        pass
