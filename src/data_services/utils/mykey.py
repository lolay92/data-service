import os
import logging
import logging.config
from typing import Dict, Union
from configparser import ConfigParser

from data_services.utils.log_utils import logging_dict, log_exception

# Initialize logger
logging.config.dictConfig(logging_dict)
_logger = logging.getLogger(__name__)

# List of APIs
API_KEY_NAME_LIST = [
    "eodhd_api_key",
    "tiingo_api_key",
    "fred_api_key",
    "SimFin_api_key",
]

# Configuration file name
KEY_FILEPATH = "./src/data_services/utils/constants/mykey.ini"

# Initializing the logger
logging.config.dictConfig(logging_dict)
_logger = logging.getLogger(__name__)


def _load_from_key_file() -> ConfigParser:
    """Get api_tokens from a configuration file."""
    Keys_file = ConfigParser()
    Keys_file.read(KEY_FILEPATH)
    return Keys_file


def _load_api_key_from_env() -> Dict:
    """Get api_tokens from variables environment."""
    tokens: Dict = {}
    for api_key_name in API_KEY_NAME_LIST:
        if os.getenv(api_key_name) is None:
            _logger.warning(
                f"Unable to find the key in the env variables: {api_key_name}"
            )
        tokens[api_key_name] = os.getenv(api_key_name)
    return tokens


@log_exception(_logger)
def get_api_keys() -> Union[Dict, ConfigParser]:
    """Get api tokens from configuration file or vars environment."""
    if os.path.exists(KEY_FILEPATH):
        return _load_from_key_file()
    else:
        _logger.warning(f"Unable to find the configuration file: {KEY_FILEPATH}")
        return _load_api_key_from_env()
