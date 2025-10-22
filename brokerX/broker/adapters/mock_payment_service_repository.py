import json
import logging
from decimal import Decimal

from ..domain.ports.payment_service_repository import (
    PaymentServiceRepository,
    PaymentServiceRepositoryResponse,
)
from ..external_source.mock_payment_service import MockPaymentService

logger = logging.getLogger(__name__)


class MockPaymentServiceRepository(PaymentServiceRepository):
    def __init__(self, payment_service=None):
        super().__init__()
        self.payment_service = (
            payment_service if payment_service is not None else MockPaymentService()
        )

    def withdraw_funds(
        self, email: str, amount: Decimal
    ) -> PaymentServiceRepositoryResponse:
        try:
            response = self.payment_service.withdraw_funds(email, amount)
            response = json.loads(response)

            if not response.get("success"):
                logger.error(response)

            return PaymentServiceRepositoryResponse(
                success=response.get("success", False),
                code=response.get("code", 0),
                message=response.get("message", ""),
            )

        except Exception as error:
            logger.error(f"An unexpected error occured: {error}")
            return PaymentServiceRepositoryResponse(
                success=False, code=500, message=str(error)
            )
