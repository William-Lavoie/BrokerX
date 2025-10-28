import datetime
from abc import abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID

from order.adapters.result import Result
from order.domain.entities.order import Order


@dataclass
class OrderDTO(Result):
    direction: str = ""
    limit: Optional[Decimal] = Decimal("0.00")
    initial_quantity: int = 0
    remaining_quantity: int = 0
    order_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime


class OrderRepository:
    @abstractmethod
    def add_order(
        self,
        client_id: UUID,
        direction: str,
        symbol: str,
        initial_quantity: int,
        idempotency_key: UUID,
        limit: Optional[Decimal] = None,
    ) -> Order:
        pass

    @abstractmethod
    def find_matching_orders(order: Order) -> list[Order]:
        pass

    @abstractmethod
    def get_orders_by_client(client_id: UUID) -> list[Order]:
        pass

    @classmethod
    def get_order_from_dto(cls, dto: OrderDTO) -> Order:
        return Order(
            direction=dto.direction,
            limit=dto.limit,
            initial_quantity=dto.initial_quantity,
            remaining_quantity=dto.remaining_quantity,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )
