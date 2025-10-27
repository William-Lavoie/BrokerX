from abc import abstractmethod
from dataclasses import dataclass
from decimal import Decimal

from ...adapters.result import Result


@dataclass
class PaymentServiceRepositoryResponse(Result):
    message: str = ""


class PaymentServiceRepository:
    @abstractmethod
    def withdraw_funds(
        self, email: str, amount: Decimal
    ) -> PaymentServiceRepositoryResponse:
        pass
