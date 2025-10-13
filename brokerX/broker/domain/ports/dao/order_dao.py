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
        type: str,
        initial_quantity: int,
        idempotency_key: UUID,
        limit: Optional[Decimal],
    ) -> OrderDTO:
        pass
