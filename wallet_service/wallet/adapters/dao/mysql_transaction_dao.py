import logging
from decimal import Decimal
from enum import Enum
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.forms import ValidationError
from wallet.domain.ports.dao.transaction_dao import TransactionDAO
from wallet.domain.ports.transaction_repository import TransactionDTO
from wallet.models import Transaction

logger = logging.getLogger("mysql")


class Status(Enum):
    COMPLETED = "C"
    PENDING = "P"
    REJECTED = "R"
    FAILED = "F"


class MySQLTransactionDAO(TransactionDAO):
    def write_transaction(
        self, client_id: UUID, amount: Decimal, idempotency_key: UUID
    ) -> TransactionDTO:
        try:
            with transaction.atomic():
                transaction_user, created = Transaction.objects.get_or_create(
                    client_id=client_id,
                    idempotency_key=idempotency_key,
                    defaults={"amount": amount},
                )
                code = 201 if created else 200

                return TransactionDTO(
                    success=True,
                    code=code,
                    amount=transaction_user.amount,
                    status=transaction_user.status,
                    message=transaction_user.message,
                    created_at=transaction_user.created_at,
                )

        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return TransactionDTO(success=False, code=400)

    def validate_transaction(self, idempotency_key: UUID) -> TransactionDTO:
        try:
            with transaction.atomic():
                transaction_user = Transaction.objects.get(
                    idempotency_key=idempotency_key
                )

                transaction_user.status = Status.COMPLETED.value
                transaction_user.save()
                return TransactionDTO(success=True, code=200)

        except ObjectDoesNotExist:
            logger.error(f"There is no transaction with the uuid {idempotency_key}")
            return TransactionDTO(success=False, code=404)

        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return TransactionDTO(success=False, code=400)

    def fail_transaction(self, idempotency_key: UUID) -> TransactionDTO:
        try:
            with transaction.atomic():
                transaction_user = Transaction.objects.get(
                    idempotency_key=idempotency_key
                )

                transaction_user.status = Status.FAILED.value
                transaction_user.save()
                return TransactionDTO(success=True, code=200)

        except ObjectDoesNotExist:
            logger.error(f"There is no transaction with the uuid {idempotency_key}")
            return TransactionDTO(success=False, code=404)

        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return TransactionDTO(success=False, code=400)
