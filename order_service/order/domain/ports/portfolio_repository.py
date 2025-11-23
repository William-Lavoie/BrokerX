from abc import abstractmethod
from decimal import Decimal

from order.domain.entities.order import Order


class PortfolioException(Exception):

    def __init__(
        self,
        user_message: str = "There was an error with the portfolio.",
        log_message: str = "There was an error with the portfolio.",
        error_code: int = 500,
    ):
        super().__init__(user_message)
        self.user_message = user_message
        self.log_message = log_message
        self.error_code = error_code


class PortfolioRepository:

    @abstractmethod
    def reserve_holdings(self, order: Order) -> None:
        pass

    @abstractmethod
    def release_holdings(self, order: Order) -> None:
        pass
