import logging

from wallet.adapters.django_wallet_repository import DjangoWalletRepository

from wallet_service.use_case_results import UseCaseResult

logger = logging.getLogger("wallet")


class ProcessPaymentUseCase:
    def __init__(
        self,
    ):
        self.wallet_repository = DjangoWalletRepository()

    def process_payments(self, orders_info: list[dict]) -> UseCaseResult:
        try:
            self.wallet_repository.process_payments(orders_info=orders_info)

            return UseCaseResult(
                success=True,
                message="Payment processed successfully.",
                code=200,
            )

        except Exception as e:
            logger.error(f"Error reserving funds: {e}", exc_info=True)
            return UseCaseResult(
                success=False,
                message="Error reserving funds.",
                code=500,
            )

    def process_transfers(self, orders_info: list[dict]) -> UseCaseResult:
        try:

            self.wallet_repository.process_transfers(orders_info=orders_info)

            return UseCaseResult(
                success=True,
                message="Transfer processed successfully.",
                code=200,
            )

        except Exception as e:
            logger.error(f"Error processing transfer: {e}", exc_info=True)
            return UseCaseResult(
                success=False,
                message="Error processing transfer.",
                code=500,
            )
