from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

import pytest
from django.core.exceptions import ObjectDoesNotExist
from order.adapters.dao.mysql_order_dao import MySQLOrderDAO
from order.models import Order, OrderAudit, OrderExecution

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

    assert (
        OrderAudit.objects.filter(
            order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac"
        ).count()
        == 1
    )


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

    assert (
        OrderAudit.objects.filter(
            order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac"
        ).count()
        == 1
    )


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

    assert (
        OrderAudit.objects.filter(
            order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac"
        ).count()
        == 1
    )


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
    assert (
        OrderAudit.objects.filter(
            order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac"
        ).count()
        == 1
    )


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

    assert (
        OrderAudit.objects.filter(
            order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac"
        ).count()
        == 0
    )


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

    assert (
        OrderAudit.objects.filter(
            order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac"
        ).count()
        == 0
    )


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

    assert (
        OrderAudit.objects.filter(
            order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac"
        ).count()
        == 0
    )


def test_get_orders_by_client():
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

    dao.add_order(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        symbol="GOOGL",
        order_type="SELL",
        order_style="LIMIT",
        order_duration="GTC",
        quantity=5,
        idempotency_key="c1234be7-c400-4f78-8f8d-9a3712d0d4ac",
        price=Decimal("1500.00"),
    )

    orders = dao.get_orders_by_client("6456e984-de35-408d-9d71-503d1f266ce2")

    assert len(orders) == 2

    symbols = {order.symbol for order in orders}
    assert symbols == {"AAPL", "GOOGL"}


def test_get_orders_by_client_no_orders():
    dao = MySQLOrderDAO()

    orders = dao.get_orders_by_client("00000000-0000-0000-0000-000000000000")
    assert len(orders) == 0


def test_get_orders_by_client_cancelled():
    dao = MySQLOrderDAO()

    Order.objects.create(
        order_id=UUID("d2342be7-c400-4f78-8f8d-9a3712d0d4ac"),
        client_id=UUID("6456e984-de35-408d-9d71-503d1f266ce2"),
        stock_symbol="AAPL",
        order_type="BUY",
        order_style="MARKET",
        order_duration="DAY",
        quantity=10,
        status="CANCELLED",
    )

    orders = dao.get_orders_by_client("6456e984-de35-408d-9d71-503d1f266ce2")

    assert len(orders) == 0


def test_delete_order():
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

    delete_dto = dao.delete_order(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
    )

    assert delete_dto.success
    assert delete_dto.code == 200
    assert delete_dto.status == "CANCELLED"

    order = Order.objects.get(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
    )
    assert order.status == "CANCELLED"
    assert (
        OrderAudit.objects.filter(
            order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac", action="ORDER_CANCELLED"
        ).count()
        == 1
    )


def test_delete_order_not_found():
    dao = MySQLOrderDAO()

    delete_dto = dao.delete_order(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
    )

    assert not delete_dto.success
    assert delete_dto.code == 404


def test_delete_order_already_cancelled():
    dao = MySQLOrderDAO()

    Order.objects.create(
        order_id=UUID("b7842be7-c400-4f78-8f8d-9a3712d0d4ac"),
        client_id=UUID("6456e984-de35-408d-9d71-503d1f266ce2"),
        stock_symbol="AAPL",
        order_type="BUY",
        order_style="MARKET",
        order_duration="DAY",
        quantity=10,
        status="CANCELLED",
    )

    delete_dto = dao.delete_order(
        client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac",
    )

    assert not delete_dto.success
    assert delete_dto.code == 400


def test_delete_order_rollback():
    dao = MySQLOrderDAO()

    # Simulate an order that will cause an exception during cancellation
    Order.objects.create(
        order_id=UUID("b7842be7-c400-4f78-8f8d-9a3712d0d4ac"),
        client_id=UUID("6456e984-de35-408d-9d71-503d1f266ce2"),
        stock_symbol="AAPL",
        order_type="BUY",
        order_style="MARKET",
        order_duration="DAY",
        quantity=10,
        status="CANCELLED",
    )

    dao.delete_order_rollback(
        client_id=UUID("6456e984-de35-408d-9d71-503d1f266ce2"),
        order_id=UUID("b7842be7-c400-4f78-8f8d-9a3712d0d4ac"),
        previous_status="PENDING",
    )

    order = Order.objects.get(
        order_id=UUID("b7842be7-c400-4f78-8f8d-9a3712d0d4ac"),
        client_id=UUID("6456e984-de35-408d-9d71-503d1f266ce2"),
    )
    assert order.status == "PENDING"


