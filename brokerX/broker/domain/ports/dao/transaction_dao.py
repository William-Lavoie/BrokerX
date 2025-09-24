import uuid
from abc import abstractmethod
from decimal import Decimal

from ....domain.ports.transaction_repository import TransactionDTO


class TransactionDAO:
    @abstractmethod
    def write_transaction(
        self, email: str, amount: Decimal, type: str, idempotency_key: uuid.UUID
    ) -> TransactionDTO:
        pass
