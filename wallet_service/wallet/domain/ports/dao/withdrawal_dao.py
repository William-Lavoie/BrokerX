from abc import abstractmethod
from decimal import Decimal
from uuid import UUID

from wallet.domain.ports.withdrawal_repository import WithdrawalDTO


class WithdrawalDAO:
    @abstractmethod
    def write_withdrawal(
        self, client_id: UUID, amount: Decimal, idempotency_key: UUID
    ) -> WithdrawalDTO:
        pass

    @abstractmethod
    def update_status(self, idempotency_key: UUID, new_status: str) -> WithdrawalDTO:
        pass
