from datetime import datetime
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from order.adapters.django_order_repository import DjangoOrderRepository
from order.domain.entities.order import Order, OrderDTO, OrderInvalidException

from order_service.exceptions import DataAccessException

pytestmark = pytest.mark.django_db


def test_add_order():
    mock_dao = MagicMock()
    mock_redis = MagicMock()

    order = Order(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        symbol="AAPL",
        order_type="BUY",
        order_style="MARKET",
        order_duration="DAY",
        quantity=10,
    )

    order_dto = OrderDTO(
        success=True,
        code=200,
        symbol="AAPL",
        order_id=UUID("b7842be7-c400-4f78-8f8d-9a3712d0d4ac"),
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        order_type="BUY",
        order_style="MARKET",
        order_duration="DAY",
        quantity=10,
        quantity_executed=0,
        status="PENDING",
        created_at=datetime(2024, 1, 1, 12, 0, 0),
        updated_at=datetime(2024, 1, 1, 12, 0, 0),
    )
    mock_dao.add_order.return_value = order_dto
    mock_redis.set_order.return_value = None

    repo = DjangoOrderRepository(dao=mock_dao, redis=mock_redis)

    repo.add_order(order=order, idempotency_key="b7842be7-c400-4f78-8f8d-9a3712d0d4ac")

    mock_dao.add_order.assert_called_once_with(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        symbol="AAPL",
        order_type="BUY",
        order_style="MARKET",
        order_duration="DAY",
        quantity=10,
        idempotency_key="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
        price=None,
        end_date=None,
    )

    mock_redis.set_order.assert_called_once_with(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2", order=order
    )

    assert order.order_id == UUID("b7842be7-c400-4f78-8f8d-9a3712d0d4ac")
    assert order.quantity_executed == 0
    assert order.status == "PENDING"
    assert order.created_at is not None


def test_add_order_error():
    mock_dao = MagicMock()
    mock_redis = MagicMock()

    order = Order(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        symbol="AAPL",
        order_type="BUY",
        order_style="MARKET",
        order_duration="DAY",
        quantity=10,
    )
    mock_dao.add_order.return_value = OrderDTO(
        success=False,
        code=500,
    )

    repo = DjangoOrderRepository(dao=mock_dao, redis=mock_redis)

    with pytest.raises(DataAccessException) as exc_info:
        repo.add_order(
            order=order, idempotency_key="b7842be7-c400-4f78-8f8d-9a3712d0d4ac"
        )

    assert (
        str(exc_info.value)
        == "An unexpected error occurred when trying to place the order."
    )

    mock_dao.add_order.assert_called_once_with(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        symbol="AAPL",
        order_type="BUY",
        order_style="MARKET",
        order_duration="DAY",
        quantity=10,
        idempotency_key="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
        price=None,
        end_date=None,
    )


def test_get_orders_by_client():
    mock_dao = MagicMock()
    mock_redis = MagicMock()

    order_dto1 = OrderDTO(
        success=True,
        code=200,
        symbol="AAPL",
        order_id=UUID("b7842be7-c400-4f78-8f8d-9a3712d0d4ac"),
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        order_type="BUY",
        order_style="MARKET",
        order_duration="DAY",
        quantity=10,
        quantity_executed=0,
        status="PENDING",
        created_at=datetime(2024, 1, 1, 12, 0, 0),
        updated_at=datetime(2024, 1, 1, 12, 0, 0),
    )

    order_dto2 = OrderDTO(
        success=True,
        code=200,
        symbol="GOOGL",
        order_id=UUID("c1234be7-c400-4f78-8f8d-9a3712d0d4ad"),
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        order_type="SELL",
        order_style="LIMIT",
        order_duration="GTC",
        quantity=5,
        quantity_executed=0,
        status="PENDING",
        created_at=datetime(2024, 1, 2, 12, 0, 0),
        updated_at=datetime(2024, 1, 2, 12, 0, 0),
    )

    mock_dao.get_orders_by_client.return_value = [order_dto1, order_dto2]
    mock_redis.set_orders_by_client.return_value = None

    repo = DjangoOrderRepository(dao=mock_dao, redis=mock_redis)

    orders = repo.get_orders_by_client(client_id="6456e984-de35-408d-9d71-503d1f266ce2")

    mock_dao.get_orders_by_client.assert_called_once_with(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2"
    )

    mock_redis.set_orders_by_client.assert_called_once_with(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2", orders=orders
    )


def test_get_orders_by_client_empty():
    mock_dao = MagicMock()
    mock_redis = MagicMock()

    mock_dao.get_orders_by_client.return_value = []
    mock_redis.set_orders_by_client.return_value = None

    repo = DjangoOrderRepository(dao=mock_dao, redis=mock_redis)

    orders = repo.get_orders_by_client(client_id="6456e984-de35-408d-9d71-503d1f266ce2")

    mock_dao.get_orders_by_client.assert_called_once_with(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2"
    )

    mock_redis.set_orders_by_client.assert_called_once_with(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2", orders=orders
    )

    assert orders == []
    assert len(orders) == 0


