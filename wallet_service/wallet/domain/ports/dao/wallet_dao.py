from abc import abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from wallet.adapters.result import Result


@dataclass
class WalletDTO(Result):
    balance: Decimal = Decimal("0.0")


class WalletDAO:
    @abstractmethod
    def get_balance(self, client_id: UUID) -> WalletDTO:
        pass

    @abstractmethod
    def add_funds(self, client_id: UUID, amount: Decimal) -> WalletDTO:
        pass

    @abstractmethod
    def get_reserved_funds(self, client_id: UUID) -> Decimal:
        pass

    @abstractmethod
    def reserve_funds(
        self, client_id: UUID, amount: Decimal, order_id: UUID
    ) -> WalletDTO:
        pass

    @abstractmethod
    def release_funds(self, client_id: UUID, order_id: UUID) -> WalletDTO:
        pass

    @abstractmethod
    def process_payments(self, orders_info: list[dict]) -> WalletDTO:
        pass

    @abstractmethod
    def process_transfers(self, orders_info: list[dict]) -> WalletDTO:
        pass
