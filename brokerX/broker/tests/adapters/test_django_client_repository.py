from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from broker.domain.ports.dao.client_dao import ClientDTO
from broker.exceptions import DataAccessException

pytestmark = pytest.mark.django_db

from broker.adapters.django_client_repository import DjangoClientRepository
from broker.domain.entities.client import (
    ClientInvalidException,
    ClientProfile,
    ClientStatus,
)


def test_get_user():
    mock_dao = MagicMock()
    mock_dao.get_client_by_email.return_value = ClientDTO(
        success=True,
        code=200,
        first_name="John",
        last_name="Smith",
        address="456 Privett Drive",
        birth_date="1978-01-01",
        email="john_smith@example.com",
        phone_number="123-456-7890",
        status="fictional",
        wallet={"balance": Decimal("100.00")},
        shares={"AAPL": 100, "VOO": 87, "XEQT": 20},
    )

    repo = DjangoClientRepository(dao=mock_dao)

    client = repo.get_user("john_smith@example.com")

    assert client.first_name == "John"
    assert client.last_name == "Smith"
    assert client.address == "456 Privett Drive"
    assert client.birth_date == "1978-01-01"
    assert client.email == "john_smith@example.com"
    assert client.phone_number == "123-456-7890"
    assert client.status == "fictional"
    assert client.wallet.balance == Decimal("100.00")
    assert client.shares == {"AAPL": 100, "VOO": 87, "XEQT": 20}

    mock_dao.get_client_by_email.assert_called_once_with("john_smith@example.com")


def test_get_user_invalid():
    mock_dao = MagicMock()
    mock_dao.get_client_by_email.return_value = ClientDTO(success=False, code=404)

    repo = DjangoClientRepository(dao=mock_dao)

    with pytest.raises(ClientInvalidException) as exc_info:
        repo.get_user("john_smith@example.com")

    assert exc_info.type == ClientInvalidException
    assert exc_info.value.error_code == 404

    mock_dao.get_client_by_email.assert_called_once_with("john_smith@example.com")


def test_get_user_data_access_error():
    mock_dao = MagicMock()
    mock_dao.get_client_by_email.return_value = ClientDTO(success=False, code=500)

    repo = DjangoClientRepository(dao=mock_dao)

    with pytest.raises(DataAccessException) as exc_info:
        repo.get_user("john_smith@example.com")

    assert exc_info.type == DataAccessException
    assert exc_info.value.error_code == 500

    mock_dao.get_client_by_email.assert_called_once_with("john_smith@example.com")


def test_add_user():
    mock_dao = MagicMock()
    mock_dao.add_user.return_value = ClientDTO(success=True, code=201)

    repo = DjangoClientRepository(dao=mock_dao)
    client = ClientProfile(
        first_name="John",
        last_name="Smith",
        address="456 Privett Drive",
        birth_date="1978-01-01",
        email="john_smith@example.com",
        phone_number="123-456-7890",
        status="fictional",
    )

    client_dto = repo.add_user(client)

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