def test_delete_order_rollback_cancelled():
    dao = MySQLOrderDAO()

    # Simulate an order that is not cancelled
    Order.objects.create(
        order_id=UUID("c7842be7-c400-4f78-8f8d-9a3712d0d4ac"),
        client_id=UUID("6456e984-de35-408d-9d71-503d1f266ce2"),
        stock_symbol="AAPL",
        order_type="BUY",
        order_style="MARKET",
        order_duration="DAY",
        quantity=10,
        status="REJECTED",
    )

    dao.delete_order_rollback(
        client_id=UUID("6456e984-de35-408d-9d71-503d1f266ce2"),
        order_id=UUID("c7842be7-c400-4f78-8f8d-9a3712d0d4ac"),
        previous_status="PENDING",
    )

    order = Order.objects.get(
        order_id=UUID("c7842be7-c400-4f78-8f8d-9a3712d0d4ac"),
        client_id=UUID("6456e984-de35-408d-9d71-503d1f266ce2"),
    )
    assert order.status == "REJECTED"


def test_get_potential_matches():
    dao = MySQLOrderDAO()

    # Create some orders to match against
    Order.objects.create(
        order_id=UUID("a1112be7-c400-4f78-8f8d-9a3712d0d4ac"),
        client_id=UUID("1111e984-de35-408d-9d71-503d1f266ce2"),
        stock_symbol="AAPL",
        order_type="SELL",
        order_style="LIMIT",
        order_duration="GTC",
        quantity=10,
        price=Decimal("150.00"),
        status="PENDING",
    )

    Order.objects.create(
        order_id=UUID("b2222be7-c400-4f78-8f8d-9a3712d0d4ac"),
        client_id=UUID("2222e984-de35-408d-9d71-503d1f266ce2"),
        stock_symbol="AAPL",
        order_type="SELL",
        order_style="LIMIT",
        order_duration="GTC",
        quantity=5,
        price=Decimal("155.00"),
        status="PENDING",
    )

    # Order to find matches for
    order = Order(
        order_id=UUID("c3333be7-c400-4f78-8f8d-9a3712d0d4ac"),
        client_id=UUID("3333e984-de35-408d-9d71-503d1f266ce2"),
        stock_symbol="AAPL",
        order_type="BUY",
        order_style="LIMIT",
        order_duration="GTC",
        quantity=8,
        price=Decimal("156.00"),
        status="PENDING",
    )

    matches = dao.get_potential_matches(order)

    assert len(matches) == 2
    match_ids = {match.order_id for match in matches}
    assert match_ids == {
        UUID("a1112be7-c400-4f78-8f8d-9a3712d0d4ac"),
        UUID("b2222be7-c400-4f78-8f8d-9a3712d0d4ac"),
    }


def test_get_potential_matches_no_matches():
    dao = MySQLOrderDAO()

    # Create some orders that won't match
    Order.objects.create(
        order_id=UUID("d4444be7-c400-4f78-8f8d-9a3712d0d4ac"),
        client_id=UUID("4444e984-de35-408d-9d71-503d1f266ce2"),
        stock_symbol="AAPL",
        order_type="BUY",
        order_style="LIMIT",
        order_duration="GTC",
        quantity=10,
        price=Decimal("150.00"),
        status="PENDING",
    )

    # Order to find matches for
    order = Order(
        order_id=UUID("e5555be7-c400-4f78-8f8d-9a3712d0d4ac"),
        client_id=UUID("5555e984-de35-408d-9d71-503d1f266ce2"),
        stock_symbol="AAPL",
        order_type="BUY",
        order_style="LIMIT",
        order_duration="GTC",
        quantity=8,
        price=Decimal("140.00"),
        status="PENDING",
    )

    matches = dao.get_potential_matches(order)

    assert len(matches) == 0


