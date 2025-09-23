from enum import Enum
from xmlrpc.client import DateTime

from ...domain.entities.client import ClientProfile


class Transaction:
    def __init__(self, client, amount, status, type, created_at=None):
        self.client: ClientProfile = client
        self.amount: float = amount
        self.created_at: DateTime = created_at
        self.status: TransactionStatus = status
        self.type: TransactionType = type


class TransactionStatus(Enum):
    Completed = "Completed"
    PENDING = "Pending"
    REJECTED = "Rejected"
    FAILED = "Failed"


class TransactionType(Enum):
    DEPOSIT = "Deposit"
