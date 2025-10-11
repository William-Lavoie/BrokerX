from abc import abstractmethod
from dataclasses import dataclass
from decimal import Decimal

from ...adapters.result import Result
from ...domain.entities.stock import Stock


@dataclass
class StockDTO(Result):
    symbol: str = ""
    previous_close: Decimal = Decimal("0.00")
    volume: int = 0
    last_price: Decimal = Decimal("0.00")
    active: bool = True


class StockRepository:
    @abstractmethod
    def get_stock_by_symbol(self, symbol) -> Stock:
        pass
