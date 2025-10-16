from unittest.mock import MagicMock

import pytest
from broker.domain.ports.dao.client_dao import ClientDTO

pytestmark = pytest.mark.django_db

from broker.adapters.django_client_repository import DjangoClientRepository
from broker.domain.entities.client import Client, ClientStatus


def test_add_user():
    mock_dao = MagicMock()
    mock_dao.add_user.return_value = ClientDTO(success=True, code=201)

    repo = DjangoClientRepository(dao=mock_dao)
    client = Client(
        first_name="John",
        last_name="Smith",
        address="456 Privett Drive",
        birth_date="1978-01-01",
        email="john_smith@example.com",
        phone_number="123-456-7890",
        status="fictional",
    )

    client_dto: ClientDTO = repo.add_user(client)

    assert client_dto.success
    assert client_dto.code == 201
    mock_dao.add_user.assert_called_once_with(client)


def test_update_user_status():
    mock_dao = MagicMock()
    repo = DjangoClientRepository(dao=mock_dao)

    repo.update_user_status("john_smith@example.com", "updated")
    mock_dao.update_status.assert_called_once_with("john_smith@example.com", "updated")


def test_client_is_active():
    mock_dao = MagicMock()
    mock_dao.get_status.return_value = ClientDTO(
        success=True, code=200, status=ClientStatus.ACTIVE.value
    )
    repo = DjangoClientRepository(dao=mock_dao)

    assert repo.client_is_active("john_smith@example.com")
    mock_dao.get_status.assert_called_once_with("john_smith@example.com")


def test_client_is_not_active():
    mock_dao = MagicMock()
    mock_dao.get_status.return_value = ClientDTO(
        success=True, code=200, status=ClientStatus.REJECTED.value
    )
    repo = DjangoClientRepository(dao=mock_dao)

    assert not repo.client_is_active("john_smith@example.com")
    mock_dao.get_status.assert_called_once_with("john_smith@example.com")
