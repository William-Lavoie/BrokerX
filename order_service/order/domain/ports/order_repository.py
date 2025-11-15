from abc import abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from order.adapters.result import Result
from order.domain.entities.order import Order


@dataclass
class OrderDTO(Result):
    order_id: Optional[UUID] = None
    client_id: Optional[UUID] = None
    stock_symbol: str = ""
    order_type: str = ""
    order_style: str = ("",)
    order_duration: str = ""
    quantity: int = 0
    quantity_executed: int = 0
    price: Optional[Decimal] = Decimal("0.00")
    end_date: Optional[datetime] = None
    status: str = "PENDING"
    created_at: datetime = None
    updated_at: datetime = None
    executed_at: Optional[datetime] = None

    def to_dict(self):
        data = asdict(self)
        if self.client_id:
            if self.order_id:
                data["order_id"] = str(self.order_id)
            if self.client_id:
                data["client_id"] = str(self.client_id)
            if self.created_at:
                data["created_at"] = self.created_at.isoformat()
            if self.updated_at:
                data["updated_at"] = self.updated_at.isoformat()
            if self.executed_at:
                data["executed_at"] = self.executed_at.isoformat()
            if self.price is not None:
                data["price"] = str(self.price)
            if self.end_date:
                data["end_date"] = self.end_date.isoformat()
        return data


class OrderRepository:
    @abstractmethod
    def add_order(
        self,
        client_id: UUID,
        symbol: str,
        order_type: str,
        order_style: str,
        order_duration: str,
        quantity: int,
        idempotency_key: UUID,
        price: Optional[Decimal] = None,
        end_date: Optional[datetime] = None,
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
            order_id=dto.order_id,
            client_id=dto.client_id,
            stock_symbol=dto.stock_symbol,
            order_type=dto.order_type,
            order_style=dto.order_style,
            order_duration=dto.order_duration,
            quantity=dto.quantity,
            quantity_executed=dto.quantity_executed,
            price=dto.price,
            end_date=dto.end_date,
            status=dto.status,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            executed_at=dto.executed_at,
        )
