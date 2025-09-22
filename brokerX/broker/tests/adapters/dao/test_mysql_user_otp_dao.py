import pytest

pytestmark = pytest.mark.django_db

from broker.adapters.dao.mysql_user_otp_dao import MySQLUserOTPDAO
from broker.domain.entities.user import User
from broker.models import User, UserOPT


@pytest.fixture(autouse=True)
def setup_function(db):
    user = User.objects.create(
        first_name="John",
        last_name="Smith",
        address="456 Privett Drive",
        birth_date="1978-01-01",
        email="john_smith@example.com",
        phone_number="123-456-7890",
        status="fictional",
    )

    UserOPT.objects.create(user=user, secret="123abc", number_attempts=0)

    yield


def test_set_secret_key():
    dao = MySQLUserOTPDAO()

    assert dao.set_secret_key("john_smith@example.com", "test")

    user_otp = UserOPT.objects.filter(user__email="john_smith@example.com")
    assert user_otp.count() == 1

    user = User.objects.get(email="john_smith@example.com")
    user_otp = user_otp.first()

    assert user_otp.secret == "test"
    assert user_otp.user == user
    assert user_otp.number_attempts == 0


def test_get_secret_key():
    dao = MySQLUserOTPDAO()

    assert dao.get_secret_key("john_smith@example.com") == "123abc"


def test_increment_attempts():
    dao = MySQLUserOTPDAO()

    assert dao.increment_attempts("john_smith@example.com")

    user_otp = UserOPT.objects.get(user__email="john_smith@example.com")
    assert user_otp.number_attempts == 1


def test_increment_attempts_maximum():
    dao = MySQLUserOTPDAO()
    user_otp = UserOPT.objects.get(user__email="john_smith@example.com")
    user_otp.number_attempts = 2
    user_otp.save()

    assert not dao.increment_attempts("john_smith@example.com")

    assert not UserOPT.objects.filter(user__email="john_smith@example.com")


def test_delete_passcode():
    dao = MySQLUserOTPDAO()
    assert dao.delete_passcode("john_smith@example.com")

    assert not UserOPT.objects.filter(user__email="john_smith@example.com")
