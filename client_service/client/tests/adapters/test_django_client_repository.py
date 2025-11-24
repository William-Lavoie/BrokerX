from typing import Any
from unittest.mock import MagicMock

import pytest
from client.domain.ports.dao.client_dao import ClientDTO

pytestmark = pytest.mark.django_db

from client.adapters.django_client_repository import DjangoClientRepository
from client.domain.entities.client import Client, ClientInvalidException, ClientStatus


def test_get_client_from_cache():
    mock_redis = MagicMock()
    mock_client = Client(
        first_name="Jane",
        last_name="Doe",
        birth_date="1990-01-01",
        address="123 Main St",
        email="jane_doe@example.com",
        status=ClientStatus.ACTIVE.value,
        phone_number="555-1234",
        client_id="123e4567-e89b-12d3-a456-426614174000",
    )
    mock_redis.get_client.return_value = mock_client

    repo = DjangoClientRepository(redis=mock_redis)
    client = repo.get_client("jane_doe@example.com")

    assert client == mock_client
    mock_redis.get_client.assert_called_once_with(email="jane_doe@example.com")


def test_get_client_from_dao():
    mock_redis = MagicMock()
    mock_redis.get_client.return_value = None

    mock_dao = MagicMock()
    mock_dao.get_client_by_email.return_value = ClientDTO(
        success=True,
        code=200,
        first_name="Jane",
        last_name="Doe",
        birth_date="1990-01-01",
        address="123 Main St",
        email="jane_doe@example.com",
    )
    repo = DjangoClientRepository(dao=mock_dao, redis=mock_redis)
    client = repo.get_client("jane_doe@example.com")

    assert client.first_name == "Jane"
    assert client.last_name == "Doe"
    assert client.birth_date == "1990-01-01"
    assert client.address == "123 Main St"
    assert client.email == "jane_doe@example.com"

    mock_redis.get_client.assert_called_once_with(email="jane_doe@example.com")
    mock_dao.get_client_by_email.assert_called_once_with(email="jane_doe@example.com")


def test_get_client_not_found():
    mock_redis = MagicMock()
    mock_redis.get_client.return_value = None

    mock_dao = MagicMock()
    mock_dao.get_client_by_email.return_value = ClientDTO(
        success=False,
        code=404,
    )
    repo = DjangoClientRepository(dao=mock_dao, redis=mock_redis)

    with pytest.raises(ClientInvalidException) as exc_info:
        repo.get_client("jane_doe@example.com")

    mock_redis.get_client.assert_called_once_with(email="jane_doe@example.com")
    mock_dao.get_client_by_email.assert_called_once_with(email="jane_doe@example.com")


def test_get_client_data_access_error():
    mock_redis = MagicMock()
    mock_redis.get_client.return_value = None

    mock_dao = MagicMock()
    mock_dao.get_client_by_email.return_value = ClientDTO(
        success=False,
        code=500,
    )
    repo = DjangoClientRepository(dao=mock_dao, redis=mock_redis)

    with pytest.raises(Exception) as exc_info:
        repo.get_client("jane_doe@example.com")

    mock_redis.get_client.assert_called_once_with(email="jane_doe@example.com")
    assert not mock_redis.set_client.called


def test_add_user():
    mock_dao = MagicMock()
    mock_dao.add_user.return_value = ClientDTO(success=True, code=201)
    mock_redis = MagicMock()
    repo = DjangoClientRepository(dao=mock_dao, redis=mock_redis)

    mock_dao.add_user.return_value = ClientDTO(
        success=True,
        code=201,
        client_id="some-uuid",
        status="PENDING",
        first_name="John",
        last_name="Smith",
        birth_date="1978-01-01",
        address="456 Privett Drive",
        email="john_smith@example.com",
        phone_number="123-456-7890",
    )

    client_dto = repo.add_user(
        first_name="John",
        last_name="Smith",
        address="456 Privett Drive",
        birth_date="1978-01-01",
        email="john_smith@example.com",
        phone_number="123-456-7890",
        password="password123",
    )

    assert client_dto.success
    assert client_dto.code == 201
    mock_dao.add_user.assert_called_once_with(
        first_name="John",
        last_name="Smith",
        address="456 Privett Drive",
        birth_date="1978-01-01",
        email="john_smith@example.com",
        phone_number="123-456-7890",
        password="password123",
    )
    mock_redis.set_client.assert_called_once_with(
        client=Client(
            first_name="John",
            last_name="Smith",
            address="456 Privett Drive",
            birth_date="1978-01-01",
            email="john_smith@example.com",
            phone_number="123-456-7890",
            status="PENDING",
            client_id="some-uuid",
            password="",
        )
    )


def test_update_user_status():
    mock_dao = MagicMock()
    mock_redis = MagicMock()
    mock_dao.update_status.return_value = ClientDTO(success=True, code=200)

    repo = DjangoClientRepository(dao=mock_dao, redis=mock_redis)

    repo.update_user_status("john_smith@example.com", "updated")
    mock_dao.update_status.assert_called_once_with("john_smith@example.com", "updated")
    mock_redis.update_client_status.assert_called_once_with(
        "john_smith@example.com", "updated"
    )


def test_client_is_active_from_cache():
    mock_dao = MagicMock()
    mock_redis = MagicMock()
    mock_redis.get_client.return_value = Client(
        first_name="John",
        last_name="Smith",
        birth_date="1978-01-01",
        address="456 Privett Drive",
        email="john_smith@example.com",
        status=ClientStatus.ACTIVE.value,
        phone_number="123-456-7890",
        client_id="123e4567-e89b-12d3-a456-426614174000",
    )
    repo = DjangoClientRepository(dao=mock_dao, redis=mock_redis)

    assert repo.client_is_active("john_smith@example.com")
    mock_redis.get_client.assert_called_once_with(email="john_smith@example.com")
    assert not mock_dao.get_status.called


def test_client_is_active():
    mock_dao = MagicMock()
    mock_redis = MagicMock()

    mock_dao.get_status.return_value = ClientDTO(
        success=True, code=200, status=ClientStatus.ACTIVE.value
    )
    mock_redis.get_client.return_value = None

    repo = DjangoClientRepository(dao=mock_dao, redis=mock_redis)

    assert repo.client_is_active("john_smith@example.com")
    mock_dao.get_status.assert_called_once_with("john_smith@example.com")
    assert not mock_redis.set_client.called


def test_client_is_not_active():
    mock_dao = MagicMock()
    mock_redis = MagicMock()
    mock_dao.get_status.return_value = ClientDTO(
        success=True, code=200, status=ClientStatus.REJECTED.value
    )
    mock_redis.get_client.return_value = None

    repo = DjangoClientRepository(dao=mock_dao, redis=mock_redis)

    assert not repo.client_is_active("john_smith@example.com")
    mock_dao.get_status.assert_called_once_with("john_smith@example.com")