def test_get_potential_matches_sell_order():
    dao = MySQLOrderDAO()

    # Create some orders to match against
    Order.objects.create(
        order_id=UUID("f6666be7-c400-4f78-8f8d-9a3712d0d4ac"),
        client_id=UUID("6666e984-de35-408d-9d71-503d1f266ce2"),
        stock_symbol="AAPL",
        order_type="BUY",
        order_style="LIMIT",
        order_duration="GTC",
        quantity=10,
        price=Decimal("150.00"),
        status="PENDING",
    )

    Order.objects.create(
        order_id=UUID("81aee000-e675-48a2-b587-5da602206c29"),
        client_id=UUID("7777e984-de35-408d-9d71-503d1f266ce2"),
        stock_symbol="AAPL",
        order_type="BUY",
        order_style="LIMIT",
        order_duration="GTC",
        quantity=5,
        price=Decimal("145.00"),
        status="PENDING",
    )

    # Order to find matches for
    order = Order(
        order_id=UUID("79072794-96e7-412e-88e9-eea9492062cb"),
        client_id=UUID("8888e984-de35-408d-9d71-503d1f266ce2"),
        stock_symbol="AAPL",
        order_type="SELL",
        order_style="LIMIT",
        order_duration="GTC",
        quantity=8,
        price=Decimal("148.00"),
        status="PENDING",
    )

    matches = dao.get_potential_matches(order)

    assert len(matches) == 2
    match_ids = {match.order_id for match in matches}
    assert match_ids == {
        UUID("f6666be7-c400-4f78-8f8d-9a3712d0d4ac"),
        UUID("81aee000-e675-48a2-b587-5da602206c29"),
    }


def test_get_potential_matches_same_client():
    dao = MySQLOrderDAO()

    # Create some orders to match against
    Order.objects.create(
        order_id=UUID("81aee000-e675-48a2-b587-5da602206c29"),
        client_id=UUID("9999e984-de35-408d-9d71-503d1f266ce2"),
        stock_symbol="AAPL",
        order_type="SELL",
        order_style="LIMIT",
        order_duration="GTC",
        quantity=10,
        price=Decimal("150.00"),
        status="PENDING",
    )

    # Order to find matches for
    order = Order(
        order_id=UUID("79072794-96e7-412e-88e9-eea9492062cb"),
        client_id=UUID("9999e984-de35-408d-9d71-503d1f266ce2"),
        stock_symbol="AAPL",
        order_type="BUY",
        order_style="LIMIT",
        order_duration="GTC",
        quantity=8,
        price=Decimal("156.00"),
        status="PENDING",
    )

    matches = dao.get_potential_matches(order)

    assert len(matches) == 0


