import logging
from decimal import Decimal
from uuid import UUID

from wallet.domain.entities.transaction import Transaction
from wallet.domain.entities.wallet import Wallet
from wallet.domain.ports.dao.wallet_dao import WalletDTO
from wallet.domain.ports.transaction_repository import (
    TransactionDTO,
    TransactionRepository,
)
from wallet.domain.ports.wallet_repository import WalletRepository

from wallet_service.use_case_results import UseCaseResult

from ..adapters.mock_payment_service_repository import (
    PaymentServiceRepository,
    PaymentServiceRepositoryResponse,
)

logger = logging.getLogger("wallet")


class AddFundsToWalletUseCaseResult(UseCaseResult):
    def __init__(
        self,
        success: bool,
        message: str,
        code: int,
        balance: Decimal = Decimal("0.00"),
    ):
        super().__init__(success=success, message=message, code=code)
        self.balance: Decimal = balance

    def to_dict(self):
        dict = super().to_dict()
        dict["balance"] = self.balance
        return dict


class AddFundsToWalletUseCase:
    def __init__(
        self,
        payment_service_repository: PaymentServiceRepository,
        wallet_repository: WalletRepository,
        transaction_repository: TransactionRepository,
    ):
        self.payment_service_repository = payment_service_repository
        self.wallet_repository = wallet_repository
        self.transaction_repository = transaction_repository

    def execute(
        self, client_id: UUID, email: str, amount: Decimal, idempotency_key: UUID
    ) -> AddFundsToWalletUseCaseResult:

        transaction_dto: TransactionDTO = self.transaction_repository.write_transaction(
            client_id=client_id,
            amount=amount,
            idempotency_key=idempotency_key,
        )

        transaction = Transaction(
            amount=transaction_dto.amount,
            created_at=transaction_dto.created_at,
            status=transaction_dto.status,
            message=transaction_dto.message,
        )

        if transaction.has_been_processed():
            return AddFundsToWalletUseCaseResult(
                success=True,
                message="This transaction has already been processed",
                code=200,
            )

        payment_service_response: PaymentServiceRepositoryResponse = (
            self.payment_service_repository.withdraw_funds(email, amount)
        )

        if not payment_service_response.success:
            return AddFundsToWalletUseCaseResult(
                success=False,
                message="There was an error with the payment service. The deposit was not processed.",
                code=500,
            )

        wallet_dto: WalletDTO = self.wallet_repository.get_balance(client_id)
        wallet = Wallet(balance=wallet_dto.balance)

        if not wallet.can_add_funds(amount):
            return AddFundsToWalletUseCaseResult(
                success=False,
                message="You cannot have more than 10,000.00$ in your wallet.",
                code=400,
            )

        result_wallet: WalletDTO = self.wallet_repository.add_funds(client_id, amount)
        if not result_wallet.success:
            return AddFundsToWalletUseCaseResult(
                success=False,
                message="There was an error adding the money into your virtual wallet.",
                code=500,
            )

        wallet.balance = result_wallet.balance

        if self.transaction_repository.validate_transaction(idempotency_key).success:
            return AddFundsToWalletUseCaseResult(
                success=True,
                message="The money has been successfully deposited into your account",
                code=200,
                balance=wallet.balance,
            )

        else:
            self.transaction_repository.fail_transaction(idempotency_key)
            return AddFundsToWalletUseCaseResult(
                success=False,
                message="There was an error while trying to process your deposit. Please try again.",
                code=500,
                balance=wallet.balance,
            )

    def get_balance(self, client_id: UUID) -> AddFundsToWalletUseCaseResult:
        result = self.wallet_repository.get_balance(client_id)

        message = (
            "There was an error trying to get your balance."
            if not result.success
            else f"Your wallet balance is {result.balance}$."
        )

        return AddFundsToWalletUseCaseResult(
            success=result.success,
            message=message,
            code=result.code,
            balance=result.balance,
        )
