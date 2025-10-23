import copy
from decimal import Decimal
from enum import Enum
from typing import Optional

from ...domain.entities.stock import Stock
from ...domain.entities.wallet import Wallet

# TODO: integrate with django user authentification class
# TODO: cronjob to delete users after 24h
# User refers strictly to django auth model


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
        wallet: Optional[Wallet] = None,
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
        self.wallet: Optional[Wallet] = wallet
        self.shares: dict[str, int] = shares

    def is_active(self) -> bool:
        return self.status == ClientStatus.ACTIVE.value

    def can_sell_shares(self, symbol: str, quantity: int) -> bool:
        return self.shares.get(symbol, 0) == quantity

    def can_buy_shares(
        self, stock: Stock, quantity: int, limit: Optional[Decimal]
    ) -> bool:
        if self.wallet is None:
            return False

        if limit is not None:
            return self.wallet.balance >= limit * quantity

        return self.wallet.balance >= stock.last_price * Decimal(quantity)
    
    def to_dict(self):
        dict = copy.copy(self.__dict__)
        dict["wallet"] = self.wallet.to_dict()
        return dict
    