def test_execute_order():
    dao = MySQLOrderDAO()

    Order.objects.create(
        order_id=UUID("b7842be7-c400-4f78-8f8d-9a3712d0d4ac"),
        client_id=UUID("6456e984-de35-408d-9d71-503d1f266ce2"),
        stock_symbol="AAPL",
        order_type="BUY",
        order_style="MARKET",
        order_duration="DAY",
        quantity=10,
        quantity_executed=0,
        status="PENDING",
    )

    Order.objects.create(
        order_id=UUID("c1234be7-c400-4f78-8f8d-9a3712d0d4ac"),
        client_id=UUID("2222e984-de35-408d-9d71-503d1f266ce2"),
        stock_symbol="AAPL",
        order_type="SELL",
        order_style="LIMIT",
        order_duration="GTC",
        quantity=10,
        price=Decimal("150.00"),
        status="PENDING",
    )

    order = Order(
        order_id=UUID("b7842be7-c400-4f78-8f8d-9a3712d0d4ac"),
        client_id=UUID("6456e984-de35-408d-9d71-503d1f266ce2"),
        stock_symbol="AAPL",
        order_type="BUY",
        order_style="MARKET",
        order_duration="DAY",
        quantity=10,
        quantity_executed=0,
        status="PENDING",
    )

    matching_orders = [
        Order(
            order_id=UUID("c1234be7-c400-4f78-8f8d-9a3712d0d4ac"),
            client_id=UUID("2222e984-de35-408d-9d71-503d1f266ce2"),
            stock_symbol="AAPL",
            order_type="SELL",
            order_style="LIMIT",
            order_duration="GTC",
            quantity=10,
            price=Decimal("150.00"),
            status="PENDING",
        )
    ]

    dict = dao.execute_order(
        order=order,
        matching_orders=matching_orders,
    )

    order = Order.objects.get(order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac")
    matching_order = Order.objects.get(order_id="c1234be7-c400-4f78-8f8d-9a3712d0d4ac")
    assert order.quantity_executed == 10
    assert order.status == "EXECUTED"
    assert order.executed_at is not None
    assert matching_order.quantity_executed == 10
    assert matching_order.status == "EXECUTED"
    assert matching_order.executed_at is not None

    assert OrderExecution.objects.filter(
        buyer_client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        seller_client_id="2222e984-de35-408d-9d71-503d1f266ce2",
        quantity=10,
        price=Decimal("150.00"),
    ).exists()

    assert dict["c1234be7-c400-4f78-8f8d-9a3712d0d4ac"]["trade_quantity"] == 10
    assert dict["c1234be7-c400-4f78-8f8d-9a3712d0d4ac"]["price"] == Decimal("150.00")


def test_execute_order_partial():
    dao = MySQLOrderDAO()

    Order.objects.create(
        order_id=UUID("b7842be7-c400-4f78-8f8d-9a3712d0d4ac"),
        client_id=UUID("6456e984-de35-408d-9d71-503d1f266ce2"),
        stock_symbol="AAPL",
        order_type="BUY",
        order_style="MARKET",
        order_duration="DAY",
        quantity=10,
        quantity_executed=0,
        status="PENDING",
    )

    Order.objects.create(
        order_id=UUID("c1234be7-c400-4f78-8f8d-9a3712d0d4ac"),
        client_id=UUID("2222e984-de35-408d-9d71-503d1f266ce2"),
        stock_symbol="AAPL",
        order_type="SELL",
        order_style="LIMIT",
        order_duration="GTC",
        quantity=5,
        price=Decimal("150.00"),
        status="PENDING",
    )

    order = Order(
        order_id=UUID("b7842be7-c400-4f78-8f8d-9a3712d0d4ac"),
        client_id=UUID("6456e984-de35-408d-9d71-503d1f266ce2"),
        stock_symbol="AAPL",
        order_type="BUY",
        order_style="MARKET",
        order_duration="DAY",
        quantity=10,
        quantity_executed=0,
        status="PENDING",
    )

    matching_orders = [
        Order(
            order_id=UUID("c1234be7-c400-4f78-8f8d-9a3712d0d4ac"),
            client_id=UUID("2222e984-de35-408d-9d71-503d1f266ce2"),
            stock_symbol="AAPL",
            order_type="SELL",
            order_style="LIMIT",
            order_duration="GTC",
            quantity=5,
            price=Decimal("150.00"),
            status="PENDING",
        )
    ]

    dict = dao.execute_order(
        order=order,
        matching_orders=matching_orders,
    )

    order = Order.objects.get(order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac")
    matching_order = Order.objects.get(order_id="c1234be7-c400-4f78-8f8d-9a3712d0d4ac")
    assert order.quantity_executed == 5
    assert order.status == "PARTIALLY_EXECUTED"
    assert order.executed_at is None
    assert matching_order.quantity_executed == 5
    assert matching_order.status == "EXECUTED"
    assert matching_order.executed_at is not None

    assert OrderExecution.objects.filter(
        buyer_client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        seller_client_id="2222e984-de35-408d-9d71-503d1f266ce2",
        quantity=5,
        price=Decimal("150.00"),
    ).exists()

    assert dict["c1234be7-c400-4f78-8f8d-9a3712d0d4ac"]["trade_quantity"] == 5
    assert dict["c1234be7-c400-4f78-8f8d-9a3712d0d4ac"]["price"] == Decimal("150.00")


def test_execute_multiple_matching():
    dao = MySQLOrderDAO()

    Order.objects.create(
        order_id=UUID("b7842be7-c400-4f78-8f8d-9a3712d0d4ac"),
        client_id=UUID("6456e984-de35-408d-9d71-503d1f266ce2"),
        stock_symbol="AAPL",
        order_type="BUY",
        order_style="MARKET",
        order_duration="DAY",
        quantity=15,
        quantity_executed=0,
        status="PENDING",
    )

    Order.objects.create(
        order_id=UUID("c1234be7-c400-4f78-8f8d-9a3712d0d4ac"),
        client_id=UUID("2222e984-de35-408d-9d71-503d1f266ce2"),
        stock_symbol="AAPL",
        order_type="SELL",
        order_style="LIMIT",
        order_duration="GTC",
        quantity=10,
        price=Decimal("150.00"),
        status="PENDING",
    )

    Order.objects.create(
        order_id=UUID("d2342be7-c400-4f78-8f8d-9a3712d0d4ac"),
        client_id=UUID("3333e984-de35-408d-9d71-503d1f266ce2"),
        stock_symbol="AAPL",
        order_type="SELL",
        order_style="LIMIT",
        order_duration="GTC",
        quantity=10,
        price=Decimal("150.00"),
        status="PENDING",
    )

    order = Order(
        order_id=UUID("b7842be7-c400-4f78-8f8d-9a3712d0d4ac"),
        client_id=UUID("6456e984-de35-408d-9d71-503d1f266ce2"),
        stock_symbol="AAPL",
        order_type="BUY",
        order_style="MARKET",
        order_duration="DAY",
        quantity=15,
        quantity_executed=0,
        status="PENDING",
    )

    matching_orders = [
        Order(
            order_id=UUID("c1234be7-c400-4f78-8f8d-9a3712d0d4ac"),
            client_id=UUID("2222e984-de35-408d-9d71-503d1f266ce2"),
            stock_symbol="AAPL",
            order_type="SELL",
            order_style="LIMIT",
            order_duration="GTC",
            quantity=10,
            price=Decimal("150.00"),
            status="PENDING",
        ),
        Order(
            order_id=UUID("d2342be7-c400-4f78-8f8d-9a3712d0d4ac"),
            client_id=UUID("3333e984-de35-408d-9d71-503d1f266ce2"),
            stock_symbol="AAPL",
            order_type="SELL",
            order_style="LIMIT",
            order_duration="GTC",
            quantity=10,
            price=Decimal("150.00"),
            status="PENDING",
        ),
    ]

    dict = dao.execute_order(
        order=order,
        matching_orders=matching_orders,
    )

    order = Order.objects.get(order_id="b7842be7-c400-4f78-8f8d-9a3712d0d4ac")
    matching_order1 = Order.objects.get(order_id="c1234be7-c400-4f78-8f8d-9a3712d0d4ac")
    matching_order2 = Order.objects.get(order_id="d2342be7-c400-4f78-8f8d-9a3712d0d4ac")
    assert order.quantity_executed == 15
    assert order.status == "EXECUTED"
    assert order.executed_at is not None

    assert matching_order1.quantity_executed == 10
    assert matching_order1.status == "EXECUTED"
    assert matching_order1.executed_at is not None

    assert matching_order2.quantity_executed == 5
    assert matching_order2.status == "PARTIALLY_EXECUTED"
    assert matching_order2.executed_at is None

    assert OrderExecution.objects.filter(
        buyer_client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        seller_client_id="2222e984-de35-408d-9d71-503d1f266ce2",
        quantity=10,
        price=Decimal("150.00"),
    ).exists()
    assert OrderExecution.objects.filter(
        buyer_client_id="6456e984-de35-408d-9d71-503d1f266ce2",
        seller_client_id="3333e984-de35-408d-9d71-503d1f266ce2",
        quantity=5,
        price=Decimal("150.00"),
    ).exists()
    assert dict["c1234be7-c400-4f78-8f8d-9a3712d0d4ac"]["trade_quantity"] == 10
    assert dict["c1234be7-c400-4f78-8f8d-9a3712d0d4ac"]["price"] == Decimal("150.00")
    assert dict["d2342be7-c400-4f78-8f8d-9a3712d0d4ac"]["trade_quantity"] == 5
    assert dict["d2342be7-c400-4f78-8f8d-9a3712d0d4ac"]["price"] == Decimal("150.00")


def test_execute_order_not_existing():
    dao = MySQLOrderDAO()

    order = Order(
        order_id=UUID("6456e984-de35-408d-9d71-503d1f266ce2"),
        client_id=UUID("6456e984-de35-408d-9d71-503d1f266ce2"),
        stock_symbol="AAPL",
        order_type="BUY",
        order_style="MARKET",
        order_duration="DAY",
        quantity=10,
        quantity_executed=0,
        status="PENDING",
    )

    matching_orders = [
        Order(
            order_id=UUID("2222e984-de35-408d-9d71-503d1f266ce2"),
            client_id=UUID("2222e984-de35-408d-9d71-503d1f266ce2"),
            stock_symbol="AAPL",
            order_type="SELL",
            order_style="LIMIT",
            order_duration="GTC",
            quantity=10,
            price=Decimal("150.00"),
            status="PENDING",
        )
    ]

    dict = dao.execute_order(
        order=order,
        matching_orders=matching_orders,
    )

    assert dict == {}
