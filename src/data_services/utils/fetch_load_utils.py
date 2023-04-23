import pickle
import json
import pandas as pd
from pathlib import Path
from functools import wraps


# ---------FILE MANAGER
def file_dump(filepath: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            responses_data = func(*args, **kwargs)
            eodquery = kwargs["eodquery"]
            tickers = eodquery.tickers
            # Create file for appending if it not exists already
            filepath = Path(filepath)
            filepath.touch(exist_ok=True)
            with pd.HDFStore(filepath, mode="a") as store:
                for ticker, resp in zip(tickers, responses_data):
                    store["ticker"] = resp

            return responses_data

        return wrapper

    return decorator


# ---------RESPONSE HANDLER
