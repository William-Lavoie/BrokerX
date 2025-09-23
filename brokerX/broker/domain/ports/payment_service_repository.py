from abc import abstractmethod
from decimal import Decimal


class PaymentServiceRepositoryResponse:
    def __init__(self, success: bool, message: str = None):
        self.success = success
        self.message = message


class PaymentServiceRepository:
    @abstractmethod
    def withdraw_funds(
        self, email: str, amount: Decimal
    ) -> PaymentServiceRepositoryResponse:
        pass
