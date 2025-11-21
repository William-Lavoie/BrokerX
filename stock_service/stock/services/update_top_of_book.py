import logging
from decimal import Decimal
from typing import Optional

from stock.domain.entities.stock import Stock, StockInvalidException
from stock.domain.ports.stock_repository import StockRepository

from stock_service.exceptions import DataAccessException
from stock_service.use_case_results import UseCaseResult

logger = logging.getLogger("stock")


class UpdateTopOfBookUseCaseResult(UseCaseResult):
    def __init__(self, message: str, code: int, price: Decimal):
        super().__init__(message=message, code=code)
        self.price = price

    def to_dict(self):
        dict = super().to_dict()
        dict["price"] = str(self.price)

        return dict


class UpdateTopOfBookUseCase:
    def __init__(
        self,
        stock_repository: StockRepository,
    ):
        self.stock_repository = stock_repository

    def update_top_of_book(
        self, symbol: str, quantity: int, type: str, price: Optional[Decimal] = None
    ) -> UpdateTopOfBookUseCaseResult:
        try:
            stock: Stock = self.stock_repository.get_stock_by_symbol(symbol=symbol)
            stock.validate_order(quantity=quantity, type=type, price=price)
            self.stock_repository.update_top_of_book(
                stock=stock, quantity=quantity, type=type, price=price
            )

            if price is None:
                if type == "BUY":
                    price = stock.bid_price
                elif type == "SELL":
                    price = stock.ask_price

            return UpdateTopOfBookUseCaseResult(
                message=f"Successfully retrieved stock info for {symbol}.",
                code=200,
                price=price,
            )

        except StockInvalidException as stock_exception:
            logger.warning(
                f"StockInvalidException in GetStockInfoUseCaseResult for symbol {symbol}: {stock_exception.log_message} Code: {stock_exception.error_code}"
            )
            return UpdateTopOfBookUseCaseResult(
                message=stock_exception.user_message,
                code=stock_exception.error_code,
                price=None,
            )

        except DataAccessException as data_access_exception:
            return UpdateTopOfBookUseCaseResult(
                message=data_access_exception.user_message,
                code=data_access_exception.error_code,
                price=None,
            )
