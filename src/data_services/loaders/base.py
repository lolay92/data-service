import logging
import logging.config
import os
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Union, List, Optional
from datetime import datetime, date
from enum import Enum, auto
from dotenv import load_dotenv

from src.data_services.utils.log_utils import logging_dict

# Initialize logger
logging.config.dictConfig(logging_dict)
_logger = logging.getLogger(__name__)

# load env secret keys
load_dotenv()


class Api(Enum):
    EODHISTORICALDATA = auto()
    TIINGO = auto()
    FRED = auto()


@dataclass
class DataQuery:
    """
    Build and returns a query datamodel for any api requests.
    Currently, queries for multiple tickers is possible only for same exchange
    """

    start: Union[datetime, date]
    end: Union[datetime, date]
    exchange: str = "US"
    tickers: List[str] = field(default_factory=List)


class BaseLoader(ABC):
    """BaseLoader class model that allows to implement api providers classes"""

    def __init__(self):
        # Load api key
        self.api_key = os.environ.get(self.API.name.lower())
        _logger.info(f"Api key for {self.API} is loaded")

    @abstractmethod
    def supported_exchanges(self):
        pass

    @abstractmethod
    def exchange_traded_tickers(self, exchange_code: str, delisted: Optional[bool]):
        pass
