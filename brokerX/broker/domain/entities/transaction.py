from decimal import Decimal
from enum import Enum
from typing import Optional
from xmlrpc.client import DateTime

from ...domain.entities.client import ClientProfile


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
        type: str,
        message: str,
        client: Optional[ClientProfile] = None,
        created_at=None,
    ):
        self.client: Optional[ClientProfile] = client
        self.amount: Decimal = amount
        self.created_at: DateTime = created_at
        self.status: str = status
        self.type: str = type
        self.message: str = message

    def has_been_processed(self) -> bool:
        return self.status != TransactionStatus.PENDING.value
