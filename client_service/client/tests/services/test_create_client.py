from unittest.mock import MagicMock

import pytest
from client.adapters.result import Result
from client.domain.entities.client import Client, ClientInvalidException
from client.domain.ports.client_repository import ClientDTO
from client.services.create_client import CreateClientUseCase
from otp.domain.ports.otp_repository import OTPDTO

from client_service.exceptions import DataAccessException

pytestmark = pytest.mark.django_db


def test_execute():
    mock_client_repo = MagicMock()
    mock_otp_repo = MagicMock()

    mock_client_repo.add_user.return_value = ClientDTO(
        success=True, code=201, client_id="test"
    )
    mock_otp_repo.create_passcode.return_value = OTPDTO(
        success=True, code=201, secret="abc1223"
    )

    use_case = CreateClientUseCase(
        client_repository=mock_client_repo, otp_repository=mock_otp_repo
    )

    result = use_case.execute(
        first_name="John",
        last_name="Smith",
        address="123 Main St",
        birth_date="1990-01-01",
        email="john@example.com",
        phone_number="1234567890",
        password="securepassword",
    )

    assert result.message == "The user was successfully created"
    assert result.code == 201


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

    result = use_case.execute(
        first_name="John",
        last_name="Smith",
        address="123 Main St",
        birth_date="1990-01-01",
        email="john@example.com",
        phone_number="1234567890",
        password="securepassword",
    )

    assert (
        result.message
        == "There is already a user with the same email and/or phone number"
    )
    assert result.code == 409


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

    result = use_case.execute(
        first_name="John",
        last_name="Smith",
        address="123 Main St",
        birth_date="1990-01-01",
        email="john@example.com",
        phone_number="1234567890",
        password="securepassword",
    )

    assert (
        result.message
        == "There was an unexpected error. Please try again or contact customer support."
    )
    assert result.code == 500


def test_execute_error_passcode():
    mock_client_repo = MagicMock()
    mock_otp_repo = MagicMock()

    mock_client_repo.add_user.return_value = ClientDTO(
        success=True, code=200, client_id="test"
    )
    mock_otp_repo.create_passcode.return_value = OTPDTO(
        success=False, code=500, secret="abc1223"
    )

    use_case = CreateClientUseCase(
        client_repository=mock_client_repo, otp_repository=mock_otp_repo
    )

    result = use_case.execute(
        first_name="John",
        last_name="Smith",
        address="123 Main St",
        birth_date="1990-01-01",
        email="john@example.com",
        phone_number="1234567890",
        password="securepassword",
    )

    assert result.message == "There was an error creating your passcode."
    assert result.code == 500


def test_get_client_info():
    mock_client_repo = MagicMock()
    mock_otp_repo = MagicMock()

    client = Client(
        first_name="John",
        last_name="Smith",
        email="john@example.com",
        address="123 Main St",
        birth_date="1990-01-01",
        phone_number="1234567890",
        password="securepassword",
        client_id="test",
        status="active",
    )

    mock_client_repo.get_client.return_value = client

    use_case = CreateClientUseCase(
        client_repository=mock_client_repo, otp_repository=mock_otp_repo
    )

    result = use_case.get_client_info(email="john@example.com")

    assert result.client["email"] == "john@example.com"
    assert result.client["first_name"] == "John"
    assert result.client["last_name"] == "Smith"
    assert result.message == "The information was retrieved successfully."
    assert result.code == 200


def test_get_client_info_not_found():
    mock_client_repo = MagicMock()
    mock_otp_repo = MagicMock()

    mock_client_repo.get_client.side_effect = ClientInvalidException(
        user_message="Client not found", error_code=404
    )

    use_case = CreateClientUseCase(
        client_repository=mock_client_repo, otp_repository=mock_otp_repo
    )

    result = use_case.get_client_info(email="john@example.com")

    assert result.message == "Client not found"
    assert result.code == 404


def test_get_client_info_system_error():
    mock_client_repo = MagicMock()
    mock_otp_repo = MagicMock()

    mock_client_repo.get_client.side_effect = DataAccessException(
        user_message="An unexpected error occured", error_code=500
    )

    use_case = CreateClientUseCase(
        client_repository=mock_client_repo, otp_repository=mock_otp_repo
    )

    result = use_case.get_client_info(email="john@example.com")

    assert result.message == "An unexpected error occured"
    assert result.code == 500
