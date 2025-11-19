from abc import abstractmethod

from order.domain.entities.order import Order


class StockException(Exception):

    def __init__(
        self,
        user_message: str = "There was an error with the stock.",
        log_message: str = "There was an error with the stock.",
        error_code: int = 500,
    ):
        super().__init__(user_message)
        self.user_message = user_message
        self.log_message = log_message
        self.error_code = error_code


class StockRepository:
    @abstractmethod
    def update_top_of_book(self, order: Order) -> None:
        
        pass
