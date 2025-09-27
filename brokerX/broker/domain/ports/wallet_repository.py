from abc import abstractmethod
from decimal import Decimal


class WalletRepository:
    @abstractmethod
    def add_funds(self, email: str, amount: Decimal) -> Decimal:
        pass

    @abstractmethod
    def get_balance(self, email: str) -> Decimal:
        pass
