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

    result = dao.set_secret_key("john_smith@example.com", "test")
    assert result.success
    assert result.code == 200

    client_otp = ClientOTP.objects.filter(user__email="john_smith@example.com")
    assert client_otp.count() == 1

    user = User.objects.get(email="john_smith@example.com")
    client_otp = client_otp.first()

    assert client_otp.secret == "test"
    assert client_otp.user == user
    assert client_otp.number_attempts == 0


def test_set_secret_key_no_user():
    dao = MySQLClientOTPDAO()

    result = dao.set_secret_key("test@example.com", "test")
    assert not result.success
    assert result.code == 404


def test_get_secret_key():
    dao = MySQLClientOTPDAO()

    result = dao.get_secret_key("john_smith@example.com")
    assert result.success
    assert result.code == 200
    assert result.data == "123abc"


def test_get_secret_key_no_user():
    dao = MySQLClientOTPDAO()

    result = dao.get_secret_key("test@example.com")
    assert not result.success
    assert result.code == 404


def test_delete_passcode():
    dao = MySQLClientOTPDAO()
    result = dao.delete_passcode("john_smith@example.com")

    assert result.success
    assert result.code == 200
    assert not ClientOTP.objects.filter(user__email="john_smith@example.com")


def test_delete_passcode_no_user():
    dao = MySQLClientOTPDAO()
    result = dao.delete_passcode("test@example.com")

    assert not result.success
    assert result.code == 404


def test_increment_attempts():
    dao = MySQLClientOTPDAO()

    result = dao.increment_attempts("john_smith@example.com")

    assert result.success
    assert result.code == 200
    assert result.data == 1

    client_otp = ClientOTP.objects.get(user__email="john_smith@example.com")
    assert client_otp.number_attempts == 1


def test_increment_attempts_maximum():
    dao = MySQLClientOTPDAO()
    client_otp = ClientOTP.objects.get(user__email="john_smith@example.com")
    client_otp.number_attempts = 2
    client_otp.save()

    result = dao.increment_attempts("john_smith@example.com")
    assert result.success
    assert result.code == 200
    assert result.data == 3

    assert not ClientOTP.objects.filter(user__email="john_smith@example.com")


def test_increment_attempts_no_user():
    dao = MySQLClientOTPDAO()

    result = dao.increment_attempts("test@example.com")

    assert not result.success
    assert result.code == 404