def test_delete_order():
    mock_dao = MagicMock()
    mock_redis = MagicMock()

    order_dto = OrderDTO(
        success=True,
        code=200,
        symbol="AAPL",
        order_id=UUID("b7842be7-c400-4f78-8f8d-9a3712d0d4ac"),
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        order_type="BUY",
        order_style="MARKET",
        order_duration="DAY",
        quantity=10,
        quantity_executed=0,
        status="CANCELLED",
        created_at=datetime(2024, 1, 1, 12, 0, 0),
        updated_at=datetime(2024, 1, 2, 12, 0, 0),
    )
    mock_dao.delete_order.return_value = order_dto
    mock_redis.delete_order.return_value = None

    repo = DjangoOrderRepository(dao=mock_dao, redis=mock_redis)

    deleted_order = repo.delete_order(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
    )

    mock_dao.delete_order.assert_called_once_with(
        "6456e984-de35-408d-9d71-503d1f266ce2",
        "b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
    )

    mock_redis.delete_order.assert_called_once_with(
        order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
    )

    assert deleted_order.order_id == UUID("b7842be7-c400-4f78-8f8d-9a3712d0d4ac")
    assert deleted_order.status == "CANCELLED"


def test_delete_order_error():
    mock_dao = MagicMock()
    mock_redis = MagicMock()

    mock_dao.delete_order.return_value = OrderDTO(
        success=False,
        code=500,
    )

    repo = DjangoOrderRepository(dao=mock_dao, redis=mock_redis)

    with pytest.raises(OrderInvalidException) as exc_info:
        repo.delete_order(
            client_id="6456e984-de35-408d-9d71-503d1f266ce2",
            order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
        )

    assert str(exc_info.value) == "The order could not be deleted."

    mock_dao.delete_order.assert_called_once_with(
        "6456e984-de35-408d-9d71-503d1f266ce2",
        "b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
    )

    mock_redis.delete_order.assert_not_called()


def test_delete_order_rollback():
    mock_dao = MagicMock()
    mock_redis = MagicMock()

    mock_dao.delete_order_rollback.return_value = None

    repo = DjangoOrderRepository(dao=mock_dao, redis=mock_redis)

    repo.delete_order_rollback(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
        previous_status="PENDING",
    )

    mock_dao.delete_order_rollback.assert_called_once_with(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
        previous_status="PENDING",
    )


def test_get_potential_matches():
    mock_dao = MagicMock()
    mock_redis = MagicMock()

    order = Order(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        symbol="AAPL",
        order_type="BUY",
        order_style="MARKET",
        order_duration="DAY",
        quantity=10,
    )

    matching_order_dto1 = OrderDTO(
        success=True,
        code=200,
        symbol="AAPL",
        order_id=UUID("c1234be7-c400-4f78-8f8d-9a3712d0d4ad"),
        client_id="1234e984-de35-408d-9d71-503d1f266ce2",
        order_type="SELL",
        order_style="LIMIT",
        order_duration="GTC",
        quantity=10,
        quantity_executed=0,
        status="PENDING",
        created_at=datetime(2024, 1, 2, 12, 0, 0),
        updated_at=datetime(2024, 1, 2, 12, 0, 0),
    )

    mock_dao.get_potential_matches.return_value = [matching_order_dto1]

    repo = DjangoOrderRepository(dao=mock_dao, redis=mock_redis)

    matches = repo.get_potential_matches(order=order)

    mock_dao.get_potential_matches.assert_called_once_with(order=order)

    assert len(matches) == 1
    assert matches[0].order_id == UUID("c1234be7-c400-4f78-8f8d-9a3712d0d4ad")


def test_get_potential_matches_empty():
    mock_dao = MagicMock()
    mock_redis = MagicMock()

    order = Order(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        symbol="AAPL",
        order_type="BUY",
        order_style="MARKET",
        order_duration="DAY",
        quantity=10,
    )

    mock_dao.get_potential_matches.return_value = []

    repo = DjangoOrderRepository(dao=mock_dao, redis=mock_redis)

    matches = repo.get_potential_matches(order=order)

    mock_dao.get_potential_matches.assert_called_once_with(order=order)

    assert len(matches) == 0
    assert matches == []


def test_execute_order():
    mock_dao = MagicMock()
    mock_redis = MagicMock()

    order = Order(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        symbol="AAPL",
        order_type="BUY",
        order_style="MARKET",
        order_duration="DAY",
        quantity=10,
    )

    matching_order = Order(
        client_id="1234e984-de35-408d-9d71-503d1f266ce2",
        symbol="AAPL",
        order_type="SELL",
        order_style="LIMIT",
        order_duration="GTC",
        quantity=10,
    )

    mock_dao.execute_order.return_value = {
        "executed_quantity": 10,
        "remaining_quantity": 0,
        "status": "COMPLETED",
    }

    repo = DjangoOrderRepository(dao=mock_dao, redis=mock_redis)

    result = repo.execute_order(order=order, matching_orders=[matching_order])

    mock_dao.execute_order.assert_called_once_with(
        order=order, matching_orders=[matching_order]
    )

    assert result["executed_quantity"] == 10
    assert result["remaining_quantity"] == 0
    assert result["status"] == "COMPLETED"
