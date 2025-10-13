from decimal import Decimal

import pytest
from broker.adapters.dao.mysql_wallet_dao import MySQLWalletDAO
from broker.domain.ports.dao.wallet_dao import WalletDTO

pytestmark = pytest.mark.django_db

from broker.models import Client, Wallet
from django.contrib.auth.models import User


@pytest.fixture(autouse=True)
def setup_function(db):
    user = User.objects.create(
        first_name="John",
        last_name="Smith",
        email="john_smith@example.com",
    )

    client = Client.objects.create(
        user=user,
        first_name="John",
        last_name="Smith",
        email="john_smith@example.com",
        address="456 Privett Drive",
        birth_date="1978-01-01",
        phone_number="123-456-7890",
        status="fictional",
    )

    Wallet.objects.create(client=client, balance=Decimal(12.87))
    yield


def test_get_balance():
    dao = MySQLWalletDAO()

    wallet_dto: WalletDTO = dao.get_balance("john_smith@example.com")

    assert wallet_dto.success
    assert wallet_dto.code == 200
    assert wallet_dto.balance == Decimal("12.87")


def test_get_balance_not_existing():
    dao = MySQLWalletDAO()

    wallet_dto: WalletDTO = dao.get_balance("mike_dow@example.com")

    assert not wallet_dto.success
    assert wallet_dto.code == 404
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
