from decimal import Decimal

import pytest
from broker.adapters.dao.mysql_wallet_dao import MySQLWalletDAO
from broker.domain.ports.dao.wallet_dao import WalletDTO

pytestmark = pytest.mark.django_db

from broker.models import Wallet
from django.contrib.auth.models import User


@pytest.fixture(autouse=True)
def setup_function(db):
    user = User.objects.create(
        first_name="John",
        last_name="Smith",
        email="john_smith@example.com",
    )

    Wallet.objects.create(user=user, balance=Decimal(12.87))
    yield


def test_get_balance():
    dao = MySQLWalletDAO()

    wallet_dto: WalletDTO = dao.get_balance("john_smith@example.com")

    assert wallet_dto.success
    assert wallet_dto.code == 200
    assert wallet_dto.balance == Decimal("12.87")


def test_get_balance_not_existing():
    dao = MySQLWalletDAO()
    user = User.objects.create(
        username="mark_dow",
        first_name="Mark",
        last_name="Dow",
        email="mike_dow@example.com",
    )
    wallet_dto: WalletDTO = dao.get_balance("mike_dow@example.com")

    assert wallet_dto.success
    assert wallet_dto.code == 200
    assert wallet_dto.balance == Decimal("0.00")


def test_get_balance_no_user():
    dao = MySQLWalletDAO()

    wallet_dto: WalletDTO = dao.get_balance("test@example.com")

    assert not wallet_dto.success
    assert wallet_dto.code == 404


def test_add_funds():
    dao = MySQLWalletDAO()

    wallet_dto: WalletDTO = dao.add_funds("john_smith@example.com", Decimal("20.50"))

    assert wallet_dto.success
    assert wallet_dto.code == 200
    assert wallet_dto.balance == Decimal("33.37")


def test_add_funds_no_user():
    dao = MySQLWalletDAO()

    wallet_dto: WalletDTO = dao.add_funds("test@example.com", Decimal("20.50"))

    assert not wallet_dto.success
    assert wallet_dto.code == 404
