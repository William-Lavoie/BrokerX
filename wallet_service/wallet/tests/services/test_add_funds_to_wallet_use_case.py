from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from broker.domain.ports.dao.wallet_dao import WalletDTO
from broker.domain.ports.payment_service_repository import (
    PaymentServiceRepositoryResponse,
)
from broker.domain.ports.transaction_repository import TransactionDTO
from broker.services.add_funds_to_wallet_use_case import (
    AddFundsToWalletUseCase,
    AddFundsToWalletUseCaseResult,
)

pytestmark = pytest.mark.django_db


def test_execute_success():
    mock_client_repo = MagicMock()
    mock_payment_service_repo = MagicMock()
    mock_wallet_repo = MagicMock()
    mock_transaction_repo = MagicMock()
    mock_transaction = MagicMock()

    mock_client_repo.client_is_active.return_value = True
    mock_transaction_repo.write_transaction.return_value = TransactionDTO(
        success=True, code=200, status="P", amount=Decimal("10.0")
    )
    mock_transaction.has_been_processed.return_value = True
    mock_payment_service_repo.withdraw_funds.return_value = (
        PaymentServiceRepositoryResponse(success=True, code=200)
    )
    mock_wallet_repo.get_balance.return_value = WalletDTO(
        success=True, code=201, balance=Decimal("34.58")
    )
    mock_wallet_repo.add_funds.return_value = WalletDTO(
        success=True, code=200, balance=Decimal("44.58")
    )
    mock_transaction_repo.validate_transaction_return_value = TransactionDTO(
        success=True, code=200
    )

    use_case = AddFundsToWalletUseCase(
        client_repository=mock_client_repo,
        payment_service_repository=mock_payment_service_repo,
        wallet_repository=mock_wallet_repo,
        transaction_repository=mock_transaction_repo,
    )

    result = use_case.execute(
        "test@example.com", Decimal("10.0"), "b4efcb78-d938-48cf-b75a-bfb5b58c52be"
    )

    assert result.success
    assert result.code == 200
    assert (
        result.message == "The money has been successfully deposited into your account"
    )
    assert result.balance == Decimal("44.58")


def test_execute_client_inactive():
    mock_client_repo = MagicMock()
    mock_payment_service_repo = MagicMock()
    mock_wallet_repo = MagicMock()
    mock_transaction_repo = MagicMock()

    mock_client_repo.client_is_active.return_value = False

    use_case = AddFundsToWalletUseCase(
        client_repository=mock_client_repo,
        payment_service_repository=mock_payment_service_repo,
        wallet_repository=mock_wallet_repo,
        transaction_repository=mock_transaction_repo,
    )

    result = use_case.execute(
        "test@example.com", Decimal("10.0"), "b4efcb78-d938-48cf-b75a-bfb5b58c52be"
    )

    assert not result.success
    assert result.code == 403
    assert (
        result.message
        == "Your account must be active to add funds to your wallet. The deposit was not processed."
    )


def test_execute_already_processed():
    mock_client_repo = MagicMock()
    mock_payment_service_repo = MagicMock()
    mock_wallet_repo = MagicMock()
    mock_transaction_repo = MagicMock()
    mock_transaction = MagicMock()

    mock_client_repo.client_is_active.return_value = True
    mock_transaction_repo.write_transaction.return_value = TransactionDTO(
        success=True, code=200, status="C", amount=Decimal("10.0")
    )

    use_case = AddFundsToWalletUseCase(
        client_repository=mock_client_repo,
        payment_service_repository=mock_payment_service_repo,
        wallet_repository=mock_wallet_repo,
        transaction_repository=mock_transaction_repo,
    )

    result = use_case.execute(
        "test@example.com", Decimal("10.0"), "b4efcb78-d938-48cf-b75a-bfb5b58c52be"
    )

    assert result.success
    assert result.code == 200
    assert result.message == "This transaction has already been processed"


def test_execute_payment_service_error():
    mock_client_repo = MagicMock()
    mock_payment_service_repo = MagicMock()
    mock_wallet_repo = MagicMock()
    mock_transaction_repo = MagicMock()
    mock_transaction = MagicMock()

    mock_client_repo.client_is_active.return_value = True
    mock_transaction_repo.write_transaction.return_value = TransactionDTO(
        success=True, code=200, status="P", amount=Decimal("10.0")
    )
    mock_transaction.has_been_processed.return_value = True
    mock_payment_service_repo.withdraw_funds.return_value = (
        PaymentServiceRepositoryResponse(success=False, code=500)
    )

    use_case = AddFundsToWalletUseCase(
        client_repository=mock_client_repo,
        payment_service_repository=mock_payment_service_repo,
        wallet_repository=mock_wallet_repo,
        transaction_repository=mock_transaction_repo,
    )

    result = use_case.execute(
        "test@example.com", Decimal("10.0"), "b4efcb78-d938-48cf-b75a-bfb5b58c52be"
    )

    assert not result.success
    assert result.code == 500
    assert (
        result.message
        == "There was an error with the payment service. The deposit was not processed."
    )


