from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from broker.adapters.django_transaction_repository import DjangoTransactionRepository
from broker.domain.ports.dao.client_dao import ClientDTO
from broker.domain.ports.transaction_repository import TransactionDTO

pytestmark = pytest.mark.django_db


def test_write_transaction():
    mock_dao = MagicMock()
    mock_dao.write_transaction.return_value = TransactionDTO(success=True, code=201)

    repo = DjangoTransactionRepository(dao=mock_dao)

    transaction_dto: ClientDTO = repo.write_transaction(
        "test", Decimal("10.99"), "Deposit", "abcdefghijklmnopqrstuvwxyz"
    )

    assert transaction_dto.success
    assert transaction_dto.code == 201

    mock_dao.write_transaction.assert_called_once_with(
        email="test",
        amount=Decimal("10.99"),
        idempotency_key="abcdefghijklmnopqrstuvwxyz",
        type="Deposit",
    )


def test_validate_transaction():
    mock_dao = MagicMock()
    mock_dao.validate_transaction.return_value = TransactionDTO(success=True, code=200)

    repo = DjangoTransactionRepository(dao=mock_dao)

    transaction_dto: ClientDTO = repo.validate_transaction("abcdefghijklmnopqrstuvwxyz")

    assert transaction_dto.success
    assert transaction_dto.code == 200

    mock_dao.validate_transaction.assert_called_once_with("abcdefghijklmnopqrstuvwxyz")


def test_fail_transaction():
    mock_dao = MagicMock()
    mock_dao.fail_transaction.return_value = TransactionDTO(success=True, code=200)

    repo = DjangoTransactionRepository(dao=mock_dao)

    transaction_dto: ClientDTO = repo.fail_transaction("abcdefghijklmnopqrstuvwxyz")

    assert transaction_dto.success
    assert transaction_dto.code == 200

    mock_dao.fail_transaction.assert_called_once_with("abcdefghijklmnopqrstuvwxyz")
