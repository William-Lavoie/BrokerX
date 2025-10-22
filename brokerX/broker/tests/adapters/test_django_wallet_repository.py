from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from broker.adapters.django_wallet_repository import DjangoWalletRepository
from broker.domain.entities.wallet import Wallet
from broker.domain.ports.dao.wallet_dao import WalletDTO

pytestmark = pytest.mark.django_db


def test_add_funds():
    mock_dao = MagicMock()
    mock_dao.add_funds.return_value = WalletDTO(
        success=True, code=200, balance=Decimal("34.56")
    )

    repo = DjangoWalletRepository(dao=mock_dao)

    wallet_dto = repo.add_funds("john_smith@example.com", Decimal("24.56"))

    assert wallet_dto.success
    assert wallet_dto.code == 200
    assert wallet_dto.balance == Decimal("34.56")

    mock_dao.add_funds.assert_called_once_with(
        "john_smith@example.com", Decimal("24.56")
    )


def test_get_balance():
    mock_dao = MagicMock()
    mock_dao.get_balance.return_value = WalletDTO(
        success=True, code=200, balance=Decimal("24.56")
    )

    repo = DjangoWalletRepository(dao=mock_dao)

    balance = repo.get_balance("john_smith@example.com").balance

    assert balance == Decimal("24.56")
    mock_dao.get_balance.assert_called_once_with("john_smith@example.com")


def test_get_balance_error():
    mock_dao = MagicMock()
    mock_dao.get_balance.return_value = WalletDTO(
        success=False, code=500, balance=Decimal("10.00")
    )

    repo = DjangoWalletRepository(dao=mock_dao)

    balance = repo.get_balance("john_smith@example.com").balance

    assert balance == Decimal("0.0")
    mock_dao.get_balance.assert_called_once_with("john_smith@example.com")
