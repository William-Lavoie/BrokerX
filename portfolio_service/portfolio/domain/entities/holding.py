from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID


class HoldingInvalidException(Exception):

    def __init__(
        self,
        user_message: str = "The holding is invalid.",
        log_message: str = "The holding is invalid.",
        error_code: int = 400,
    ):
        super().__init__(user_message)
        self.user_message = user_message
        self.log_message = log_message
        self.error_code = error_code


@dataclass
class Holding:

    def __init__(
        self,
        client_id: UUID,
        symbol: str = "",
        name: str = "",
        quantity: int = 0,
        buying_price: Optional[Decimal] = None,
        current_price: Optional[Decimal] = None,
        performance: Optional[Decimal] = None,
    ):
        self.client_id = client_id
        self.symbol = symbol
        self.name = name
        self.quantity = quantity
        self.buying_price = buying_price
        self.current_price = current_price
        self.performance = performance


    def to_dict(self):
        return {
            "client_id": str(self.client_id),
            "symbol": self.symbol,
            "name": self.name,
            "quantity": self.quantity,
            "buying_price": Decimal(self.buying_price) if self.buying_price is not None else None,
            "current_price": Decimal(self.current_price) if self.current_price is not None else None,
            "performance": Decimal(self.performance) if self.performance is not None else None,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            client_id=UUID(data["client_id"]),
            symbol=data["symbol"],
            name=data["name"],
            quantity=data["quantity"],
            buying_price=Decimal(data["buying_price"]) if data.get("buying_price") is not None else None,
            current_price=Decimal(data["current_price"]) if data.get("current_price") is not None else None,
            performance=Decimal(data["performance"]) if data.get("performance") is not None else None,
        )
