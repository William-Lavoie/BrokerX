from unittest.mock import MagicMock
import pytest

pytestmark = pytest.mark.django_db

from broker.adapters.django_client_repository import DjangoClientRepository
from broker.domain.entities.client import ClientProfile


def test_add_user():
    mock_dao = MagicMock()
    mock_dao.add_user.return_value = True

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

    assert repo.add_user(client)
    mock_dao.add_user.assert_called_once_with(client)

    mock_dao.add_user.return_value = False
    assert not repo.add_user(client)


def test_update_user_status():
    mock_dao = MagicMock()
    repo = DjangoClientRepository(dao=mock_dao)

    repo.update_user_status("john_smith@example.com", "updated")
    mock_dao.update_status.assert_called_once_with("john_smith@example.com", "updated")
