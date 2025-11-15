from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

import pytest
from order.adapters.dao.mysql_order_dao import MySQLOrderDAO
from order.models import Order

pytestmark = pytest.mark.django_db


def test_add_order_market():
    dao = MySQLOrderDAO()

    order_dto = dao.add_order(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        symbol="AAPL",
        order_type="BUY",
        order_style="MARKET",
        order_duration="DAY",
        quantity=10,
        idempotency_key="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
    )

    assert order_dto.success
    assert order_dto.code == 201
    assert order_dto.client_id == UUID("6456e984-de35-408d-9d71-503d1f266ce2")
    assert order_dto.symbol == "AAPL"
    assert order_dto.order_type == "BUY"
    assert order_dto.order_style == "MARKET"
    assert order_dto.order_duration == "DAY"
    assert order_dto.quantity == 10
    assert order_dto.quantity_executed == 0
    assert order_dto.price is None
    assert order_dto.end_date is None
    assert order_dto.status == "PENDING"

    order = Order.objects.filter(order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac")

    assert order.count() == 1
    order = order.first()

    assert order.client_id == UUID("6456e984-de35-408d-9d71-503d1f266ce2")
    assert order.stock_symbol == "AAPL"
    assert order.order_type == "BUY"
    assert order.order_style == "MARKET"
    assert order.order_duration == "DAY"
    assert order.quantity == 10
    assert order.quantity_executed == 0
    assert order.price is None
    assert order.order_end_date is None
    assert order.status == "PENDING"


def test_add_order_limit():
    dao = MySQLOrderDAO()

    order_dto = dao.add_order(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        symbol="AAPL",
        order_type="BUY",
        order_style="LIMIT",
        order_duration="GTC",
        quantity=10,
        idempotency_key="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
        price=Decimal("250.00"),
    )

    assert order_dto.success
    assert order_dto.code == 201
    assert order_dto.client_id == UUID("6456e984-de35-408d-9d71-503d1f266ce2")
    assert order_dto.symbol == "AAPL"
    assert order_dto.order_type == "BUY"
    assert order_dto.order_style == "LIMIT"
    assert order_dto.order_duration == "GTC"
    assert order_dto.quantity == 10
    assert order_dto.quantity_executed == 0
    assert order_dto.status == "PENDING"
    assert order_dto.price == Decimal("250.00")
    assert order_dto.end_date is None

    order = Order.objects.filter(order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac")

    assert order.count() == 1
    order = order.first()

    assert order.client_id == UUID("6456e984-de35-408d-9d71-503d1f266ce2")
    assert order.stock_symbol == "AAPL"
    assert order.order_type == "BUY"
    assert order.order_style == "LIMIT"
    assert order.order_duration == "GTC"
    assert order.quantity == 10
    assert order.quantity_executed == 0
    assert order.status == "PENDING"
    assert order.price == Decimal("250.00")
    assert order.order_end_date is None


def test_add_order_GTD():
    dao = MySQLOrderDAO()

    order_dto = dao.add_order(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        symbol="AAPL",
        order_type="BUY",
        order_style="LIMIT",
        order_duration="GTD",
        quantity=10,
        end_date=datetime(2024, 12, 31, 23, 59, 59),
        idempotency_key="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
        price=Decimal("250.00"),
    )

    assert order_dto.success
    assert order_dto.code == 201
    assert order_dto.client_id == UUID("6456e984-de35-408d-9d71-503d1f266ce2")
    assert order_dto.symbol == "AAPL"
    assert order_dto.order_type == "BUY"
    assert order_dto.order_style == "LIMIT"
    assert order_dto.order_duration == "GTD"
    assert order_dto.quantity == 10
    assert order_dto.quantity_executed == 0
    assert order_dto.status == "PENDING"
    assert order_dto.price == Decimal("250.00")
    assert order_dto.end_date == date(2024, 12, 31)

    order = Order.objects.filter(order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac")

    assert order.count() == 1
    order = order.first()

    assert order.client_id == UUID("6456e984-de35-408d-9d71-503d1f266ce2")
    assert order.stock_symbol == "AAPL"
    assert order.order_type == "BUY"
    assert order.order_style == "LIMIT"
    assert order.order_duration == "GTD"
    assert order.quantity == 10
    assert order.quantity_executed == 0
    assert order.status == "PENDING"
    assert order.price == Decimal("250.00")
    assert order.order_end_date == date(2024, 12, 31)


def test_add_order_idempotentency():
    dao = MySQLOrderDAO()

    dao.add_order(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        symbol="AAPL",
        order_type="BUY",
        order_style="MARKET",
        order_duration="DAY",
        quantity=10,
        idempotency_key="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
    )

    order_dto = dao.add_order(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        symbol="AAPL",
        order_type="BUY",
        order_style="MARKET",
        order_duration="DAY",
        quantity=10,
        idempotency_key="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
    )

    assert order_dto.success
    assert order_dto.code == 200

    order = Order.objects.filter(order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac")

    assert order.count() == 1


def test_add_order_invalid_quantity():
    dao = MySQLOrderDAO()

    order_dto = dao.add_order(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        symbol="AAPL",
        order_type="BUY",
        order_style="LIMIT",
        order_duration="GTC",
        quantity=-5,
        idempotency_key="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
        price=Decimal("250.00"),
    )

    assert not order_dto.success
    assert order_dto.code == 400

    assert not Order.objects.filter(
        order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac"
    ).exists()


def test_add_order_invalid_limit():
    dao = MySQLOrderDAO()

    order_dto = dao.add_order(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        symbol="AAPL",
        order_type="BUY",
        order_style="LIMIT",
        order_duration="GTC",
        quantity=5,
        idempotency_key="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
    )

    assert not order_dto.success
    assert order_dto.code == 400

    assert not Order.objects.filter(
        order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac"
    ).exists()


def test_add_order_price_with_market():
    dao = MySQLOrderDAO()

    order_dto = dao.add_order(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        symbol="AAPL",
        order_type="BUY",
        order_style="MARKET",
        order_duration="GTC",
        quantity=5,
        price=Decimal("250.00"),
        idempotency_key="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
    )

    assert not order_dto.success
    assert order_dto.code == 400

    assert not Order.objects.filter(
        order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac"
    ).exists()


def test_add_order_gtd_no_date():
    dao = MySQLOrderDAO()

    order_dto = dao.add_order(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        symbol="AAPL",
        order_type="BUY",
        order_style="LIMIT",
        order_duration="GTD",
        quantity=5,
        idempotency_key="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
    )

    assert not order_dto.success
    assert order_dto.code == 400

    assert not Order.objects.filter(
        order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac"
    ).exists()


def test_add_order_end_date_not_gtd():
    dao = MySQLOrderDAO()

    order_dto = dao.add_order(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        symbol="AAPL",
        order_type="BUY",
        order_style="LIMIT",
        order_duration="GTC",
        quantity=5,
        end_date=datetime(2024, 12, 31, 23, 59, 59),
        idempotency_key="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
    )

    assert not order_dto.success
    assert order_dto.code == 400

    assert not Order.objects.filter(
        order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac"
    ).exists()
