import pandas as pd
import typing
import concurrent.futures
from dataclasses import dataclass, field
from datetime import datetime, date


# -------------------------------------------------------------------------------------------------------------
# Query data stuctures
# -------------------------------------------------------------------------------------------------------------
@dataclass
class TimeSeriesDataQuery:
    """
    Build and returns a query datamodel for any api requests.
    Currently, queries for multiple tickers is possible only for same exchange.
    """

    start: typing.Union[datetime, date]
    end: typing.Union[datetime, date]
    exchange: str = "US"
    symbols: typing.List[str] = field(default_factory=list)


# -------------------------------------------------------------------------------------------------------------
# Data processing helpers
# -------------------------------------------------------------------------------------------------------------
def preprocess_data_helper(data: typing.Dict) -> typing.Dict:
    """
    Preprocess time series raw dataframe.
    """
    df = pd.DataFrame(data)
    df.date = pd.to_datetime(df.date)
    df.sort_values(by="date", inplace=True)
    df.set_index("date", inplace=True)
    return df


def parallel_data_processing(data: typing.List[typing.Dict]) -> typing.Iterable:
    """
    Preprocess concurrently list of time series raw dataframe.
    """
    with concurrent.futures.ProcessPoolExecutor() as pool:
        return pool.map(preprocess_data_helper, data)


def remove_duplicates(existing_df: pd.DataFrame, new_df: pd.DataFrame) -> typing.Union[None, pd.DataFrame]:
    """
    Remove duplicated data
    """
    duplicates = existing_df.index.intersection(new_df.index)
    if duplicates.empty:
        return new_df
    else:
        return new_df.drop(duplicates, inplace=True)
