import pytest

pytestmark = pytest.mark.django_db

from broker.adapters.dao.mysql_user_dao import MySQLUserDAO
from broker.domain.entities.user import User
from broker.models import User


@pytest.fixture(autouse=True)
def setup_function(db):
    User.objects.create(
        first_name="John",
        last_name="Smith",
        address="456 Privett Drive",
        birth_date="1978-01-01",
        email="john_smith@example.com",
        phone_number="123-456-7890",
        status="fictional",
    )
    yield


def test_add_user():
    dao = MySQLUserDAO()
    mock_user = User(
        first_name="Tom",
        last_name="Hanks",
        address="398 Sherbrooke",
        birth_date="1954-01-01",
        email="tom_hanks@example.com",
        phone_number="514-872-1231",
        status="fictional",
    )
    assert dao.add_user(mock_user)

    saved_user = User.objects.filter(email="tom_hanks@example.com")

    assert saved_user.count() == 1

    saved_user = saved_user.first()

    assert saved_user.first_name == mock_user.first_name
    assert saved_user.last_name == mock_user.last_name
    assert saved_user.address == mock_user.address
    assert str(saved_user.birth_date) == mock_user.birth_date
    assert saved_user.email == mock_user.email
    assert saved_user.phone_number == mock_user.phone_number
    assert saved_user.status == mock_user.status


def test_add_user_email_already_used():
    dao = MySQLUserDAO()
    mock_user = User(
        first_name="Mike",
        last_name="Collin",
        address="876 New York",
        birth_date="2001-01-01",
        email="john_smith@example.com",
        phone_number="234-633-6431",
        status="pending",
    )

    assert not dao.add_user(mock_user)


def test_add_user_phone_already_used():
    dao = MySQLUserDAO()
    mock_user = User(
        first_name="Mike",
        last_name="Collin",
        address="876 New York",
        birth_date="2001-01-01",
        email="mike_collin@example.com",
        phone_number="123-456-7890",
        status="pending",
    )

    assert not dao.add_user(mock_user)


def test_update_update_status():
    dao = MySQLUserDAO()
    dao.update_status("john_smith@example.com", "updated")

    user = User.objects.get(email="john_smith@example.com")
    assert user.status == "updated"
