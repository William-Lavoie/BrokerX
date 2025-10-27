from decimal import Decimal

import pytest
from wallet.adapters.django_transaction_repository import DjangoTransactionRepository
from wallet.adapters.django_wallet_repository import DjangoWalletRepository
from wallet.adapters.mock_payment_service_repository import MockPaymentServiceRepository
from wallet.services.add_funds_to_wallet_use_case import AddFundsToWalletUseCase

pytestmark = pytest.mark.django_db


def test_execute_success():

    use_case = AddFundsToWalletUseCase(
        MockPaymentServiceRepository(),
        DjangoWalletRepository(),
        DjangoTransactionRepository(),
    )

    result = use_case.execute(
        "6246b964-f640-4139-b2ed-17c8e25b37ed",
        "john@example.com",
        Decimal("10.3"),
        "b4efcb78-d938-48cf-b75a-bfb5b58c52be",
    )

    assert result.success
    assert result.code == 200
    assert (
        result.message == "The money has been successfully deposited into your account"
    )
    assert result.balance == Decimal("10.3")
