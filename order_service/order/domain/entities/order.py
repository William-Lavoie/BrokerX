import copy
from dataclasses import asdict, dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from order.adapters.result import Result


@dataclass
class OrderDTO(Result):
    order_id: Optional[UUID] = None
    client_id: Optional[UUID] = None
    symbol: str = ""
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


class OrderInvalidException(Exception):
    def __init__(
        self,
        user_message: str = "The order could not be placed.",
        log_message: str = "The order was invalid.",
        error_code: int = 400,
    ):
        super().__init__(user_message)
        self.user_message = user_message
        self.log_message = log_message
        self.error_code = error_code


@dataclass
class Order:

    def __init__(
        self,
        client_id: UUID,
        symbol: str,
        order_type: str,
        order_style: str,
        order_duration: str,
        quantity: int,
        order_id: Optional[UUID] = None,
        quantity_executed: int = 0,
        price: Optional[Decimal] = None,
        end_date: Optional[datetime] = None,
        status: str = "NOT_PROCESSED",
        created_at: datetime = None,
        updated_at: datetime = None,
        executed_at: Optional[datetime] = None,
    ):

        self.order_id = order_id
        self.client_id = client_id
        self.symbol = symbol
        self.order_type = order_type
        self.order_style = order_style
        self.order_duration = order_duration
        self.quantity = quantity
        self.quantity_executed = quantity_executed
        self.price = price
        self.end_date = end_date
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.executed_at = executed_at

    def price_is_acceptable(
        self, offered_price: Decimal, market_price: Decimal
    ) -> bool:
        return self.limit is None and offered_price == market_price

    def to_dict(self):
        return copy.copy(self.__dict__)

    def update_from_dto(self, order_dto: OrderDTO) -> None:
        self.order_id = order_dto.order_id
        self.client_id = order_dto.client_id
        self.symbol = order_dto.symbol
        self.order_type = order_dto.order_type
        self.order_style = order_dto.order_style
        self.order_duration = order_dto.order_duration
        self.quantity = order_dto.quantity
        self.quantity_executed = order_dto.quantity_executed
        self.price = order_dto.price
        self.end_date = order_dto.end_date
        self.status = order_dto.status
        self.created_at = order_dto.created_at
        self.updated_at = order_dto.updated_at
        self.executed_at = order_dto.executed_at

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            symbol=data.get("symbol"),
            client_id=data.get("client_id"),
            direction=data.get("direction", ""),
            initial_quantity=data.get("initial_quantity", 0),
            remaining_quantity=data.get("remaining_quantity", 0),
            order_id=data.get("order_id", ""),
            created_at=data.get("created_at", ""),
            updated_at=data.get("created_at"),
        )
