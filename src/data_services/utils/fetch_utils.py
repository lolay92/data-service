import pandas as pd
from functools import wraps
from datetime import datetime, date


# ---------PREPROCESSIND DATAFRAME
def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess time series raw dataframe."""
    df.date = pd.to_datetime(df.date)
    df.sort_values(by="date", inplace=True)
    df.set_index("date", inplace=True)
    return df


def remove_duplicates(existing_df: pd.DataFrame, new_df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicated data"""
    duplicates = existing_df.index.intersection(new_df.index)
    if duplicates.empty:
        return new_df
    else:
        return new_df.drop(duplicates, inplace=True)


# ---------FILE MANAGER


def file_dump(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        filepath_universe, tickers, data = await func(*args, **kwargs)

        with pd.HDFStore(filepath_universe, mode="a") as store:
            for ticker, ticker_ts_data in zip(tickers, data):
                df = preprocess_df(pd.DataFrame(ticker_ts_data))
                # Handle duplicates for existing ticker
                if f"/{ticker}" in store.keys():
                    existing_df = store[ticker]
                    remove_duplicates(existing_df, df)
                    del existing_df
                # Append new data to existing ticker or create new table for a new ticker
                store.append(ticker, df)

        return data

    return wrapper


# ---------RESPONSE HANDLER
