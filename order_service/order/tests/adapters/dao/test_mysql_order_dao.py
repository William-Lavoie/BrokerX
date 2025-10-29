from decimal import Decimal

import pytest
from order.adapters.dao.mysql_order_dao import MySQLOrderDAO
from order.domain.ports.order_repository import OrderDTO
from order.models import Order

pytestmark = pytest.mark.django_db


def test_add_order_no_limit():
    dao = MySQLOrderDAO()

    order_dto = dao.add_order(
        email="john_smith@example.com",
        symbol="AAPL",
        direction="B",
        initial_quantity=10,
        idempotency_key="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
    )

    assert order_dto.success
    assert order_dto.code == 200
    assert order_dto.direction == "B"
    assert order_dto.limit is None
    assert order_dto.remaining_quantity == 10

    order = Order.objects.filter(order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac")

    assert order.count() == 1
    order = order.first()

    assert order.direction == "B"
    assert order.type == "M"
    assert order.initial_quantity == 10
    assert order.remaining_quantity == 10
    assert order.limit is None


def test_add_order_with_limit():
    dao = MySQLOrderDAO()

    order_dto = dao.add_order(
        email="john_smith@example.com",
        symbol="AAPL",
        direction="S",
        initial_quantity=10,
        idempotency_key="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
        limit=Decimal("250.00"),
    )

    assert order_dto.success
    assert order_dto.code == 200
    assert order_dto.direction == "S"
    assert order_dto.limit == Decimal("250.00")
    assert order_dto.remaining_quantity == 10

    order = Order.objects.filter(order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac")

    assert order.count() == 1
    order = order.first()

    assert order.direction == "S"
    assert order.type == "L"
    assert order.stock == Stock.objects.get(symbol="AAPL")
    assert order.initial_quantity == 10
    assert order.remaining_quantity == 10
    assert order.limit == Decimal("250.00")


def test_add_order_client_not_found():
    dao = MySQLOrderDAO()

    order_dto = dao.add_order(
        email="joe@example.com",
        symbol="AAPL",
        direction="B",
        initial_quantity=10,
        idempotency_key="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
        limit=Decimal("250.00"),
    )

    assert not order_dto.success
    assert order_dto.code == 404


def test_add_order_stock_not_found():
    dao = MySQLOrderDAO()

    order_dto = dao.add_order(
        email="joe@example.com",
        symbol="XEQT",
        direction="B",
        initial_quantity=10,
        idempotency_key="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
        limit=Decimal("250.00"),
    )

    assert not order_dto.success
    assert order_dto.code == 404


def test_add_order_is_idempotent():
    dao = MySQLOrderDAO()

    dao.add_order(
        email="john_smith@example.com",
        symbol="AAPL",
        direction="B",
        initial_quantity=10,
        idempotency_key="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
    )
    dao.add_order(
        email="john_smith@example.com",
        symbol="AAPL",
        direction="B",
        initial_quantity=10,
        idempotency_key="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
    )
    order_dto = dao.add_order(
        email="john_smith@example.com",
        symbol="AAPL",
        direction="B",
        initial_quantity=10,
        idempotency_key="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
    )

    assert order_dto.success
    assert order_dto.code == 200
    assert order_dto.direction == "B"
    assert order_dto.limit is None
    assert order_dto.remaining_quantity == 10

    order = Order.objects.filter(order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac")

    assert order.count() == 1
