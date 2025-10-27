from decimal import Decimal

import pytest
from broker.adapters.dao.mysql_client_dao import MySQLClientDAO
from broker.adapters.django_client_repository import DjangoClientRepository
from broker.adapters.django_transaction_repository import DjangoTransactionRepository
from broker.adapters.django_wallet_repository import DjangoWalletRepository
from broker.adapters.mock_payment_service_repository import MockPaymentServiceRepository
from broker.domain.entities.client import Client, ClientStatus
from broker.services.add_funds_to_wallet_use_case import (
    AddFundsToWalletUseCase,
    AddFundsToWalletUseCaseResult,
)

pytestmark = pytest.mark.django_db


def test_execute_success():
    dao = MySQLClientDAO()
    dao.add_user(
        client=Client(
            first_name="John",
            last_name="Smith",
            address="123 Main St",
            birth_date="1990-01-01",
            email="john@example.com",
            phone_number="1234567890",
            password="securepassword",
            status=ClientStatus.ACTIVE.value,
        )
    )

    use_case = AddFundsToWalletUseCase(
        DjangoClientRepository(),
        MockPaymentServiceRepository(),
        DjangoWalletRepository(),
        DjangoTransactionRepository(),
    )

    result = use_case.execute(
        "john@example.com", Decimal("10.3"), "b4efcb78-d938-48cf-b75a-bfb5b58c52be"
    )

    assert result.success
    assert result.code == 200
    assert (
        result.message == "The money has been successfully deposited into your account"
    )
    assert result.balance == Decimal("10.3")
