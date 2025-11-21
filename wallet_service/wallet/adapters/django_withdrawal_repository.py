from decimal import Decimal
from uuid import UUID

from wallet.adapters.dao.mysql_withdrawal_dao import MySQLWithdrawalDAO
from wallet.domain.ports.withdrawal_repository import (WithdrawalDTO,
                                                       WithdrawalRepository)


class DjangoWithdrawalRepository(WithdrawalRepository):
    def __init__(self, dao=None):
        super().__init__()
        self.dao = dao if dao is not None else MySQLWithdrawalDAO()

    def write_withdrawal(
        self, client_id: UUID, amount: Decimal, idempotency_key: UUID
    ) -> WithdrawalDTO:
        return self.dao.write_withdrawal(
            client_id=client_id, amount=amount, idempotency_key=idempotency_key
        )

    def update_status(self, idempotency_key: UUID, status: str) -> WithdrawalDTO:
        return self.dao.update_status(idempotency_key, status)
