import copy
import logging
from decimal import Decimal
from enum import Enum
from typing import Optional

from ...domain.entities.stock import Stock

# TODO: integrate with django user authentification class
# TODO: cronjob to delete users after 24h
# User refers strictly to django auth model
logger = logging.getLogger(__name__)


class ClientInvalidException(Exception):
    def __init__(
        self,
        user_message: str = "Your account has been deactivated or could not be found.",
        log_message: str = "Client instance was not found",
        error_code: int = 400,
    ):
        super().__init__(user_message)
        self.user_message = user_message
        self.log_message = log_message
        self.error_code = error_code


class ClientStatus(Enum):
    ACTIVE = "Active"
    PENDING = "Pending"
    REJECTED = "Rejected"


class Client:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        address: str,
        birth_date: str,
        email: str,
        phone_number: str,
        status: str,
        password: str = "",
        shares: dict[str, int] = {},
    ):
        self.first_name: str = first_name
        self.last_name = last_name
        self.address: str = address
        self.birth_date: str = birth_date
        self.email: str = email
        self.phone_number: str = phone_number
        self.status: str = status
        self.password: str = password
        self.shares: dict[str, int] = shares

    def is_active(self) -> bool:
        return self.status == ClientStatus.ACTIVE.value

    def can_sell_shares(self, symbol: str, quantity: int) -> bool:
        return self.shares.get(symbol, 0) == quantity

    def can_buy_shares(
        self, stock: Stock, quantity: int, limit: Optional[Decimal], balance: Decimal
    ) -> bool:
        if balance is None:
            return False

        if limit is not None:
            return balance >= limit * quantity

        return balance >= stock.last_price * Decimal(quantity)

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address,
            "birth_date": self.birth_date,
            "email": self.email,
            "phone_number": self.phone_number,
            "status": self.status,
            "password": self.password,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            first_name=data["first_name"],
            last_name=data["last_name"],
            address=data["address"],
            birth_date=data["birth_date"],
            email=data["email"],
            phone_number=data["phone_number"],
            status=data.get("status", ""),
            password=data.get("password", ""),
            shares=data.get("shares", {}),
        )
