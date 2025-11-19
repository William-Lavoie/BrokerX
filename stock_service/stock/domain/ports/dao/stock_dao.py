from abc import abstractmethod
from decimal import Decimal
from typing import Optional

from stock.domain.ports.stock_repository import StockDTO


class StockDAO:
    @abstractmethod
    def get_stock_by_symbol(self, symbol: str) -> StockDTO:
        pass

    @abstractmethod
    def set_bid(self, symbol: str, quantity: int, price: Optional[Decimal]):
        pass

    @abstractmethod
    def set_ask(self, symbol: str, quantity: int, price: Optional[Decimal]):
        pass