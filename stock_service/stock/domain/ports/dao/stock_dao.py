from abc import abstractmethod
from decimal import Decimal

from stock.domain.ports.stock_repository import StockDTO


class StockDAO:
    @abstractmethod
    def get_stock_by_symbol(self, symbol: str) -> StockDTO:
        pass

    @abstractmethod
    def set_bid(symbol: str, quantity: int, price: Decimal):
        pass

    @abstractmethod
    def set_ask(symbol: str, quantity: int, price: Decimal):
        pass