from abc import abstractmethod
from decimal import Decimal
from uuid import UUID

from wallet.domain.ports.transaction_repository import TransactionDTO


class TransactionDAO:
    @abstractmethod
    def write_transaction(
        self, client_id: UUID, amount: Decimal, idempotency_key: UUID
    ) -> TransactionDTO:
        pass

    @abstractmethod
    def validate_transaction(self, idempotency_key: UUID) -> TransactionDTO:
        pass

    @abstractmethod
    def fail_transaction(self, idempotency_key: UUID) -> TransactionDTO:
        pass
