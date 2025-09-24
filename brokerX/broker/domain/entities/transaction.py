from decimal import Decimal
from enum import Enum
from typing import Optional
from xmlrpc.client import DateTime

from ...domain.entities.client import ClientProfile


class TransactionStatus(Enum):
    Completed = "Completed"
    PENDING = "Pending"
    REJECTED = "Rejected"
    FAILED = "Failed"


class TransactionType(Enum):
    DEPOSIT = "Deposit"


class Transaction:
    def __init__(
        self,
        amount: Decimal,
        status: TransactionStatus,
        type: TransactionType,
        message: str,
        client: Optional[ClientProfile] = None,
        created_at=None,
    ):
        self.client: Optional[ClientProfile] = client
        self.amount: Decimal = amount
        self.created_at: DateTime = created_at
        self.status: TransactionStatus = status
        self.type: TransactionType = type
        self.message: str = message
