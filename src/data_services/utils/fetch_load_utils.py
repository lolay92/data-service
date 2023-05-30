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


# ---------FILE MANAGER
def file_dump(filepath: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            func_results = await func(*args, **kwargs)
            tickers = func_results[0]

            with pd.HDFStore(filepath, mode="a") as store:
                for ticker, result in zip(tickers, func_results[1]):
                    result_df = pd.DataFrame(result)
                    result_df = preprocess_df(result_df)
                    store.append(ticker, result_df)

            return func_results

        return wrapper

    return decorator


# ---------RESPONSE HANDLER
