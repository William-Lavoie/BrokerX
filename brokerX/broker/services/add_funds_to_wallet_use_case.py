import logging
import uuid
from decimal import Decimal

from ..adapters.mock_payment_service_repository import (
    PaymentServiceRepository,
    PaymentServiceRepositoryResponse,
)
from ..domain.entities.transaction import Transaction, TransactionType
from ..domain.entities.wallet import Wallet
from ..domain.ports.client_repository import ClientRepository
from ..domain.ports.dao.wallet_dao import WalletDTO
from ..domain.ports.transaction_repository import TransactionDTO, TransactionRepository
from ..domain.ports.wallet_repository import WalletRepository
from ..services.use_case_result import UseCaseResult

logger = logging.getLogger(__name__)


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
        client_repository: ClientRepository,
        payment_service_repository: PaymentServiceRepository,
        wallet_repository: WalletRepository,
        transaction_repository: TransactionRepository,
    ):
        self.client_repository = client_repository
        self.payment_service_repository = payment_service_repository
        self.wallet_repository = wallet_repository
        self.transaction_repository = transaction_repository

    def execute(
        self, email: str, amount: Decimal, idempotency_key: uuid.UUID
    ) -> AddFundsToWalletUseCaseResult:

        if not self.client_repository.client_is_active(email):
            return AddFundsToWalletUseCaseResult(
                success=False,
                message="Your account must be active to add funds to your wallet. The deposit was not processed.",
                code=403,
            )

        transaction_dto: TransactionDTO = self.transaction_repository.write_transaction(
            email=email,
            amount=amount,
            type=str(TransactionType.DEPOSIT.value),
            idempotency_key=idempotency_key,
        )

        transaction = Transaction(
            amount=transaction_dto.amount,
            created_at=transaction_dto.created_at,
            status=transaction_dto.status,
            type=transaction_dto.type,
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

        wallet_dto: WalletDTO = self.wallet_repository.get_balance(email)
        logger.error(wallet_dto)
        wallet = Wallet(balance=wallet_dto.balance)

        if not wallet.can_add_funds(amount):
            return AddFundsToWalletUseCaseResult(
                success=False,
                message="You cannot have more than 10,000.00$ in your wallet.",
                code=400,
            )

        result_wallet: WalletDTO = self.wallet_repository.add_funds(email, amount)
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

    def get_balance(self, email: str) -> AddFundsToWalletUseCaseResult:
        result = self.wallet_repository.get_balance(email)

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