def test_execute_cannot_add_funds():
    mock_client_repo = MagicMock()
    mock_payment_service_repo = MagicMock()
    mock_wallet_repo = MagicMock()
    mock_transaction_repo = MagicMock()
    mock_transaction = MagicMock()

    mock_client_repo.client_is_active.return_value = True
    mock_transaction_repo.write_transaction.return_value = TransactionDTO(
        success=True, code=200, status="P", amount=Decimal("10.0")
    )
    mock_transaction.has_been_processed.return_value = True
    mock_payment_service_repo.withdraw_funds.return_value = (
        PaymentServiceRepositoryResponse(success=True, code=200)
    )
    mock_wallet_repo.get_balance.return_value = WalletDTO(
        success=False, code=400, balance=Decimal("34.58")
    )

    use_case = AddFundsToWalletUseCase(
        client_repository=mock_client_repo,
        payment_service_repository=mock_payment_service_repo,
        wallet_repository=mock_wallet_repo,
        transaction_repository=mock_transaction_repo,
    )

    result = use_case.execute(
        "test@example.com", Decimal("100000.0"), "b4efcb78-d938-48cf-b75a-bfb5b58c52be"
    )

    assert not result.success
    assert result.code == 400
    assert result.message == "You cannot have more than 10,000.00$ in your wallet."


def test_execute_add_funds_error():
    mock_client_repo = MagicMock()
    mock_payment_service_repo = MagicMock()
    mock_wallet_repo = MagicMock()
    mock_transaction_repo = MagicMock()
    mock_transaction = MagicMock()

    mock_client_repo.client_is_active.return_value = True
    mock_transaction_repo.write_transaction.return_value = TransactionDTO(
        success=True, code=200, status="P", amount=Decimal("10.0")
    )
    mock_transaction.has_been_processed.return_value = True
    mock_payment_service_repo.withdraw_funds.return_value = (
        PaymentServiceRepositoryResponse(success=True, code=200)
    )
    mock_wallet_repo.get_balance.return_value = WalletDTO(
        success=False, code=500, balance=Decimal("34.58")
    )
    mock_wallet_repo.add_funds.return_value = WalletDTO(success=False, code=500)

    use_case = AddFundsToWalletUseCase(
        client_repository=mock_client_repo,
        payment_service_repository=mock_payment_service_repo,
        wallet_repository=mock_wallet_repo,
        transaction_repository=mock_transaction_repo,
    )

    result = use_case.execute(
        "test@example.com", Decimal("10.0"), "b4efcb78-d938-48cf-b75a-bfb5b58c52be"
    )

    assert not result.success
    assert result.code == 500
    assert (
        result.message
        == "There was an error adding the money into your virtual wallet."
    )


def test_execute_fail_transaction():
    mock_client_repo = MagicMock()
    mock_payment_service_repo = MagicMock()
    mock_wallet_repo = MagicMock()
    mock_transaction_repo = MagicMock()
    mock_transaction = MagicMock()

    mock_client_repo.client_is_active.return_value = True
    mock_transaction_repo.write_transaction.return_value = TransactionDTO(
        success=True, code=200, status="P", amount=Decimal("10.0")
    )
    mock_transaction.has_been_processed.return_value = True
    mock_payment_service_repo.withdraw_funds.return_value = (
        PaymentServiceRepositoryResponse(success=True, code=200)
    )
    mock_wallet_repo.get_balance.return_value = WalletDTO(
        success=False, code=500, balance=Decimal("34.58")
    )
    mock_wallet_repo.add_funds.return_value = WalletDTO(
        success=True, code=200, balance=Decimal("44.58")
    )
    mock_transaction_repo.validate_transaction.return_value = TransactionDTO(
        success=False, code=500
    )

    use_case = AddFundsToWalletUseCase(
        client_repository=mock_client_repo,
        payment_service_repository=mock_payment_service_repo,
        wallet_repository=mock_wallet_repo,
        transaction_repository=mock_transaction_repo,
    )

    result = use_case.execute(
        "test@example.com", Decimal("10.0"), "b4efcb78-d938-48cf-b75a-bfb5b58c52be"
    )

    assert not result.success
    assert result.code == 500
    assert (
        result.message
        == "There was an error while trying to process your deposit. Please try again."
    )
    assert result.balance == Decimal("44.58")
