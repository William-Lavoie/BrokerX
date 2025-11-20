import logging
from decimal import Decimal
from uuid import UUID

from wallet.domain.ports.wallet_repository import WalletRepository

from wallet_service.use_case_results import UseCaseResult


logger = logging.getLogger("wallet")


class ReserveFundsUseCase:
    def __init__(
        self,
        wallet_repository: WalletRepository,
    ):
        self.wallet_repository = wallet_repository

    def reserve_funds(
        self, client_id: UUID, amount: Decimal, order_id: UUID
    ) -> UseCaseResult:
        try:

            amount_available: Decimal = self.wallet_repository.get_effective_balance(
                client_id=client_id
            )

            if amount_available < amount:
                return UseCaseResult(
                    success=False,
                    message="Insufficient funds.",
                    code=400,
                )

            wallet_dto = self.wallet_repository.reserve_funds(
                client_id=client_id, order_id=order_id, amount=amount
            )

            if wallet_dto.code == 201:
                return UseCaseResult(
                    success=True,
                    message="Funds reserved successfully.",
                    code=200,
                )

            elif wallet_dto.code == 409:
                return UseCaseResult(
                    success=True,
                    message=f"Funds have already been reserved by client {client_id} for the order {order_id}.",
                    code=409,
                )

        except Exception as e:
            logger.error(f"Error reserving funds: {e}")
            return UseCaseResult(
                success=False,
                message="Error reserving funds.",
                code=500,
            )


    def release_funds(
        self, client_id: UUID, order_id: UUID
    ) -> UseCaseResult:
        try:

            if self.wallet_repository.release_funds(client_id=client_id, order_id=order_id):
                return UseCaseResult(
                    success=True,
                    message="Funds released successfully.",
                    code=200,
                )                         
            
            return UseCaseResult(
                    success=False,
                    message="Funds could not be released.",
                    code=500,
                )
                
        except Exception as e:
            logger.error(f"Error reserving funds: {e}")
            return UseCaseResult(
                success=False,
                message="Error reserving funds.",
                code=500,
            )
