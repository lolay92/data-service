import logging

from abc import ABC, abstractmethod
from typing import Dict

from data_services.utils.log_utils import logging_dict
from data_services.utils.mykey import get_api_keys

# Initialize logger
logging.config.dictConfig(logging_dict)
_logger = logging.getLogger(__name__)


class BaseLoader(ABC):
    """BaseLoader class model that allows to implement api providers classes"""

    def __init__(self) -> None:
        api_keys = get_api_keys()
        try:
            if isinstance(api_keys, Dict):
                self.api_key = api_keys[self.API_KEY_NAME]
                _logger.info(f"Api key loaded from env...Done: {self.API_KEY_NAME}")
            else:
                self.api_key = api_keys[self.API_KEYS_SECTION_NAME][self.API_KEY_NAME]
                _logger.info(
                    f"Api key loaded from .ini file...Done: {self.API_KEY_NAME}"
                )
        except KeyError as e:
            _logger.exception(f"API_KEYS_SECTION_NAME or API_KEY_NAME error -- {e}")
            raise

    @abstractmethod
    def api_supported_exchanges(self):
        pass

    @abstractmethod
    def exchange_traded_tickers(self):
        pass
