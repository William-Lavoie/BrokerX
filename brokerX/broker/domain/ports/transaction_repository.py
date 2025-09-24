import uuid
from abc import abstractmethod
from decimal import Decimal
from xmlrpc.client import DateTime


class TransactionDTO:
    def __init__(
        self,
        amount: Decimal,
        status: str,
        type: str,
        message: str,
        new: bool,
        created_at=None,
    ):
        self.amount: Decimal = amount
        self.created_at: DateTime = created_at
        self.status: str = status
        self.type: str = type
        self.message: str = message
        self.new: bool = new


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
