import logging
import asyncio
import typing
from datetime import datetime
import pandas as pd

import data_services.utils.paths as output_paths

from data_services.vendors.vendor import MarketDataVendor, VALID_VENDORS
from data_services.utils.universe import Universe
from data_services.utils.log import logging_dict
from data_services.utils.data_process_utils import (
    TimeSeriesDataQuery,
    parallel_data_processing,
    remove_duplicates,
)

# Initialize logger
logging.config.dictConfig(logging_dict)
_logger = logging.getLogger(__name__)


def build_ohlcv_query(
    universe: Universe | typing.Tuple,
    start: type[datetime],
    end: type[datetime],
    exchange: str = "US",
):
    """
    Build query for fetching ohlcv data

    """
    if isinstance(universe, typing.Tuple):
        _logger.info("Loading custom universe parameters....")
        universe_name = universe[0]
        symbols = universe[1]
    else:
        _logger.info("Loading universe parameters....")
        universe_name = universe.value[0]
        symbols = universe.value[2]

    return universe_name, TimeSeriesDataQuery(start, end, exchange, symbols)


def h5_archive(path: str, data: typing.Tuple[str, typing.List[typing.Dict]]):
    processed_data = parallel_data_processing(data.values())

    with pd.HDFStore(path, mode="a", complevel=9, complib="blosc", index=False) as store:
        for symbol, symbol_data in zip(data.keys(), processed_data):
            if f"/{symbol}" in store.keys():
                # Handle duplicates rows for existing symbol
                remove_duplicates(store[symbol], symbol_data)
            store.append(symbol, symbol_data)

    return


async def get_data(
    vendor: type[MarketDataVendor],
    universe: Universe | typing.Tuple,
    start: type[datetime],
    end: type[datetime],
    exchange: str = "US",
    do_archive: bool = False,
) -> typing.Coroutine[any, any, any]:
    """
    Returns a list of historical Open-High-Low-Close-Volume (OHLCV) data
    for a defined universe, as specified in the global universe
    configuration file.

    """
    if vendor.__name__ not in VALID_VENDORS:
        _logger.error("Invalid vendor provided!")
        raise ValueError("Vendor provided is not valid or implemented!")

    provider = vendor()
    universe_name, query = build_ohlcv_query(universe, start=start, end=end, exchange=exchange)

    _logger.info(f"Now fetching Ohlcv data for {universe_name}...")
    universe_filepath = f"{output_paths.OUTPUT_ETF_OHLCV}/{universe_name}.h5"
    _logger.info(f"Vendor: {provider.__class__.__name__}")
    if not hasattr(provider, "fetch_multi_symbols_data"):
        raise NotImplementedError("'fetchMultiSymbols' method has not been implemented for this vendor...")

    data = await provider.fetch_multi_symbols_data(query=query)

    if do_archive:
        h5_archive(universe_filepath, data)

    return universe_name, data


def get_last_data(
    vendor: type[MarketDataVendor],
    universe: Universe | typing.Tuple,
    exchange: str = "US",
    do_archive: bool = False,
):
    """
    Returns last day Open-High-Low-Close-Volume (OHLCV) data
    for a defined universe, as specified in the global universe
    configuration file.

    """
    start = end = datetime.now()
    return asyncio.run(get_data(vendor, universe, start, end, exchange, do_archive))
