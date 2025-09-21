import pytest

pytestmark = pytest.mark.django_db

from broker.adapters.dao.mysql_user_dao import MySQLUserDAO
from broker.domain.entities.user import User
from broker.models import User


@pytest.mark.django_db
def test_add_user():
    dao = MySQLUserDAO()
    mock_user = User(
        first_name="John",
        last_name="Smith",
        address="456 Privett Drive",
        birth_date="1978-01-01",
        email="john_smith@example.com",
        phone_number="123-456-7890",
        status="fictional",
    )
    dao.add_user(mock_user)

    saved_user = User.objects.filter(email="john_smith@example.com")

    assert saved_user.count() == 1

    saved_user = saved_user.first()

    assert saved_user.first_name == mock_user.first_name
    assert saved_user.last_name == mock_user.last_name
    assert saved_user.address == mock_user.address
    assert str(saved_user.birth_date) == mock_user.birth_date
    assert saved_user.email == mock_user.email
    assert saved_user.phone_number == mock_user.phone_number
    assert saved_user.status == mock_user.status
