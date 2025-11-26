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

    @abstractmethod
    def delete_order(self, client_id: UUID, order_id: UUID) -> Order:
        pass

    @abstractmethod
    def delete_order_rollback(
        self, client_id: UUID, order_id: UUID, previous_status: str
    ) -> None:
        pass

    @abstractmethod
    def get_potential_matches(self, order: Order) -> list[Order]:
        pass

    @abstractmethod
    def execute_order(self, order: Order, matching_orders: list[Order]) -> dict:
        pass
