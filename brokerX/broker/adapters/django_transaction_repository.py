import uuid
from decimal import Decimal

from ..adapters.dao.mysql_transaction_dao import MySQLTransactionDAO
from ..domain.ports.transaction_repository import TransactionDTO, TransactionRepository


class DjangoTransactionRepository(TransactionRepository):
    def __init__(self, dao=None):
        super().__init__()
        self.dao = dao if dao is not None else MySQLTransactionDAO()

    def write_transaction(
        self, email: str, amount: Decimal, type: str, idempotency_key: uuid.UUID
    ) -> TransactionDTO:
        return self.dao.write_transaction(
            email=email, amount=amount, idempotency_key=idempotency_key, type=type
        )

    def validate_transaction(self, idempotency_key: uuid.UUID) -> bool:
        return self.dao.validate_transaction(idempotency_key)

    def fail_transaction(self, idempotency_key: uuid.UUID) -> bool:
        return self.dao.fail_transaction(idempotency_key)
