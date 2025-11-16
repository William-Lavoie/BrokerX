import logging
from decimal import Decimal
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.forms import ValidationError
from wallet.domain.ports.dao.withdrawal_dao import WithdrawalDAO
from wallet.domain.ports.withdrawal_repository import WithdrawalDTO
from wallet.models import Withdrawal

logger = logging.getLogger("mysql")


class MySQLWithdrawalDAO(WithdrawalDAO):
    def write_withdrawal(
        self, client_id: UUID, amount: Decimal, idempotency_key: UUID
    ) -> WithdrawalDAO:
        try:
            with transaction.atomic():
                withdrawal, created = Withdrawal.objects.get_or_create(
                    client_id=client_id,
                    idempotency_key=idempotency_key,
                    defaults={"amount": amount},
                )
                code = 201 if created else 200

                return WithdrawalDTO(
                    success=True,
                    code=code,
                    amount=withdrawal.amount,
                    status=withdrawal.status,
                    message=withdrawal.message,
                    created_at=withdrawal.created_at,
                )

        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return WithdrawalDTO(success=False, code=400)

    def validate_withdrawal(self, idempotency_key: UUID) -> WithdrawalDTO:
        try:
            with transaction.atomic():
                withdrawal = Withdrawal.objects.get(idempotency_key=idempotency_key)

                withdrawal.status = "COMPLETED"
                withdrawal.save()
                return WithdrawalDTO(success=True, code=200)

        except ObjectDoesNotExist:
            logger.error(f"There is no withdrawal with the uuid {idempotency_key}")
            return WithdrawalDTO(success=False, code=404)

        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return WithdrawalDTO(success=False, code=400)

    def fail_withdrawal(self, idempotency_key: UUID) -> WithdrawalDTO:
        try:
            with transaction.atomic():
                withdrawal = Withdrawal.objects.get(idempotency_key=idempotency_key)

                withdrawal.status = "FAILED"
                withdrawal.save()
                return WithdrawalDTO(success=True, code=200)

        except ObjectDoesNotExist:
            logger.error(f"There is no withdrawal with the uuid {idempotency_key}")
            return WithdrawalDTO(success=False, code=404)

        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return WithdrawalDTO(success=False, code=400)
