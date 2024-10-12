import typing
import logging.config
import asyncio
import aiohttp

from data_services.utils.log import logging_dict
from data_services.utils.generic import DataQuery
from data_services.utils.http_response_handler import async_response_handler, retry
from enum import Enum, auto

# Initialize logger
logging.config.dictConfig(logging_dict)
_logger = logging.getLogger(__name__)

VALID_VENDORS = [
    "EodhdVendor",
    "TiingoVendor",
    "PolygonVendor",
]

class DataVendors(Enum):
    EODHISTORICALDATA = auto()
    TIINGO = auto()
    POLYGON = auto()

class MarketDataVendor(typing.Protocol):
    """Base Server protocol interface to implement api providers classes."""

    def fetch_supported_exchanges(self) -> typing.List[typing.Dict]: ...

    def fetch_symbols_from_exchange(self, exchange_code: str, delisted: typing.Optional[bool]) -> typing.List[typing.Dict]: ...