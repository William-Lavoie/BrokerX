from unittest.mock import ANY, MagicMock, patch

import pytest

pytestmark = pytest.mark.django_db

from broker.adapters.base_otp_repository import BaseOTPRepository
from broker.domain.entities.client import ClientProfile


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

    client = ClientProfile(
        first_name="John",
        last_name="Smith",
        address="456 Privett Drive",
        birth_date="1978-01-01",
        email="john_smith@example.com",
        phone_number="123-456-7890",
        status="fictional",
    )

    repo.create_passcode(client)
    mock_send.assert_called_once_with("john_smith@example.com", ANY)
    mock_register.assert_called_once_with(client.email, ANY)


@patch.object(DummyBaseOTPRepository, "send_passcode")
@patch.object(DummyBaseOTPRepository, "register_secret", return_value="secret")
def test_create_passcode_error_send(mock_register, mock_send):
    repo = DummyBaseOTPRepository()

    client = ClientProfile(
        first_name="John",
        last_name="Smith",
        address="456 Privett Drive",
        birth_date="1978-01-01",
        email="john_smith@example.com",
        phone_number="123-456-7890",
        status="fictional",
    )
    mock_send.return_value = False
    result = repo.create_passcode(client)
    assert not result.success
    assert result.code == 500


@patch.object(DummyBaseOTPRepository, "send_passcode")
@patch.object(DummyBaseOTPRepository, "register_secret", return_value="secret")
def test_create_passcode_error_register(mock_register, mock_send):
    repo = DummyBaseOTPRepository()

    client = ClientProfile(
        first_name="John",
        last_name="Smith",
        address="456 Privett Drive",
        birth_date="1978-01-01",
        email="john_smith@example.com",
        phone_number="123-456-7890",
        status="fictional",
    )
    mock_register.return_value = False
    result = repo.create_passcode(client)
    assert not result.success
    assert result.code == 500


def test_generate_passcode():
    repo = DummyBaseOTPRepository()
    secret = repo.generate_passcode()

    assert len(secret) == 32
