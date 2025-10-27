from abc import abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from wallet.adapters.result import Result


@dataclass
class TransactionDTO(Result):
    status: str = ""
    amount: Decimal = Decimal(0.0)
    created_at: datetime = field(default_factory=datetime.now)
    message: str = ""


class TransactionRepository:
    @abstractmethod
    def write_transaction(
        self,
        client_id: UUID,
        amount: Decimal,
        idempotency_key: UUID,
    ) -> TransactionDTO:
        """By default a transaction is set to pending"""
        pass

    @abstractmethod
    def validate_transaction(self, idempotency_key: UUID) -> TransactionDTO:
        pass

    @abstractmethod
    def fail_transaction(self, idempotency_key: UUID) -> TransactionDTO:
        pass
