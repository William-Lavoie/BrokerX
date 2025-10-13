from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from broker.adapters.django_order_repository import DjangoOrderRepository
from broker.domain.entities.client import ClientProfile
from broker.domain.entities.stock import Stock
from broker.domain.ports.order_repository import OrderDTO
from broker.exceptions import DataAccessException

pytestmark = pytest.mark.django_db


def test_add_order():
    mock_dao = MagicMock()
    mock_dao.add_order.return_value = OrderDTO(
        success=True,
        code=200,
        stock="AAPL",
        direction="B",
        limit=Decimal("250.00"),
        initial_quantity=10,
        remaining_quantity=10,
    )
    repo = DjangoOrderRepository(dao=mock_dao)

    client = ClientProfile(
        first_name="John",
        last_name="Smith",
        address="456 Privett Drive",
        birth_date="1978-01-01",
        email="john_smith@example.com",
        phone_number="123-456-7890",
        status="fictional",
    )

    stock = Stock(
        symbol="AAPL",
        volume=123456789,
        previous_close=Decimal("249.15"),
        last_price=Decimal("249.28"),
    )

    order = repo.add_order(
        client=client,
        stock=stock,
        direction="B",
        initial_quantity=10,
        idempotency_key="ab7608db-5c8c-46be-a7ea-b239d8e13aa6",
        limit=Decimal("250.00"),
    )

    assert order.stock == stock
    assert order.direction == "B"
    assert order.limit == Decimal("250.00")
    assert order.initial_quantity == 10
    assert order.remaining_quantity == 10

    mock_dao.add_order.assert_called_once_with(
        email="john_smith@example.com",
        symbol="AAPL",
        direction="B",
        initial_quantity=10,
        idempotency_key="ab7608db-5c8c-46be-a7ea-b239d8e13aa6",
        limit=Decimal("250.00"),
    )


def test_add_order_data_access_error():
    mock_dao = MagicMock()
    mock_dao.add_order.return_value = OrderDTO(
        success=False,
        code=500,
    )
    repo = DjangoOrderRepository(dao=mock_dao)

    client = ClientProfile(
        first_name="John",
        last_name="Smith",
        address="456 Privett Drive",
        birth_date="1978-01-01",
        email="john_smith@example.com",
        phone_number="123-456-7890",
        status="fictional",
    )

    stock = Stock(
        symbol="AAPL",
        volume=123456789,
        previous_close=Decimal("249.15"),
        last_price=Decimal("249.28"),
    )

    with pytest.raises(DataAccessException) as exc_info:
        order = repo.add_order(
            client=client,
            stock=stock,
            direction="B",
            initial_quantity=10,
            idempotency_key="ab7608db-5c8c-46be-a7ea-b239d8e13aa6",
            limit=Decimal("250.00"),
        )

    assert exc_info.type is DataAccessException
    assert exc_info.value.error_code == 500
    assert (
        exc_info.value.user_message
        == "An unexpected error occurred when trying to place an order for AAPL"
    )

    mock_dao.add_order.assert_called_once_with(
        email="john_smith@example.com",
        symbol="AAPL",
        direction="B",
        initial_quantity=10,
        idempotency_key="ab7608db-5c8c-46be-a7ea-b239d8e13aa6",
        limit=Decimal("250.00"),
    )
