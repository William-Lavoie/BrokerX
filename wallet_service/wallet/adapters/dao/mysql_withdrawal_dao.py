import logging
from decimal import Decimal
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.forms import ValidationError
from wallet.domain.ports.dao.withdrawal_dao import WithdrawalDAO
from wallet.domain.ports.withdrawal_repository import WithdrawalDTO
from wallet.models import WalletAudit, Withdrawal

logger = logging.getLogger("mysql")


class MySQLWithdrawalDAO(WithdrawalDAO):
    def write_withdrawal(
        self, client_id: UUID, amount: Decimal, idempotency_key: UUID
    ) -> WithdrawalDTO:
        try:
            with transaction.atomic():
                withdrawal, created = Withdrawal.objects.get_or_create(
                    client_id=client_id,
                    idempotency_key=idempotency_key,
                    defaults={"amount": amount},
                )
                code = 201 if created else 200

                if created:
                    WalletAudit.objects.create(
                        wallet=None,
                        withdrawal=withdrawal,
                        action="CREATE_WITHDRAWAL",
                        metadata={
                            "client_id": str(client_id),
                            "amount": str(amount),
                        },
                    )

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

    def update_status(self, idempotency_key: UUID, new_status: str) -> WithdrawalDTO:
        try:
            with transaction.atomic():
                withdrawal = Withdrawal.objects.get(idempotency_key=idempotency_key)

                withdrawal.status = new_status
                withdrawal.save()

                WalletAudit.objects.create(
                    wallet=None,
                    withdrawal=withdrawal,
                    action="UPDATE_WITHDRAWAL_STATUS",
                    metadata={
                        "client_id": str(withdrawal.client_id),
                        "new_status": new_status,
                    },
                )

                return WithdrawalDTO(success=True, code=200)

        except ObjectDoesNotExist:
            logger.error(f"There is no withdrawal with the uuid {idempotency_key}")
            return WithdrawalDTO(success=False, code=404)

        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return WithdrawalDTO(success=False, code=400)
