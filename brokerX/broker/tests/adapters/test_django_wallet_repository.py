from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from broker.adapters.django_wallet_repository import DjangoWalletRepository
from broker.domain.entities.wallet import Wallet
from broker.domain.ports.dao.wallet_dao import WalletDTO

pytestmark = pytest.mark.django_db


def test_add_funds():
    mock_dao = MagicMock()
    mock_dao.add_funds.return_value = Decimal("10.00")

    repo = DjangoWalletRepository(dao=mock_dao)

    assert repo.add_funds("john_smith@example.com", Decimal("24.56")) == Decimal(
        "10.00"
    )
    mock_dao.add_funds.assert_called_once_with(
        "john_smith@example.com", Decimal("24.56")
    )


def test_get_wallet():
    mock_dao = MagicMock()
    mock_dao.get_wallet.return_value = WalletDTO(balance=Decimal("24.56"))

    repo = DjangoWalletRepository(dao=mock_dao)

    wallet = repo.get_wallet("john_smith@example.com")

    assert type(wallet) == Wallet
    assert wallet.balance == Decimal("24.56")
    mock_dao.get_wallet.assert_called_once_with("john_smith@example.com")
