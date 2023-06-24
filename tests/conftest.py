import pytest
from datetime import date
from src.data_services.loaders.eodhd import Eodhd
from src.data_services.loaders.base import DataQuery


@pytest.fixture
def dummy_eodhd():
    return Eodhd()


@pytest.fixture
def dummy_ohlcvquery():
    return DataQuery(
        exchange="US",
        start=date(2023, 1, 1),
        end=date(2023, 5, 31),
        tickers=["MCD", "AAPL"],
    )
