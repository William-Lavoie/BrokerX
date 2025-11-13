from abc import abstractmethod
from dataclasses import dataclass
from decimal import Decimal

from stock.adapters.result import Result
from stock.domain.entities.stock import Stock


@dataclass
class StockDTO(Result):
    symbol: str = ""
    name: str = ""
    exchange: str = ""
    currency: str = "CAD"
    last_price: Decimal = Decimal("0.00")
    open_price: Decimal = Decimal("0.00")
    high_price: Decimal = Decimal("0.00")
    low_price: Decimal = Decimal("0.00")
    close_price: Decimal = Decimal("0.00")
    bid_price: Decimal = Decimal("0.00")
    bid_size: int = 0
    ask_price: Decimal = Decimal("0.00")
    ask_size: int = 0
    volume: int = 0
    active: bool = True


class StockRepository:
    @abstractmethod
    def get_stock_by_symbol(self, symbol) -> Stock:
        pass

    def get_from_dto(cls, dto: StockDTO) -> "Stock":
        return Stock(
            symbol=dto.symbol,
            name=dto.name,
            exchange=dto.exchange,
            currency=dto.currency,
            last_price=dto.last_price,
            open_price=dto.open_price,
            high_price=dto.high_price,
            low_price=dto.low_price,
            close_price=dto.close_price,
            bid_price=dto.bid_price,
            bid_size=dto.bid_size,
            ask_price=dto.ask_price,
            ask_size=dto.ask_size,
            volume=dto.volume,
            active=dto.active,
        )
