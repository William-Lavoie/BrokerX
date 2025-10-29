from abc import abstractmethod
from decimal import Decimal
from uuid import UUID

from wallet.domain.ports.dao.wallet_dao import WalletDTO


class WalletRepository:
    @abstractmethod
    def add_funds(self, client_id: UUID, amount: Decimal) -> WalletDTO:
        pass

    @abstractmethod
    def get_balance(self, client_id: UUID) -> WalletDTO:
        pass
