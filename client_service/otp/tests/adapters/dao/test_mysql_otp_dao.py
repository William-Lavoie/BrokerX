import pytest
from otp.models import OTP

pytestmark = pytest.mark.django_db

from otp.adapters.dao.mysql_otp_dao import MySQLOTPDAO


@pytest.fixture(autouse=True)
def setup_function(db):
    OTP.objects.create(
        client_id="fc6a8193-d8a7-4b43-aa5c-63a376a89e60",
        secret="123abc",
        number_attempts=0,
    )

    yield


def test_set_secret_key():
    dao = MySQLOTPDAO()

    result = dao.set_secret_key("fc6a8193-d8a7-4b43-aa5c-63a376a89e60", "test")
    assert result.success
    assert result.code == 200

    client_otp = OTP.objects.filter(client_id="fc6a8193-d8a7-4b43-aa5c-63a376a89e60")
    assert client_otp.count() == 1

    client_otp = client_otp.first()

    assert client_otp.secret == "test"
    assert str(client_otp.client_id) == "fc6a8193-d8a7-4b43-aa5c-63a376a89e60"
    assert client_otp.number_attempts == 0


def test_get_secret_key():
    dao = MySQLOTPDAO()

    result = dao.get_secret_key("fc6a8193-d8a7-4b43-aa5c-63a376a89e60")
    assert result.success
    assert result.code == 200
    assert result.secret == "123abc"


def test_get_secret_key_no_user():
    dao = MySQLOTPDAO()

    result = dao.get_secret_key("e79ba06b-624a-42dd-8897-5698f068c1fc")
    assert not result.success
    assert result.code == 404


def test_delete_passcode():
    dao = MySQLOTPDAO()
    result = dao.delete_passcode("fc6a8193-d8a7-4b43-aa5c-63a376a89e60")

    assert result.success
    assert result.code == 200
    assert result.validated
    assert not OTP.objects.filter(client_id="fc6a8193-d8a7-4b43-aa5c-63a376a89e60")


def test_delete_passcode_no_user():
    dao = MySQLOTPDAO()
    result = dao.delete_passcode("e79ba06b-624a-42dd-8897-5698f068c1fc")

    assert not result.success
    assert result.code == 404
    assert not result.validated


def test_increment_attempts():
    dao = MySQLOTPDAO()

    result = dao.increment_attempts("fc6a8193-d8a7-4b43-aa5c-63a376a89e60")

    assert not result.success
    assert result.code == 401
    assert result.attempts == 1
    assert not result.validated

    client_otp = OTP.objects.get(client_id="fc6a8193-d8a7-4b43-aa5c-63a376a89e60")
    assert client_otp.number_attempts == 1


def test_increment_attempts_maximum():
    dao = MySQLOTPDAO()
    client_otp = OTP.objects.get(client_id="fc6a8193-d8a7-4b43-aa5c-63a376a89e60")
    client_otp.number_attempts = 2
    client_otp.save()

    result = dao.increment_attempts("fc6a8193-d8a7-4b43-aa5c-63a376a89e60")
    assert not result.success
    assert result.code == 401
    assert result.attempts == 3
    assert not result.validated

    assert not OTP.objects.filter(client_id="fc6a8193-d8a7-4b43-aa5c-63a376a89e60")


def test_increment_attempts_no_user():
    dao = MySQLOTPDAO()

    result = dao.increment_attempts(client_id="e79ba06b-624a-42dd-8897-5698f068c1fc")

    assert not result.success
    assert result.code == 404
    assert not result.validated
