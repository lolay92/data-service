import asyncio
import pickle
import aiofiles
from pathlib import Path
from functools import wraps


# ---------FILE MANAGER
async def pkl_dump(filepath, data):
    # Perform all necessary checks for file existence
    filepath = Path(filepath)
    if not filepath.is_file():
        filepath_parent_dir = filepath.parent
        filepath_parent_dir.mkdir(parents=True, exist_ok=True)
        filepath.touch()
    async with aiofiles.open(filepath, "ab") as output_file:
        await output_file.write(pickle.dumps(data))


async def pkl_dumps(filepath_parent, universe, responses_data):
    # Gathering coroutine tasks
    tasks = [
        pkl_dump(f"{filepath_parent}/{ticker}.pkl", resp)
        for ticker, resp in zip(universe, responses_data)
    ]
    await asyncio.gather(*tasks)


def file_dumper(filepath_parent):
    def decorator(func):
        def wrapper(*args, **kwargs):
            responses_data = func(*args, **kwargs)
            eodquery = kwargs["eodquery"]
            tickers = eodquery.tickers
            return asyncio.run(pkl_dumps(filepath_parent, tickers, responses_data))

        return wrapper

    return decorator


# ---------RESPONSE HANDLER
# universe_name = us_eq_sector
# filepath_parent = Output/ETF/ohclv/{universe_name}
