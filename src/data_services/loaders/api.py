from dataclasses import dataclass, field
from typing import Callable, List

from data_services.loaders.eodhd import Eodhd


@dataclass
class Service:
    api: Callable = field(init=True, default_factory=Eodhd)
    api2: Callable = Eodhd()


# class Data:
#     # def __init__(self, apiServiceName: str) -> None:
#     #     api = ApiServiceInitializer(apiServiceName).api

#     def __init__(self) -> None:
#         self.api = Service().api
#         self.api2 = Service().api2


# class EtfData(Data):
#     def __init__(self) -> None:
#         super().__init__()

#     def fetch_ohclv(self):
#         query = EodQueryOhclv(tickers=["AAPL"])
#         return self.api2.fetch_ohlcv(eodquery=query)


# if __name__ == "__main__":
#     data = EtfData()
#     data = data.fetch_ohclv()
#     print(data)

if __name__ == "__main__":
    eod = Eodhd()
    eod.ohlcv
