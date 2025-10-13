from decimal import Decimal

import pytest
from broker.adapters.dao.mysql_order_dao import MySQLOrderDAO
from broker.domain.ports.order_repository import OrderDTO
from broker.models import Client, Order, Stock
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def setup_function(db):
    Stock.objects.create(
        symbol="AAPL",
        volume=123456789,
        previous_close=Decimal("249.15"),
        last_price=Decimal("249.28"),
    )
    user = User.objects.create(
        first_name="John",
        last_name="Smith",
        email="john_smith@example.com",
    )

    Client.objects.create(
        user=user,
        first_name="John",
        last_name="Smith",
        email="john_smith@example.com",
        address="456 Privett Drive",
        birth_date="1978-01-01",
        phone_number="123-456-7890",
        status="fictional",
    )
    yield


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
    assert order.stock == Stock.objects.get(symbol="AAPL")
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
