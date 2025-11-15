from datetime import datetime
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from order.adapters.django_order_repository import DjangoOrderRepository
from order.domain.entities.order import Order, OrderDTO

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
    mock_dao.add_order.return_value = OrderDTO(
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
        price=None,
        end_date=None,
        status="PENDING",
        created_at=datetime(2024, 1, 1, 12, 0, 0),
        updated_at=datetime(2024, 1, 1, 12, 0, 0),
    )
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

    assert order.order_id == UUID("b7842be7-c400-4f78-8f8d-9a3712d0d4ac")
    assert order.quantity_executed == 0
    assert order.status == "PENDING"
    assert order.created_at is not None
