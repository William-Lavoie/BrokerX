from decimal import Decimal
from enum import Enum
from xmlrpc.client import DateTime


class TransactionStatus(Enum):
    COMPLETED = "C"
    PENDING = "P"
    REJECTED = "R"
    FAILED = "F"


class TransactionType(Enum):
    DEPOSIT = "Deposit"


class Transaction:
    def __init__(
        self,
        amount: Decimal,
        status: str,
        message: str,
        created_at=None,
    ):
        self.amount: Decimal = amount
        self.created_at: DateTime = created_at
        self.status: str = status
        self.message: str = message

    def has_been_processed(self) -> bool:
        return self.status != TransactionStatus.PENDING.value
