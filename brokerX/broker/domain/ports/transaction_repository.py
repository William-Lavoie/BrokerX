import uuid
from abc import abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from ...adapters.result import Result


@dataclass
class TransactionDTO(Result):
    status: str = ""
    type: str = ""
    amount: Decimal = Decimal(0.0)
    created_at: datetime = field(default_factory=datetime.now)
    message: str = ""
    new: bool = False


class TransactionRepository:
    @abstractmethod
    def write_transaction(
        self,
        email: str,
        amount: Decimal,
        type: str,
        idempotency_key: uuid.UUID,
    ) -> TransactionDTO:
        """By default a transaction is set to pending"""
        pass

    @abstractmethod
    def validate_transaction(self, idempotency_key: uuid.UUID) -> TransactionDTO:
        pass

    @abstractmethod
    def fail_transaction(self, idempotency_key: uuid.UUID) -> TransactionDTO:
        pass
