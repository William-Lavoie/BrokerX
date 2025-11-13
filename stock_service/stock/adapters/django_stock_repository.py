from stock.adapters.dao.mysql_stock_dao import MySQLStockDAO
from stock.adapters.redis.redis_stock import RedisStock
from stock.domain.entities.stock import Stock, StockInvalidException
from stock.domain.ports.dao.stock_dao import StockDAO
from stock.domain.ports.stock_repository import StockDTO, StockRepository

from stock_service.exceptions import DataAccessException


class DjangoStockRepository(StockRepository):
    def __init__(self, dao=None, redis=None):
        super().__init__()
        self.dao: StockDAO = dao if dao is not None else MySQLStockDAO()
        self.redis = redis if redis is not None else RedisStock()

    def get_stock_by_symbol(self, symbol: str) -> Stock:
        redis_stock = self.redis.get_stock(symbol=symbol)

        if redis_stock:
            return redis_stock

        stock_dto: StockDTO = self.dao.get_stock_by_symbol(symbol)

        if not stock_dto.success:
            if stock_dto.code == 404:
                raise StockInvalidException(error_code=404)
            else:
                raise DataAccessException(
                    user_message=f"An unexpected error occurred when trying to access {symbol}"
                )

        stock = super().get_from_dto(stock_dto)
        self.redis.set_stock(stock=stock)
        return stock
