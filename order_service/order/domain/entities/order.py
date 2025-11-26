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
    order_style: str = ""
    order_duration: str = ""
    quantity: int = 0
    quantity_executed: int = 0
    price: Optional[Decimal] = Decimal("0.00")
    end_date: Optional[datetime] = None
    status: str = "PENDING"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
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

    def get_order_from_dto(self) -> "Order":
        order = Order(
            order_id=self.order_id,
            client_id=self.client_id,
            symbol=self.symbol,
            order_type=self.order_type,
            order_style=self.order_style,
            order_duration=self.order_duration,
            quantity=self.quantity,
            quantity_executed=self.quantity_executed,
            price=self.price,
            end_date=self.end_date,
            status=self.status,
            created_at=self.created_at,
            updated_at=self.updated_at,
            executed_at=self.executed_at,
        )
        return order


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
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
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

    def validate_data(self) -> None:
        if self.quantity < 1:
            raise OrderInvalidException(
                user_message="The order quantity must be at least 1.",
                log_message=f"Order quantity {self.quantity} is invalid.",
                error_code=400,
            )

        if self.order_type not in ["BUY", "SELL"]:
            raise OrderInvalidException(
                user_message="The order type is invalid.",
                log_message=f"Order type {self.order_type} is invalid.",
                error_code=400,
            )

        if self.order_style not in ["MARKET", "LIMIT"]:
            raise OrderInvalidException(
                user_message="The order style is invalid.",
                log_message=f"Order style {self.order_style} is invalid.",
                error_code=400,
            )

        if self.order_duration not in ["DAY", "GTC", "GTD", "IOC", "FOK"]:
            raise OrderInvalidException(
                user_message="The order duration is invalid.",
                log_message=f"Order duration {self.order_duration} is invalid.",
                error_code=400,
            )

        if self.order_style == "LIMIT":
            if self.price is None or self.price <= Decimal("0.00"):
                raise OrderInvalidException(
                    user_message="The limit order must have a valid price.",
                    log_message=f"Limit order has invalid price {self.price}.",
                    error_code=400,
                )

        if self.quantity_executed > self.quantity:
            raise OrderInvalidException(
                user_message="The executed quantity cannot exceed the order quantity.",
                log_message=f"Executed quantity {self.quantity_executed} exceeds order quantity {self.quantity}.",
                error_code=400,
            )

        if self.order_duration == "GTD":
            if self.end_date is None:
                raise OrderInvalidException(
                    user_message="The GTD order must have an end date.",
                    log_message="GTD order missing end date.",
                    error_code=400,
                )

            if self.end_date <= datetime.now().date():
                raise OrderInvalidException(
                    user_message="The end date must be in the future.",
                    log_message="The GTD order must have an end date later than the current date.",
                    error_code=400,
                )

        if self.order_duration != "GTD":
            if self.end_date is not None:
                raise OrderInvalidException(
                    user_message="Only GTD orders can have an end date.",
                    log_message="Non-GTD order has an end date specified.",
                    error_code=400,
                )

    def to_dict(self):
        return {
            "order_id": str(self.order_id) if self.order_id else None,
            "client_id": str(self.client_id),
            "symbol": self.symbol,
            "order_type": self.order_type,
            "order_style": self.order_style,
            "order_duration": self.order_duration,
            "quantity": self.quantity,
            "quantity_executed": self.quantity_executed,
            "price": float(self.price) if self.price is not None else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "executed_at": self.executed_at.isoformat() if self.executed_at else None,
        }

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
            client_id=UUID(data["client_id"]),
            symbol=data["symbol"],
            order_type=data["order_type"],
            order_style=data["order_style"],
            order_duration=data["order_duration"],
            quantity=data["quantity"],
            order_id=UUID(data["order_id"]) if data.get("order_id") else None,
            quantity_executed=data.get("quantity_executed", 0),
            price=Decimal(data["price"]) if data.get("price") is not None else None,
            end_date=(
                datetime.fromisoformat(data["end_date"])
                if data.get("end_date")
                else None
            ),
            status=data.get("status", "NOT_PROCESSED"),
            created_at=(
                datetime.fromisoformat(data["created_at"])
                if data.get("created_at")
                else None
            ),
            updated_at=(
                datetime.fromisoformat(data["updated_at"])
                if data.get("updated_at")
                else None
            ),
            executed_at=(
                datetime.fromisoformat(data["executed_at"])
                if data.get("executed_at")
                else None
            ),
        )
