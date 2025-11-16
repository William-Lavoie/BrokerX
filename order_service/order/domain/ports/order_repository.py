from abc import abstractmethod
from uuid import UUID

from order.domain.entities.order import Order


class OrderRepository:
    @abstractmethod
    def add_order(self, order: Order, idempotency_key: UUID) -> None:
        pass

    @abstractmethod
    def find_matching_orders(self, order: Order) -> list[Order]:
        pass

    @abstractmethod
    def get_orders_by_client(self, client_id: UUID) -> list[Order]:
        pass
