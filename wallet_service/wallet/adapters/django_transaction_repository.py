from decimal import Decimal
from uuid import UUID

from wallet.adapters.dao.mysql_transaction_dao import MySQLTransactionDAO
from wallet.domain.ports.transaction_repository import (
    TransactionDTO,
    TransactionRepository,
)


class DjangoTransactionRepository(TransactionRepository):
    def __init__(self, dao=None):
        super().__init__()
        self.dao = dao if dao is not None else MySQLTransactionDAO()

    def write_transaction(
        self, client_id: UUID, amount: Decimal, idempotency_key: UUID
    ) -> TransactionDTO:
        return self.dao.write_transaction(
            client_id=client_id, amount=amount, idempotency_key=idempotency_key
        )

    def validate_transaction(self, idempotency_key: UUID) -> TransactionDTO:
        return self.dao.validate_transaction(idempotency_key)

    def fail_transaction(self, idempotency_key: UUID) -> TransactionDTO:
        return self.dao.fail_transaction(idempotency_key)
