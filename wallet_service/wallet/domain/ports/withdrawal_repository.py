from abc import abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from wallet.adapters.result import Result


@dataclass
class WithdrawalDTO(Result):
    status: str = ""
    amount: Decimal = Decimal(0.0)
    created_at: datetime = field(default_factory=datetime.now)
    message: str = ""


class WithdrawalRepository:
    @abstractmethod
    def write_withdrawal(
        self,
        client_id: UUID,
        amount: Decimal,
        idempotency_key: UUID,
    ) -> WithdrawalDTO:
        pass

    @abstractmethod
    def validate_withdrawal(self, idempotency_key: UUID) -> WithdrawalDTO:
        pass

    @abstractmethod
    def fail_withdrawal(self, idempotency_key: UUID) -> WithdrawalDTO:
        pass
