import pytest

pytestmark = pytest.mark.django_db

from broker.adapters.dao.mysql_client_dao import MySQLClientDAO
from broker.domain.entities.client import ClientProfile
from broker.models import Client
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
        address="456 Privett Drive",
        birth_date="1978-01-01",
        phone_number="123-456-7890",
        status="fictional",
    )
    yield


def test_add_user():
    dao = MySQLClientDAO()
    mock_client = ClientProfile(
        first_name="Tom",
        last_name="Hanks",
        address="398 Sherbrooke",
        birth_date="1954-01-01",
        email="tom_hanks@example.com",
        phone_number="514-872-1231",
        status="fictional",
    )
    assert dao.add_user(mock_client)

    saved_client = Client.objects.filter(user__email="tom_hanks@example.com")
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
    mock_client = ClientProfile(
        first_name="Mike",
        last_name="Collin",
        address="876 New York",
        birth_date="2001-01-01",
        email="john_smith@example.com",
        phone_number="234-633-6431",
        status="pending",
    )

    assert not dao.add_user(mock_client)


def test_add_user_phone_already_used():
    dao = MySQLClientDAO()
    mock_client = ClientProfile(
        first_name="Mike",
        last_name="Collin",
        address="876 New York",
        birth_date="2001-01-01",
        email="mike_collin@example.com",
        phone_number="123-456-7890",
        status="pending",
    )

    assert not dao.add_user(mock_client)


def test_update_update_status():
    dao = MySQLClientDAO()
    dao.update_status("john_smith@example.com", "updated")

    client = Client.objects.get(user__email="john_smith@example.com")
    assert client.status == "updated"


def test_get_status():
    dao = MySQLClientDAO()
    assert dao.get_status("john_smith@example.com") == "fictional"
