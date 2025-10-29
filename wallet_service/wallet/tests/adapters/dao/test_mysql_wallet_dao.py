from decimal import Decimal

import pytest
from wallet.adapters.dao.mysql_wallet_dao import MySQLWalletDAO
from wallet.domain.ports.dao.wallet_dao import WalletDTO

pytestmark = pytest.mark.django_db

from wallet.models import Wallet


@pytest.fixture(autouse=True)
def setup_function(db):

    Wallet.objects.create(
        client_id="72a8eff3-9e1e-4d5f-a8b6-438e151a27e7", balance=Decimal(12.87)
    )
    yield


def test_get_balance():
    dao = MySQLWalletDAO()

    wallet_dto = dao.get_balance("72a8eff3-9e1e-4d5f-a8b6-438e151a27e7")

    assert wallet_dto.success
    assert wallet_dto.code == 200
    assert wallet_dto.balance == Decimal("12.87")


def test_get_balance_no_user():
    dao = MySQLWalletDAO()

    wallet_dto = dao.get_balance("820b220d-5967-4597-a584-a5e853c0521c")

    assert wallet_dto.success
    assert wallet_dto.code == 200
    assert wallet_dto.balance == Decimal("0.00")


def test_add_funds():
    dao = MySQLWalletDAO()

    wallet_dto = dao.add_funds("72a8eff3-9e1e-4d5f-a8b6-438e151a27e7", Decimal("20.50"))

    assert wallet_dto.success
    assert wallet_dto.code == 200
    assert wallet_dto.balance == Decimal("33.37")


def test_add_funds_no_user():
    dao = MySQLWalletDAO()

    wallet_dto = dao.add_funds("820b220d-5967-4597-a584-a5e853c0521c", Decimal("20.50"))

    assert wallet_dto.success
    assert wallet_dto.code == 200
    assert wallet_dto.balance == Decimal("20.50")
