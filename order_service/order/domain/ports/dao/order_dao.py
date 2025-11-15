from abc import abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from order.domain.entities.order import OrderDTO


class OrderDAO:
    @abstractmethod
    def add_order(
        self,
        client_id: UUID,
        symbol: str,
        order_type: str,
        order_style: str,
        quantity: int,
        idempotency_key: UUID,
        end_date: Optional[datetime],
        price: Optional[Decimal] = None,
    ) -> OrderDTO:
        pass

    @abstractmethod
    def find_matching_orders(
        self, email: str, symbol: str, direction: str, quantity: int
    ) -> list[OrderDTO]:
        pass

    @abstractmethod
    def get_orders_by_client(self, email: str) -> list[OrderDTO]:
        pass
