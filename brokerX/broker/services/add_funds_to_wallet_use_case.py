from decimal import Decimal

from ..models import Wallet

from ..domain.ports.wallet_repository import WalletRepository
from ..adapters.mock_payment_service_repository import PaymentServiceRepository
from ..domain.ports.client_repository import ClientRepository


class AddFundsToWalletUseCaseResult:
    def __init__(
        self,
        success: bool,
        message: str = None,
        code: str = None,
        new_balance: Decimal = None,
    ):
        self.success = success
        self.message = message
        self.code = code
        self.new_balance = new_balance


class AddFundsToWalletUseCase:
    def __init__(
        self,
        client_repository: ClientRepository,
        payment_service_repository: PaymentServiceRepository,
        wallet_repository: WalletRepository,
    ):
        self.client_repository = client_repository
        self.payment_service_repository = payment_service_repository
        self.wallet_repository = wallet_repository

    def execute(self, email: str, amount: Decimal):

        if not self.client_repository.client_is_active(email):
            return AddFundsToWalletUseCaseResult(
                success=False,
                message="Your account must be active to add funds to your wallet. The deposit was not processed.",
                code=403,
            )

        payment_service_response = self.payment_service_repository.withdraw_funds(
            email, amount
        )

        if not payment_service_response.success:
            return AddFundsToWalletUseCaseResult(
                success=False,
                message="There was an error with the payment service. The deposit was not processed.",
                code=500,
            )

        wallet: Wallet = self.wallet_repository.get_wallet(email)
        if not wallet.can_add_funds(amount):
            return AddFundsToWalletUseCaseResult(
                success=False,
                message="You cannot have more than 10 000.00$ in your wallet.",
                code=400,
            )

        new_balance = self.wallet_repository.add_funds(email, amount)
        wallet.balance = new_balance

        # TODO: log transaction
        return AddFundsToWalletUseCaseResult(
            success=True,
            message="The money has been successfully deposited into your account",
            code=200,
            new_balance=new_balance,
        )
