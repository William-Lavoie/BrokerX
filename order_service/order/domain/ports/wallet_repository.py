from abc import abstractmethod
from uuid import UUID

from order.domain.entities.order import Order


class WalletRepository:
    @abstractmethod
    def reserve_funds(self, order: Order) -> None:
        pass
