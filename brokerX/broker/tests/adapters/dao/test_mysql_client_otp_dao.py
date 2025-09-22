import pytest

pytestmark = pytest.mark.django_db

from broker.adapters.dao.mysql_client_otp_dao import MySQLClientOTPDAO
from broker.models import Client, ClientOTP
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

    ClientOTP.objects.create(user=user, secret="123abc", number_attempts=0)

    yield


def test_set_secret_key():
    dao = MySQLClientOTPDAO()

    assert dao.set_secret_key("john_smith@example.com", "test")

    client_otp = ClientOTP.objects.filter(user__email="john_smith@example.com")
    assert client_otp.count() == 1

    user = User.objects.get(email="john_smith@example.com")
    client_otp = client_otp.first()

    assert client_otp.secret == "test"
    assert client_otp.user == user
    assert client_otp.number_attempts == 0


def test_get_secret_key():
    dao = MySQLClientOTPDAO()

    assert dao.get_secret_key("john_smith@example.com") == "123abc"


def test_increment_attempts():
    dao = MySQLClientOTPDAO()

    assert dao.increment_attempts("john_smith@example.com")

    client_otp = ClientOTP.objects.get(user__email="john_smith@example.com")
    assert client_otp.number_attempts == 1


def test_increment_attempts_maximum():
    dao = MySQLClientOTPDAO()
    client_otp = ClientOTP.objects.get(user__email="john_smith@example.com")
    client_otp.number_attempts = 2
    client_otp.save()

    assert not dao.increment_attempts("john_smith@example.com")

    assert not ClientOTP.objects.filter(user__email="john_smith@example.com")


def test_delete_passcode():
    dao = MySQLClientOTPDAO()
    assert dao.delete_passcode("john_smith@example.com")

    assert not ClientOTP.objects.filter(user__email="john_smith@example.com")
