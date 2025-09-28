import logging
import uuid
from decimal import Decimal
from enum import Enum

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction
from django.forms import ValidationError

from ...domain.ports.dao.transaction_dao import TransactionDAO
from ...domain.ports.transaction_repository import TransactionDTO
from ...models import Transaction

logger = logging.getLogger(__name__)


class Status(Enum):
    COMPLETED = "C"
    PENDING = "P"
    REJECTED = "R"
    FAILED = "F"


class MySQLTransactionDAO(TransactionDAO):
    def write_transaction(
        self, email: str, amount: Decimal, type: str, idempotency_key: uuid.UUID
    ) -> TransactionDTO:
        try:
            with transaction.atomic():
                user = User.objects.get(email=email)
                transaction_user, created = Transaction.objects.get_or_create(
                    user=user,
                    idempotency_key=idempotency_key,
                    defaults={"amount": amount, "transaction_type": type},
                )
                return TransactionDTO(
                    success=True,
                    code=201,
                    amount=transaction_user.amount,
                    status=transaction_user.status,
                    type=transaction_user.transaction_type,
                    message=transaction_user.message,
                    new=created,
                    created_at=transaction_user.created_at,
                )

        except ObjectDoesNotExist:
            logger.error(f"There is no user with the email {email}")
            return TransactionDTO(success=False, code=404)

        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return TransactionDTO(success=False, code=400)

    def validate_transaction(self, idempotency_key: uuid.UUID) -> TransactionDTO:
        try:
            with transaction.atomic():
                transaction_user = Transaction.objects.get(
                    idempotency_key=idempotency_key
                )

                transaction_user.status = Status.COMPLETED.value  # type: ignore
                transaction_user.save()  # type: ignore
                return TransactionDTO(success=True, code=200)

        except ObjectDoesNotExist:
            logger.error(f"There is no user with the uuid {idempotency_key}")
            return TransactionDTO(success=False, code=404)

        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return TransactionDTO(success=False, code=400)

    def fail_transaction(self, idempotency_key: uuid.UUID) -> TransactionDTO:
        try:
            with transaction.atomic():
                transaction_user = Transaction.objects.get(
                    idempotency_key=idempotency_key
                )

                transaction_user.status = Status.FAILED.value  # type: ignore
                transaction_user.save()  # type: ignore
                return TransactionDTO(success=True, code=200)

        except ObjectDoesNotExist:
            logger.error(f"There is no user with the uuid {idempotency_key}")
            return TransactionDTO(success=False, code=404)

        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return TransactionDTO(success=False, code=400)
