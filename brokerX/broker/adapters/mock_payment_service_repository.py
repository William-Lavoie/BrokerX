from decimal import Decimal
import json
from ..external_source.mock_payment_service import MockPaymentService
from ..domain.ports.payment_service_repository import (
    PaymentServiceRepository,
    PaymentServiceRepositoryResponse,
)
from ..domain.entities.client import ClientProfile


class MockPaymentServiceRepository(PaymentServiceRepository):
    def __init__(self):
        super().__init__()
        self.payment_service = MockPaymentService()

    def withdraw_funds(
        self, email: str, amount: Decimal
    ) -> PaymentServiceRepositoryResponse:
        response = self.payment_service.withdraw_funds(email, amount)
        response = json.loads(response)

        return PaymentServiceRepositoryResponse(
            success=response.get("success", False), message=response.get("message", "")
        )
