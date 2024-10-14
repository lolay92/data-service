import typing
import json
import logging

from data_services.utils.log import logging_dict
from data_services.vendors.vendor import MarketDataVendor, VALID_VENDORS
import data_services.utils.paths as output_paths


# Initialize logger
logging.config.dictConfig(logging_dict)
_logger = logging.getLogger(__name__)


# MISCELLANEOUS DATA
class Miscellaneous:
    """
    Requests and load miscellaneous data

    """

    def __init__(self, vendor: type[MarketDataVendor]) -> None:
        self._vendor = vendor()  # Initialize a vendor class like Eodhd...

    @property
    def vendor(self) -> str:
        return self._vendor.__class__.__name__

    @vendor.setter
    def vendor(self, vendor: type[MarketDataVendor]) -> None:
        if vendor.__name__ not in VALID_VENDORS:
            raise ValueError("Vendor provided is not valid or implemented!")
        else:
            self._vendor = vendor()

    def search(self, query: str) -> typing.List[typing.Dict]:
        if hasattr(self._vendor, "search"):
            return self._vendor.search(search_query=query)
        else:
            raise NotImplementedError(
                f"Search method is not implemented for this vendor: {self._vendor.__class__.__name__}"
            )

    def get_exchanges(self) -> typing.List[typing.Dict]:
        """
        Get supported exchanges by the vendor

        """
        json_response = self._vendor.fetch_supported_exchanges()
        with open(
            f"{output_paths.OUTPUT_METADATA}/{self._vendor.__class__.__name__}_supported_exchanges.json",
            "w",
        ) as file:
            json.dump(json_response, file, indent=4)
            _logger.info(
                f"Successfully fetch a list of supported exchanges of: {self._vendor.__class__.__name__}"
            )
        return json_response

    def get_symbols_from_exchange(
        self,
        exchange_code: str = "US",
        delisted: typing.Optional[bool] = False,
    ) -> typing.List[typing.Dict]:
        """
        Get traded symbols available

        """
        json_response = self._vendor.fetch_symbols_from_exchange(
            exchange_code=exchange_code, delisted=delisted
        )
        with open(f"{output_paths.OUTPUT_METADATA}/{exchange_code}_tickers.json", "w") as file:
            json.dump(json_response, file, indent=4)
            _logger.info(f"Successfully fetch a list of symbols of exchange: {exchange_code}")
        return json_response
