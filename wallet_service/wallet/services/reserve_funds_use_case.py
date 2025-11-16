import logging
from decimal import Decimal
from uuid import UUID

from wallet.domain.ports.dao.wallet_dao import WalletDTO
from wallet.domain.ports.wallet_repository import WalletRepository

from wallet_service.use_case_results import UseCaseResult


logger = logging.getLogger("wallet")


class ReserveFundsUseCaseResult:
    def __init__(
        self,
        wallet_repository: WalletRepository,
        transaction_repository: TransactionRepository,
    ):
        self.wallet_repository = wallet_repository
        self.transaction_repository = transaction_repository

    def execute(
        self, client_id: UUID, amount: Decimal, order_id: UUID
    ) -> UseCaseResult:
        try:

            wallet_dto: WalletDTO = self.wallet_repository.get_balance(
                client_id=client_id
            )

            if wallet_dto.balance < amount:
                return UseCaseResult(
                    success=False,
                    message="Insufficient funds.",
                    code=400,
                )

            # Deduct the reserved amount from the wallet balance
            new_balance = wallet_dto.balance - amount
            self.wallet_repository.update_wallet_balance(
                client_id=client_id, new_balance=new_balance
            )

            # Record the reservation transaction
            transaction_dto: TransactionDTO = (
                self.transaction_repository.write_transaction(
                    client_id=client_id,
                    amount=-amount,
                    idempotency_key=order_id,
                )
            )

            return UseCaseResult(
                success=True,
                message="Funds reserved successfully.",
                code=200,
            )
        except Exception as e:
            logger.error(f"Error reserving funds: {e}")
            return UseCaseResult(
                success=False,
                message="Error reserving funds.",
                code=500,
            )
