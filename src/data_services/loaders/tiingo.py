# import logging
# from data_services.loaders.base import BaseLoader, Api
# from data_services.utils.log_utils import logging_dict

# # Initialize logger
# logging.config.dictConfig(logging_dict)
# _logger = logging.getLogger(__name__)


# class TiingoError(Exception):
#     pass


# class InvalidTiingoKeyError(TiingoError):
#     pass


# class Tiingo(BaseLoader):
#     API = Api.TIINGO
#     ROOT_URL = "https://eodhistoricaldata.com/api"

#     def __init__(self) -> None:
#         super().__init__()
#         try:
#             if self.api_key is None:
#                 raise InvalidTiingoKeyError(f"{Tiingo.API.name} cannot be None!")
#             self.params = {
#                 "api_token": self.api_key,
#                 "fmt": "json",
#             }
#         except InvalidTiingoKeyError as e:
#             _logger.exception(e)
#             raise

#     def supported_exchanges(self):
#         pass

#     def exchange_traded_tickers(self, exchange_code: str, delisted: bool = False):
#         pass
