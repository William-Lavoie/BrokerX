import logging
from decimal import Decimal
from uuid import UUID

from django.db import transaction
from wallet.adapters.mock_payment_service_repository import (
    PaymentServiceRepository,
    PaymentServiceRepositoryResponse,
)
from wallet.domain.entities.wallet import Wallet
from wallet.domain.entities.withdrawal import Withdrawal
from wallet.domain.ports.dao.wallet_dao import WalletDTO
from wallet.domain.ports.wallet_repository import WalletRepository
from wallet.domain.ports.withdrawal_repository import WithdrawalRepository

from wallet_service.use_case_results import UseCaseResult

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
        withdrawal_repository: WithdrawalRepository,
    ):
        self.payment_service_repository = payment_service_repository
        self.wallet_repository = wallet_repository
        self.withdrawal_repository = withdrawal_repository

    def execute(
        self, client_id: UUID, email: str, amount: Decimal, idempotency_key: UUID
    ) -> AddFundsToWalletUseCaseResult:

        withdrawal_dto = self.withdrawal_repository.write_withdrawal(
            client_id=client_id,
            amount=amount,
            idempotency_key=idempotency_key,
        )

        if withdrawal_dto.code == 200:
            return AddFundsToWalletUseCaseResult(
                success=True,
                message="This withdrawal has already been processed",
                code=200,
            )

        withdrawal = Withdrawal(
            amount=withdrawal_dto.amount,
            created_at=withdrawal_dto.created_at,
            status=withdrawal_dto.status,
            message=withdrawal_dto.message,
        )

        payment_service_response: PaymentServiceRepositoryResponse = (
            self.payment_service_repository.withdraw_funds(email, amount)
        )

        if not payment_service_response.success:
            self.withdrawal_repository.update_status(idempotency_key, "FAILED")
            return AddFundsToWalletUseCaseResult(
                success=False,
                message="There was an error with the payment service. The deposit was not processed.",
                code=500,
            )

        wallet_dto: WalletDTO = self.wallet_repository.get_balance(client_id)
        wallet = Wallet(balance=wallet_dto.balance)

        if not wallet.can_add_funds(amount):
            self.withdrawal_repository.update_status(idempotency_key, "REJECTED")
            return AddFundsToWalletUseCaseResult(
                success=False,
                message="You cannot have more than 10,000.00$ in your wallet.",
                code=400,
            )

        result_wallet: WalletDTO = self.wallet_repository.add_funds(client_id, amount)
        if not result_wallet.success:
            self.withdrawal_repository.update_status(idempotency_key, "FAILED")
            return AddFundsToWalletUseCaseResult(
                success=False,
                message="There was an error adding the money into your virtual wallet.",
                code=500,
            )

        wallet.balance = result_wallet.balance

        if self.withdrawal_repository.update_status(
            idempotency_key, "COMPLETED"
        ).success:
            return AddFundsToWalletUseCaseResult(
                success=True,
                message="The money has been successfully deposited into your account.",
                code=201,
                balance=wallet.balance,
            )

        else:
            self.withdrawal_repository.update_status(idempotency_key, "FAILED")
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
