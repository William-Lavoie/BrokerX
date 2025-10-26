from unittest.mock import MagicMock

import pytest
from client.adapters.result import Result
from client.services.create_client import CreateClientUseCase

pytestmark = pytest.mark.django_db


def test_execute():
    mock_client_repo = MagicMock()
    mock_otp_repo = MagicMock()

    mock_client_repo.add_user.return_value = Result(success=True, code=201)
    mock_otp_repo.create_passcode.return_value = OTPDTO(
        success=True, code=201, secret="abc1223"
    )

    use_case = CreateClientUseCase(
        client_repository=mock_client_repo, otp_repository=mock_otp_repo
    )

    result = use_case.execute(make_command())

    assert result.success
    assert result.message == "The user was successfully created"


def test_execute_repeat_user():
    mock_client_repo = MagicMock()
    mock_otp_repo = MagicMock()

    mock_client_repo.add_user.return_value = Result(success=False, code=409)
    mock_otp_repo.create_passcode.return_value = OTPDTO(
        success=True, code=201, secret="abc1223"
    )

    use_case = CreateClientUseCase(
        client_repository=mock_client_repo, otp_repository=mock_otp_repo
    )

    result = use_case.execute(make_command())

    assert not result.success
    assert (
        result.message
        == "There is already a user with the same email and/or phone number"
    )


def test_execute_error():
    mock_client_repo = MagicMock()
    mock_otp_repo = MagicMock()

    mock_client_repo.add_user.return_value = Result(success=False, code=500)
    mock_otp_repo.create_passcode.return_value = OTPDTO(
        success=True, code=201, secret="abc1223"
    )

    use_case = CreateClientUseCase(
        client_repository=mock_client_repo, otp_repository=mock_otp_repo
    )

    result = use_case.execute(make_command())

    assert not result.success
    assert (
        result.message
        == "There was an unexpected error. Please try again or contact customer support."
    )


def test_execute_error_passcode():
    mock_client_repo = MagicMock()
    mock_otp_repo = MagicMock()

    mock_client_repo.add_user.return_value = Result(success=True, code=200)
    mock_otp_repo.create_passcode.return_value = OTPDTO(
        success=False, code=500, secret="abc1223"
    )

    use_case = CreateClientUseCase(
        client_repository=mock_client_repo, otp_repository=mock_otp_repo
    )

    result = use_case.execute(make_command())

    assert not result.success
    assert result.message == "There was an error creating your passcode."


def make_command():
    return CreateClientCommand(
        first_name="John",
        last_name="Smith",
        address="123 Main St",
        birth_date="1990-01-01",
        email="john@example.com",
        phone_number="1234567890",
        password="securepassword",
    )
