from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from wallet.adapters.django_wallet_repository import DjangoWalletRepository
from wallet.domain.ports.dao.wallet_dao import WalletDTO

pytestmark = pytest.mark.django_db


def test_add_funds():
    mock_dao = MagicMock()
    mock_redis = MagicMock()

    mock_dao.add_funds.return_value = WalletDTO(
        success=True, code=200, balance=Decimal("34.56")
    )
    mock_redis.set_wallet_balance.return_value = None

    repo = DjangoWalletRepository(dao=mock_dao, redis=mock_redis)

    wallet_dto = repo.add_funds(
        "4a785ef6-4ac3-49ed-bcf7-13fa953b57a7", Decimal("24.56")
    )

    assert wallet_dto.success
    assert wallet_dto.code == 200
    assert wallet_dto.balance == Decimal("34.56")

    mock_dao.add_funds.assert_called_once_with(
        "4a785ef6-4ac3-49ed-bcf7-13fa953b57a7", Decimal("24.56")
    )


def test_get_balance():
    mock_dao = MagicMock()
    mock_redis = MagicMock()

    mock_dao.get_balance.return_value = WalletDTO(
        success=True, code=200, balance=Decimal("24.56")
    )
    mock_redis.get_wallet_balance.return_value = None

    repo = DjangoWalletRepository(dao=mock_dao, redis=mock_redis)

    balance = repo.get_balance("4a785ef6-4ac3-49ed-bcf7-13fa953b57a7").balance

    assert balance == Decimal("24.56")
    mock_dao.get_balance.assert_called_once_with("4a785ef6-4ac3-49ed-bcf7-13fa953b57a7")


def test_get_balance_error():
    mock_dao = MagicMock()
    mock_redis = MagicMock()

    mock_dao.get_balance.return_value = WalletDTO(
        success=False, code=500, balance=Decimal("0.00")
    )
    mock_redis.get_wallet_balance.return_value = None

    repo = DjangoWalletRepository(dao=mock_dao, redis=mock_redis)

    balance = repo.get_balance("4a785ef6-4ac3-49ed-bcf7-13fa953b57a7").balance

    assert balance == Decimal("0.00")
    mock_dao.get_balance.assert_called_once_with("4a785ef6-4ac3-49ed-bcf7-13fa953b57a7")
