from abc import abstractmethod
from decimal import Decimal

from ...models import Wallet


class WalletRepository:
    @abstractmethod
    def add_funds(self, email: str, amount: Decimal) -> Decimal:
        pass

    @abstractmethod
    def get_wallet(self, email: str) -> Wallet:
        pass
