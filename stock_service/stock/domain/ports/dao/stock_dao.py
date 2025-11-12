from abc import abstractmethod

from stock.domain.ports.stock_repository import StockDTO


class StockDAO:
    @abstractmethod
    def get_stock_by_symbol(self, symbol: str) -> StockDTO:
        pass
