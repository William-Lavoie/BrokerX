from unittest.mock import MagicMock, patch

import pytest
from otp.adapters.email_otp_repository import EmailOTPRepository
from otp.domain.ports.otp_repository import OTPDTO

pytestmark = pytest.mark.django_db

from otp.models import OTP


@pytest.fixture(autouse=True)
def setup_function(db):
    OTP.objects.create(
        client_id="54cc5b84-5720-4c43-af3f-1ef8d13a440c",
        secret="123abc",
        number_attempts=0,
    )
    yield


@patch("otp.adapters.email_otp_repository.send_mail")
def test_send_passcode(mock_send_mail):
    repo = EmailOTPRepository()
    mock_send_mail.return_value = 1

    assert repo.send_passcode("test", "john_smith@example.com", "123abc")
    mock_send_mail.assert_called_once_with(
        "Here is your passcode: ",
        "123abc",
        "from@example.com",
        ["john_smith@example.com"],
        fail_silently=False,
    )


@patch("otp.adapters.email_otp_repository.send_mail")
def test_send_passcode_failure(mock_send_mail):
    repo = EmailOTPRepository()
    mock_send_mail.return_value = 0

    assert not repo.send_passcode("test", "john_smith@example.com", "123abc")


@patch("otp.adapters.email_otp_repository.send_mail")
def test_send_passcode_exception(mock_send_mail):
    repo = EmailOTPRepository()
    mock_send_mail.side_effect = Exception("Server error")

    assert not repo.send_passcode("test", "john_smith@example.com", "123abc")


@patch("otp.adapters.email_otp_repository.pyotp.TOTP")
def test_verify_passcode(mock_totp):
    mock_dao = MagicMock()
    repo = EmailOTPRepository(mock_dao)
    mock_dao.get_secret_key.return_value = OTPDTO(
        success=True, code=200, secret="123abc"
    )
    mock_totp.return_value.now.return_value = "123456"

    result = repo.verify_passcode("54cc5b84-5720-4c43-af3f-1ef8d13a440c", "123456")
    assert result.success

    mock_dao.delete_passcode.assert_called_once_with(
        "54cc5b84-5720-4c43-af3f-1ef8d13a440c"
    )


@patch("otp.adapters.email_otp_repository.pyotp.TOTP")
def test_invalid_passcode_wrong_passcode(mock_totp):
    mock_dao = MagicMock()
    repo = EmailOTPRepository(mock_dao)
    mock_dao.get_secret_key.return_value = OTPDTO(
        success=True, code=200, secret="123abc"
    )
    mock_dao.increment_attempts.return_value = OTPDTO(
        success=False, code=500, secret="123abc"
    )
    mock_totp.return_value.now.return_value = "123456"

    result = repo.verify_passcode("54cc5b84-5720-4c43-af3f-1ef8d13a440c", "987654")
    assert not result.success
    mock_dao.increment_attempts.assert_called_once_with(
        "54cc5b84-5720-4c43-af3f-1ef8d13a440c"
    )


@patch("otp.adapters.email_otp_repository.pyotp.TOTP")
def test_verify_passcode_no_secret(mock_totp):
    mock_dao = MagicMock()
    repo = EmailOTPRepository(mock_dao)
    mock_dao.get_secret_key.return_value = OTPDTO(success=False, code=500)
    mock_totp.return_value.now.return_value = "123456"

    result = repo.verify_passcode("54cc5b84-5720-4c43-af3f-1ef8d13a440c", "123456")
    assert not result.success


def test_register_secret():
    mock_dao = MagicMock()
    repo = EmailOTPRepository(mock_dao)

    repo.register_secret("54cc5b84-5720-4c43-af3f-1ef8d13a440c", "123abc")

    mock_dao.set_secret_key.assert_called_once_with(
        "54cc5b84-5720-4c43-af3f-1ef8d13a440c", "123abc"
    )
