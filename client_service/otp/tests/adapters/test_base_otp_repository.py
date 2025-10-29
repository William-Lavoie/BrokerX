from unittest.mock import ANY, patch

import pytest

pytestmark = pytest.mark.django_db

from otp.adapters.base_otp_repository import BaseOTPRepository


class DummyBaseOTPRepository(BaseOTPRepository):
    def register_secret(self, user, email):
        return "secret"

    def send_passcode(self, email, passcode):
        pass

    def verify_passcode(self, email, passcode):
        return True


@patch.object(DummyBaseOTPRepository, "send_passcode")
@patch.object(DummyBaseOTPRepository, "register_secret", return_value="secret")
def test_create_passcode(mock_register, mock_send):
    repo = DummyBaseOTPRepository()

    repo.create_passcode("b7da9c9a-7a07-4cd9-b05d-ee0af131eed4", "test")
    mock_send.assert_called_once_with(
        "b7da9c9a-7a07-4cd9-b05d-ee0af131eed4", "test", ANY
    )
    mock_register.assert_called_once_with("b7da9c9a-7a07-4cd9-b05d-ee0af131eed4", ANY)


@patch.object(DummyBaseOTPRepository, "send_passcode")
@patch.object(DummyBaseOTPRepository, "register_secret", return_value="secret")
def test_create_passcode_error_send(mock_register, mock_send):
    repo = DummyBaseOTPRepository()

    mock_send.return_value = False
    result = repo.create_passcode("b7da9c9a-7a07-4cd9-b05d-ee0af131eed4", "test")
    assert not result.success
    assert result.code == 500


@patch.object(DummyBaseOTPRepository, "send_passcode")
@patch.object(DummyBaseOTPRepository, "register_secret", return_value="secret")
def test_create_passcode_error_register(mock_register, mock_send):
    repo = DummyBaseOTPRepository()

    mock_register.return_value = False
    result = repo.create_passcode("b7da9c9a-7a07-4cd9-b05d-ee0af131eed4", "test")
    assert not result.success
    assert result.code == 500


def test_generate_passcode():
    repo = DummyBaseOTPRepository()
    secret = repo.generate_passcode()

    assert len(secret) == 32
