from abc import abstractmethod
from decimal import Decimal
from typing import Optional
from uuid import UUID

from ....domain.ports.order_repository import OrderDTO


class OrderDAO:
    @abstractmethod
    def add_order(
        self,
        email: str,
        symbol: str,
        direction: str,
        initial_quantity: int,
        idempotency_key: UUID,
        limit: Optional[Decimal],
    ) -> OrderDTO:
        pass

    @abstractmethod
    def find_matching_orders(self, email: str, symbol: str, direction: str, quantity: int) -> list[OrderDTO]:
        pass

    @abstractmethod
    def get_orders_by_client(self, email: str) -> list[OrderDTO]:
        pass
