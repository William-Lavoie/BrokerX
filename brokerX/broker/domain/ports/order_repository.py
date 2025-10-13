from abc import abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID

from ...adapters.result import Result
from ...domain.entities.client import ClientProfile
from ...domain.entities.order import Order
from ...domain.entities.stock import Stock


@dataclass
class OrderDTO(Result):
    stock: Optional[Stock] = None
    type: str = ""
    limit: Optional[Decimal] = Decimal("0.00")
    initial_quantity: int = 0
    remaining_quantity: int = 0


class OrderRepository:
    @abstractmethod
    def add_order(
        self,
        client: ClientProfile,
        stock: Stock,
        type: str,
        initial_quantity: int,
        idempotency_key: UUID,
        limit: Optional[Decimal] = None,
    ) -> Order:
        pass

    @classmethod
    def get_order_from_dto(cls, dto: OrderDTO) -> Order:
        return Order(
            stock=dto.stock,
            type=dto.type,
            limit=dto.limit,
            initial_quantity=dto.initial_quantity,
            remaining_quantity=dto.remaining_quantity,
        )
