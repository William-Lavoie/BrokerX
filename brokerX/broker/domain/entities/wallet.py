from decimal import Decimal
from typing import Optional

from ...domain.entities.client import ClientProfile


class Wallet:
    MAX_WALLET_BALANCE = Decimal("10000.00")

    def __init__(
        self,
        balance: Decimal,
        client: Optional[ClientProfile] = None,
    ):
        self.client: ClientProfile | None = client
        self.balance: Decimal = balance

    def can_add_funds(self, amount: Decimal):
        return Decimal(self.balance) + amount <= self.MAX_WALLET_BALANCE
