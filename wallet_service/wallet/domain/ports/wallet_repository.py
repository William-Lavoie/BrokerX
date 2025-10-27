from abc import abstractmethod
from decimal import Decimal

from ...domain.ports.dao.wallet_dao import WalletDTO


class WalletRepository:
    @abstractmethod
    def add_funds(self, email: str, amount: Decimal) -> WalletDTO:
        pass

    @abstractmethod
    def get_balance(self, email: str) -> WalletDTO:
        pass
