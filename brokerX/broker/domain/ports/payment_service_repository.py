from abc import abstractmethod
from decimal import Decimal


class PaymentServiceRepositoryResponse:
    def __init__(self, success: bool, message: str = ""):
        self.success: bool = success
        self.message: str = message


class PaymentServiceRepository:
    @abstractmethod
    def withdraw_funds(
        self, email: str, amount: Decimal
    ) -> PaymentServiceRepositoryResponse:
        pass
