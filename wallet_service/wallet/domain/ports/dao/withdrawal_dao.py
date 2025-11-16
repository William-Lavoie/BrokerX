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
    def validate_withdrawal(self, idempotency_key: UUID) -> WithdrawalDTO:
        pass

    @abstractmethod
    def fail_withdrawal(self, idempotency_key: UUID) -> WithdrawalDTO:
        pass
