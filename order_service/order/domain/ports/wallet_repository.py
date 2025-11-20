from abc import abstractmethod
from uuid import UUID

from order.domain.entities.order import Order


class WalletException(Exception):

    def __init__(
        self,
        user_message: str = "There was an error with the wallet.",
        log_message: str = "There was an error with the wallet.",
        error_code: int = 500,
    ):
        super().__init__(user_message)
        self.user_message = user_message
        self.log_message = log_message
        self.error_code = error_code


class WalletRepository:

    @abstractmethod
    def reserve_funds(self, order: Order) -> None:
        pass

    @abstractmethod
    def release_funds(self, order_id: UUID, client_id: UUID) -> None:
        pass
