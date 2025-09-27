from abc import abstractmethod
from dataclasses import dataclass
from decimal import Decimal

from ....adapters.result import Result


@dataclass
class WalletDTO(Result):
    balance: Decimal = Decimal("0.0")


class WalletDAO:
    @abstractmethod
    def get_balance(self, email: str) -> WalletDTO:
        pass

    @abstractmethod
    def add_funds(self, email: str, amount: Decimal) -> WalletDTO:
        pass
