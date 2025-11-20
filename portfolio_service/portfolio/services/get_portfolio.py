import logging
from typing import Optional

from portfolio_service.use_case_results import UseCaseResult


logger = logging.getLogger("portfolio")


class GetStockInfoUseCaseResult(UseCaseResult):
    def __init__(self, message: str, code: int, portfolio: Optional[Portfolio]):
        super().__init__(message=message, code=code)
        self.stock = stock

    def to_dict(self):
        dict = super().to_dict()
        if self.stock is not None:
            dict["stock"] = self.stock.to_dict()
            
        return dict


class GetStockInfoUseCase:
    def __init__(
        self,
        stock_repository: StockRepository,
    ):
        self.stock_repository = stock_repository

    def get_top_of_book(self, symbol: str) -> GetStockInfoUseCaseResult:
        try:
            stock: Stock = self.stock_repository.get_stock_by_symbol(symbol=symbol)

            return GetStockInfoUseCaseResult(
                message=f"Successfully retrieved stock info for {symbol}.",
                code=200,
                stock=stock,
            )

        except StockInvalidException as stock_exception:
            logger.warning(
                f"StockInvalidException in GetStockInfoUseCaseResult for symbol {symbol}: {stock_exception.log_message} Code: {stock_exception.error_code}"
            )
            return GetStockInfoUseCaseResult(
                message=stock_exception.user_message,
                code=stock_exception.error_code,
                stock=None,
            )

        except DataAccessException as data_access_exception:
            return GetStockInfoUseCaseResult(
                message=data_access_exception.user_message,
                code=data_access_exception.error_code,
                stock=None,
            )
