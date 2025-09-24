import uuid
from decimal import Decimal

from django.contrib.auth.models import User

from ...domain.ports.transaction_repository import TransactionDTO
from ...models import Transaction


class MySQLTransactionDAO:
    def write_transaction(
        self, email: str, amount: Decimal, type: str, idempotency_key: uuid.UUID
    ) -> TransactionDTO:
        user = User.objects.get(email=email)
        transaction, created = Transaction.objects.get_or_create(
            user=user,
            idempotency_key=idempotency_key,
            defaults={"email": email, "amount": amount, "type": type},
        )
        return TransactionDTO(
            amount=transaction.amount,
            status=transaction.status,
            type=transaction.type,
            message=transaction.type,
            new=created,
            created_at=transaction.created_at,
        )
