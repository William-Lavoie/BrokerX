from unittest.mock import MagicMock, patch
import pytest
from django.contrib.auth.models import User

from broker.adapters.email_otp_repository import EmailOTPRepository

pytestmark = pytest.mark.django_db

from broker.domain.entities.client import ClientProfile
from broker.models import ClientOTP


@pytest.fixture(autouse=True)
def setup_function(db):
    user = User.objects.create(
        first_name="John",
        last_name="Smith",
        email="john_smith@example.com",
    )

    ClientOTP.objects.create(user=user, secret="123abc", number_attempts=0)
    yield


@patch("broker.adapters.email_otp_repository.send_mail")
def test_send_passcode(mock_send_mail):
    repo = EmailOTPRepository()
    mock_send_mail.return_value = 1

    assert repo.send_passcode("john_smith@example.com", "123abc")
    mock_send_mail.assert_called_once_with(
        "Subject here",
        "123abc",
        "from@example.com",
        ["john_smith@example.com"],
        fail_silently=False,
    )


@patch("broker.adapters.email_otp_repository.send_mail")
def test_send_passcode_failure(mock_send_mail):
    repo = EmailOTPRepository()
    mock_send_mail.return_value = 0

    assert not repo.send_passcode("john_smith@example.com", "123abc")


@patch("broker.adapters.email_otp_repository.pyotp.TOTP")
def test_valid_passcode(mock_totp):
    mock_dao = MagicMock()
    repo = EmailOTPRepository(mock_dao)
    mock_dao.get_secret_key.return_value = "123abc"
    mock_totp.return_value.now.return_value = "123456"

    assert repo.verify_passcode("john_smith@example.com", "123456") == (
        True,
        "The passcode has been validated successfully.",
    )

    mock_dao.delete_passcode.assert_called_once_with("john_smith@example.com")


@patch("broker.adapters.email_otp_repository.pyotp.TOTP")
def test_invalid_passcode_max_attempts(mock_totp):
    mock_dao = MagicMock()
    repo = EmailOTPRepository(mock_dao)
    mock_dao.get_secret_key.return_value = "123abc"
    mock_dao.increment_attempts.return_value = False
    mock_totp.return_value.now.return_value = "123456"

    assert repo.verify_passcode("john_smith@example.com", "987654") == (
        False,
        "The maximum number of attempts has been reached",
    )


@patch("broker.adapters.email_otp_repository.pyotp.TOTP")
def test_invalid_passcode_wrong_passcode(mock_totp):
    mock_dao = MagicMock()
    repo = EmailOTPRepository(mock_dao)
    mock_dao.get_secret_key.return_value = "123abc"
    mock_dao.increment_attempts.return_value = True
    mock_totp.return_value.now.return_value = "123456"

    assert repo.verify_passcode("john_smith@example.com", "987654") == (
        False,
        "You have entered an incorrect passcode.",
    )


def test_register_secret():
    mock_dao = MagicMock()
    repo = EmailOTPRepository(mock_dao)
    user = ClientProfile(
        first_name="John",
        last_name="Smith",
        address="456 Privett Drive",
        birth_date="1978-01-01",
        email="john_smith@example.com",
        phone_number="123-456-7890",
        status="fictional",
    )
    repo.register_secret(user, "123abc")

    mock_dao.set_secret_key.assert_called_once_with("john_smith@example.com", "123abc")
