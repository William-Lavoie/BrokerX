import datetime

import pytest

pytestmark = pytest.mark.django_db

from client.adapters.dao.mysql_client_dao import MySQLClientDAO
from client.models import Client
from django.contrib.auth.models import User


@pytest.fixture(autouse=True)
def setup_function(db):
    user = User.objects.create(
        first_name="John",
        last_name="Smith",
        email="john_smith@example.com",
    )

    Client.objects.create(
        user=user,
        first_name="John",
        last_name="Smith",
        email="john_smith@example.com",
        address="456 Privett Drive",
        birth_date="1978-01-01",
        phone_number="123-456-7890",
        status="fictional",
    )
    yield


def test_get_client_by_email():
    dao = MySQLClientDAO()

    client_dto = dao.get_client_by_email("john_smith@example.com")

    assert client_dto.success
    assert client_dto.code == 200
    assert client_dto.address == "456 Privett Drive"
    assert client_dto.first_name == "John"
    assert client_dto.last_name == "Smith"
    assert client_dto.birth_date == datetime.date(1978, 1, 1)
    assert client_dto.phone_number == "123-456-7890"
    assert client_dto.status == "fictional"


def test_get_client_by_email_not_existing():
    dao = MySQLClientDAO()

    client_dto = dao.get_client_by_email("joe@example.com")

    assert not client_dto.success
    assert client_dto.code == 404


def test_get_client_by_email_no_wallet_or_shares():
    dao = MySQLClientDAO()

    client_dto = dao.get_client_by_email("john_smith@example.com")

    assert client_dto.success
    assert client_dto.code == 200
    assert client_dto.address == "456 Privett Drive"
    assert client_dto.first_name == "John"
    assert client_dto.last_name == "Smith"
    assert client_dto.birth_date == datetime.date(1978, 1, 1)
    assert client_dto.phone_number == "123-456-7890"
    assert client_dto.status == "fictional"


def test_add_user():
    dao = MySQLClientDAO()
    mock_client = Client(
        first_name="Tom",
        last_name="Hanks",
        address="398 Sherbrooke",
        birth_date="1954-01-01",
        email="tom_hanks@example.com",
        phone_number="514-872-1231",
        status="fictional",
    )
    result = dao.add_user(mock_client)
    assert result.success
    assert result.code == 201

    saved_client = Client.objects.filter(email="tom_hanks@example.com")
    saved_user = User.objects.get(email="tom_hanks@example.com")

    assert saved_client.count() == 1

    saved_client = saved_client.first()

    assert saved_user.first_name == mock_client.first_name
    assert saved_user.last_name == mock_client.last_name
    assert saved_user.email == mock_client.email
    assert saved_client.address == mock_client.address
    assert str(saved_client.birth_date) == mock_client.birth_date
    assert saved_client.phone_number == mock_client.phone_number
    assert saved_client.status == mock_client.status


def test_add_user_email_already_used():
    dao = MySQLClientDAO()
    mock_client = Client(
        first_name="Mike",
        last_name="Collin",
        address="876 New York",
        birth_date="2001-01-01",
        email="john_smith@example.com",
        phone_number="234-633-6431",
        status="pending",
    )

    result = dao.add_user(mock_client)
    assert not result.success
    assert result.code == 409


def test_add_user_phone_already_used():
    dao = MySQLClientDAO()
    mock_client = Client(
        first_name="Mike",
        last_name="Collin",
        address="876 New York",
        birth_date="2001-01-01",
        email="mike_collin@example.com",
        phone_number="123-456-7890",
        status="pending",
    )

    result = dao.add_user(mock_client)
    assert not result.success
    assert result.code == 409


def test_add_user_invalid_data():
    dao = MySQLClientDAO()
    mock_client = Client(
        first_name="Mike",
        last_name="Collin",
        address="876 New York",
        birth_date="2001-01-01",
        email=12,
        phone_number="123-456-7840",
        status="pending",
    )
    result = dao.add_user(mock_client)

    assert not result.success
    assert result.code == 400


def test_update_status():
    dao = MySQLClientDAO()
    result = dao.update_status("john_smith@example.com", "updated")

    assert result.success
    assert result.code == 200

    client = Client.objects.get(user__email="john_smith@example.com")
    assert client.status == "updated"


def test_update_status_no_user():
    dao = MySQLClientDAO()
    result = dao.update_status("test@user.com", "updated")

    assert not result.success
    assert result.code == 404


def test_get_status():
    dao = MySQLClientDAO()
    result = dao.get_status("john_smith@example.com")

    assert result.success
    assert result.code == 200
    assert result.status == "fictional"


def test_get_status_no_user():
    dao = MySQLClientDAO()
    result = dao.get_status("test@user.com")

    assert not result.success
    assert result.code == 404
