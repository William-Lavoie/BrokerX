import uuid
from decimal import Decimal
from enum import Enum

from django.contrib.auth.models import User

from ...domain.ports.transaction_repository import TransactionDTO
from ...models import Transaction


class Status(Enum):
    COMPLETED = "C"
    PENDING = "P"
    REJECTED = "R"
    FAILED = "F"


class MySQLTransactionDAO:
    def write_transaction(
        self, email: str, amount: Decimal, type: str, idempotency_key: uuid.UUID
    ) -> TransactionDTO:
        print(type)
        user = User.objects.get(email=email)
        transaction, created = Transaction.objects.get_or_create(
            user=user,
            idempotency_key=idempotency_key,
            defaults={"amount": amount, "transaction_type": type},
        )
        return TransactionDTO(
            amount=transaction.amount,
            status=transaction.status,
            type=transaction.transaction_type,
            message=transaction.message,
            new=created,
            created_at=transaction.created_at,
        )

    def validate_transaction(self, idempotency_key: uuid.UUID) -> bool:
        transactions = Transaction.objects.filter(idempotency_key=idempotency_key)

        if len(transactions) != 1:
            return False

        transaction = transactions.first()
        transaction.status = Status.COMPLETED  # type: ignore
        transaction.save()  # type: ignore

        return True

    def fail_transaction(self, idempotency_key: uuid.UUID) -> bool:
        transactions = Transaction.objects.filter(idempotency_key=idempotency_key)

        if len(transactions) != 1:
            return False

        transaction = transactions.first()
        transaction.status = Status.FAILED  # type: ignore
        transaction.save()  # type: ignore

        return True
