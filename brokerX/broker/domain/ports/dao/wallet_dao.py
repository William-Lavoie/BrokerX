from abc import abstractmethod
from decimal import Decimal


class WalletDTO:
    def __init__(self, balance: Decimal):
        self.balance = balance


class WalletDAO:
    @abstractmethod
    def get_wallet(self, email: str) -> WalletDTO:
        pass

    @abstractmethod
    def add_funds(self, email: str, amount: Decimal) -> Decimal:
        pass
