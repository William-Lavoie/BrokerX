import uuid
from decimal import Decimal

from ..adapters.mock_payment_service_repository import (
    PaymentServiceRepository,
    PaymentServiceRepositoryResponse,
)
from ..domain.entities.transaction import Transaction, TransactionType
from ..domain.entities.wallet import Wallet
from ..domain.ports.client_repository import ClientRepository
from ..domain.ports.transaction_repository import TransactionDTO, TransactionRepository
from ..domain.ports.wallet_repository import WalletRepository


class AddFundsToWalletUseCaseResult:
    def __init__(
        self,
        success: bool,
        message: str = "",
        code: int = 0,
        new_balance: Decimal = Decimal("0.00"),
    ):
        self.success: bool = success
        self.message: str = message
        self.code: int = code
        self.new_balance: Decimal = new_balance


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

    def execute(self, email: str, amount: Decimal, idempotency_key: uuid.UUID):

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

        print(transaction.status)
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

        current_balance: Decimal = self.wallet_repository.get_balance(email)
        wallet = Wallet(balance=current_balance)

        if not wallet.can_add_funds(amount):
            return AddFundsToWalletUseCaseResult(
                success=False,
                message="You cannot have more than 10,000.00$ in your wallet.",
                code=400,
            )

        new_balance = self.wallet_repository.add_funds(email, amount)
        wallet.balance = new_balance

        if self.transaction_repository.validate_transaction(idempotency_key):
            return AddFundsToWalletUseCaseResult(
                success=True,
                message="The money has been successfully deposited into your account",
                code=200,
                new_balance=new_balance,
            )

        else:
            self.transaction_repository.fail_transaction(idempotency_key)
            return AddFundsToWalletUseCaseResult(
                success=False,
                message="There was an error while trying to process your deposit. Please try again.",
                code=500,
                new_balance=new_balance,
            )
