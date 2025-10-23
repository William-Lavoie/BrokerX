from abc import abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID

from ...adapters.result import Result
from ...domain.entities.client import Client
from ...domain.entities.order import Order
from ...domain.entities.stock import Stock


@dataclass
class OrderDTO(Result):
    client: Optional[Client] = None
    stock: Optional[Stock] = None
    direction: str = ""
    limit: Optional[Decimal] = Decimal("0.00")
    initial_quantity: int = 0
    remaining_quantity: int = 0
    order_id: Optional[UUID] = None


class OrderRepository:
    @abstractmethod
    def add_order(
        self,
        client: Client,
        stock: Stock,
        direction: str,
        initial_quantity: int,
        idempotency_key: UUID,
        limit: Optional[Decimal] = None,
    ) -> Order:
        pass

    @abstractmethod
    def find_matching_orders(order: Order) -> list[Order]:
        pass

    @classmethod
    def get_order_from_dto(cls, dto: OrderDTO) -> Order:
        return Order(
            stock=dto.stock,
            direction=dto.direction,
            limit=dto.limit,
            initial_quantity=dto.initial_quantity,
            remaining_quantity=dto.remaining_quantity,
            client=dto.client,
        )
