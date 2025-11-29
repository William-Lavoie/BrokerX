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

    @abstractmethod
    def get_effective_balance(self, client_id: UUID) -> Decimal:
        pass

    @abstractmethod
    def reserve_funds(self, client_id: UUID, amount: Decimal, order_id: UUID) -> bool:
        pass

    @abstractmethod
    def release_funds(self, client_id: UUID, order_id: UUID) -> bool:
        pass

    @abstractmethod
    def process_payments(self, orders_info: list[dict]) -> None:
        pass

    @abstractmethod
    def process_transfers(self, orders_info: list[dict]) -> None:
        pass
