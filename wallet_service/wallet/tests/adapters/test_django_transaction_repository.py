from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from wallet.adapters.django_transaction_repository import DjangoTransactionRepository
from wallet.domain.ports.transaction_repository import TransactionDTO

pytestmark = pytest.mark.django_db


def test_write_transaction():
    mock_dao = MagicMock()
    mock_dao.write_transaction.return_value = TransactionDTO(success=True, code=201)

    repo = DjangoTransactionRepository(dao=mock_dao)

    transaction_dto = repo.write_transaction(
        "f551a526-0deb-42d6-98b9-06f3fcc8cdb5",
        Decimal("10.99"),
        "abcdefghijklmnopqrstuvwxyz",
    )

    assert transaction_dto.success
    assert transaction_dto.code == 201

    mock_dao.write_transaction.assert_called_once_with(
        client_id="f551a526-0deb-42d6-98b9-06f3fcc8cdb5",
        amount=Decimal("10.99"),
        idempotency_key="abcdefghijklmnopqrstuvwxyz",
    )


def test_validate_transaction():
    mock_dao = MagicMock()
    mock_dao.validate_transaction.return_value = TransactionDTO(success=True, code=200)

    repo = DjangoTransactionRepository(dao=mock_dao)

    transaction_dto = repo.validate_transaction("abcdefghijklmnopqrstuvwxyz")

    assert transaction_dto.success
    assert transaction_dto.code == 200

    mock_dao.validate_transaction.assert_called_once_with("abcdefghijklmnopqrstuvwxyz")


def test_fail_transaction():
    mock_dao = MagicMock()
    mock_dao.fail_transaction.return_value = TransactionDTO(success=True, code=200)

    repo = DjangoTransactionRepository(dao=mock_dao)

    transaction_dto = repo.fail_transaction("abcdefghijklmnopqrstuvwxyz")

    assert transaction_dto.success
    assert transaction_dto.code == 200

    mock_dao.fail_transaction.assert_called_once_with("abcdefghijklmnopqrstuvwxyz")
