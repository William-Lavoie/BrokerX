from ..adapters.dao.mysql_stock_dao import MySQLStockDAO
from ..domain.entities.stock import Stock, StockInvalidException
from ..domain.ports.dao.stock_dao import StockDAO
from ..domain.ports.stock_repository import StockDTO, StockRepository
from ..exceptions import DataAccessException


class DjangoStockRepository(StockRepository):
    def __init__(self, dao=None):
        super().__init__()
        self.dao: StockDAO = dao if dao is not None else MySQLStockDAO()

    def get_stock_by_symbol(self, symbol: str) -> Stock:
        stock_dto: StockDTO = self.dao.get_stock_by_symbol(symbol)

        if not stock_dto.success:
            if stock_dto.code == 404:
                raise StockInvalidException(error_code=404)
            else:
                raise DataAccessException(
                    user_message=f"An unexpected error occurred when trying to access {symbol}"
                )

        return super().get_from_dto(stock_dto)
