import platform
import requests
import asyncio
import aiohttp
import logging

from typing import List, Union, Dict
from dataclasses import dataclass, field
from datetime import datetime, date

from data_services.loaders.base import BaseLoader, InvalidApiKeyErr
from data_services.utils.log_utils import logging_dict

# Initialize logger
logging.config.dictConfig(logging_dict)
_logger = logging.getLogger(__name__)

# Work around solution to avoid RuntimeError from event loop policy
# that can appear for windows systems when working with asyncio
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class Tiingo(BaseLoader):
    API_KEYS_SECTION_NAME = "API_KEYS"
    API_KEY_NAME = "tiingo_api_key"
    ROOT_URL = "https://eodhistoricaldata.com/api"

    def __init__(self) -> None:
        super().__init__()
        try:
            if self.api_key is None:
                raise InvalidApiKeyErr(f"API key cannot be None: {Tiingo.API_KEY_NAME}")
            self.params = {
                "api_token": "demo",
                "fmt": "json",
            }
        except InvalidApiKeyErr as e:
            _logger.exception(e)
            raise

    def get_api_supported_exchanges(self):
        pass

    def get_exchange_traded_tickers(self):
        pass
