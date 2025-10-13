from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from broker.domain.entities.client import ClientProfile
from broker.domain.entities.order import Order
from broker.domain.entities.stock import Stock
from broker.domain.entities.wallet import Wallet
from broker.services.place_order import PlaceOrderUseCase

pytestmark = pytest.mark.django_db


def test_execute_success_sell():
    mock_client_repo = MagicMock()
    mock_stock_repo = MagicMock()
    mock_order_repo = MagicMock()

    client = ClientProfile(
        first_name="John",
        last_name="Smith",
        address="456 Privett Drive",
        birth_date="1978-01-01",
        email="john_smith@example.com",
        phone_number="123-456-7890",
        status="Active",
        wallet=Wallet(balance=Decimal("10000.00")),
        shares={"AAPL": 100},
    )

    stock = Stock(
        symbol="AAPL",
        previous_close=Decimal("249.12"),
        volume=123456,
        last_price=Decimal("249.29"),
    )

    mock_client_repo.get_user.return_value = client
    mock_stock_repo.get_stock_by_symbol.return_value = stock
    mock_order_repo.add_order.return_value = Order(
        stock=stock, direction="S", initial_quantity=25, remaining_quantity=25
    )

    use_case = PlaceOrderUseCase(
        client_repository=mock_client_repo,
        stock_repository=mock_stock_repo,
        order_repository=mock_order_repo,
    )

    result = use_case.execute(
        email="john_smith@example.com",
        direction="S",
        limit=Decimal("250.00"),
        quantity=20,
        symbol="AAPL",
        idempotency_key="b4efcb78-d938-48cf-b75a-bfb5b58c52be",
    )

    assert result.success
    assert result.code == 201
    assert result.message == "The order was placed successfully."


def test_execute_missing_shares_sell():
    mock_client_repo = MagicMock()
    mock_stock_repo = MagicMock()
    mock_order_repo = MagicMock()

    client = ClientProfile(
        first_name="John",
        last_name="Smith",
        address="456 Privett Drive",
        birth_date="1978-01-01",
        email="john_smith@example.com",
        phone_number="123-456-7890",
        status="Active",
        wallet=Wallet(balance=Decimal("10000.00")),
        shares={"AAPL": 10},
    )

    stock = Stock(
        symbol="AAPL",
        previous_close=Decimal("249.12"),
        volume=123456,
        last_price=Decimal("249.29"),
    )

    mock_client_repo.get_user.return_value = client
    mock_stock_repo.get_stock_by_symbol.return_value = stock

    use_case = PlaceOrderUseCase(
        client_repository=mock_client_repo,
        stock_repository=mock_stock_repo,
        order_repository=mock_order_repo,
    )

    result = use_case.execute(
        email="john_smith@example.com",
        direction="S",
        limit=Decimal("250.00"),
        quantity=20,
        symbol="AAPL",
        idempotency_key="b4efcb78-d938-48cf-b75a-bfb5b58c52be",
    )

    assert not result.success
    assert result.code == 400
    assert result.message == "You do not have enough shares to sell."


def test_execute_success_buy_market():
    mock_client_repo = MagicMock()
    mock_stock_repo = MagicMock()
    mock_order_repo = MagicMock()

    client = ClientProfile(
        first_name="John",
        last_name="Smith",
        address="456 Privett Drive",
        birth_date="1978-01-01",
        email="john_smith@example.com",
        phone_number="123-456-7890",
        status="Active",
        wallet=Wallet(balance=Decimal("10000.00")),
        shares={"AAPL": 100},
    )

    stock = Stock(
        symbol="AAPL",
        previous_close=Decimal("249.12"),
        volume=123456,
        last_price=Decimal("249.29"),
    )

    mock_client_repo.get_user.return_value = client
    mock_stock_repo.get_stock_by_symbol.return_value = stock
    mock_order_repo.add_order.return_value = Order(
        stock=stock, direction="B", initial_quantity=25, remaining_quantity=25
    )

    use_case = PlaceOrderUseCase(
        client_repository=mock_client_repo,
        stock_repository=mock_stock_repo,
        order_repository=mock_order_repo,
    )

    result = use_case.execute(
        email="john_smith@example.com",
        direction="B",
        quantity=20,
        symbol="AAPL",
        idempotency_key="b4efcb78-d938-48cf-b75a-bfb5b58c52be",
    )

    assert result.success
    assert result.code == 201
    assert result.message == "The order was placed successfully."


def test_execute_success_buy_limit():
    mock_client_repo = MagicMock()
    mock_stock_repo = MagicMock()
    mock_order_repo = MagicMock()

    client = ClientProfile(
        first_name="John",
        last_name="Smith",
        address="456 Privett Drive",
        birth_date="1978-01-01",
        email="john_smith@example.com",
        phone_number="123-456-7890",
        status="Active",
        wallet=Wallet(balance=Decimal("10000.00")),
        shares={"AAPL": 100},
    )

    stock = Stock(
        symbol="AAPL",
        previous_close=Decimal("249.12"),
        volume=123456,
        last_price=Decimal("249.29"),
    )

    mock_client_repo.get_user.return_value = client
    mock_stock_repo.get_stock_by_symbol.return_value = stock
    mock_order_repo.add_order.return_value = Order(
        stock=stock,
        direction="B",
        initial_quantity=25,
        remaining_quantity=25,
        limit=Decimal("250.00"),
    )

    use_case = PlaceOrderUseCase(
        client_repository=mock_client_repo,
        stock_repository=mock_stock_repo,
        order_repository=mock_order_repo,
    )

    result = use_case.execute(
        email="john_smith@example.com",
        direction="B",
        limit=Decimal("250.00"),
        quantity=20,
        symbol="AAPL",
        idempotency_key="b4efcb78-d938-48cf-b75a-bfb5b58c52be",
    )

    assert result.success
    assert result.code == 201
    assert result.message == "The order was placed successfully."


def test_execute_missing_funds_buy_limit():
    mock_client_repo = MagicMock()
    mock_stock_repo = MagicMock()
    mock_order_repo = MagicMock()

    client = ClientProfile(
        first_name="John",
        last_name="Smith",
        address="456 Privett Drive",
        birth_date="1978-01-01",
        email="john_smith@example.com",
        phone_number="123-456-7890",
        status="Active",
        wallet=Wallet(balance=Decimal("10000.00")),
        shares={"AAPL": 100},
    )

    stock = Stock(
        symbol="AAPL",
        previous_close=Decimal("249.12"),
        volume=123456,
        last_price=Decimal("249.29"),
    )

    mock_client_repo.get_user.return_value = client
    mock_stock_repo.get_stock_by_symbol.return_value = stock

    use_case = PlaceOrderUseCase(
        client_repository=mock_client_repo,
        stock_repository=mock_stock_repo,
        order_repository=mock_order_repo,
    )

    result = use_case.execute(
        email="john_smith@example.com",
        direction="B",
        limit=Decimal("100000.00"),
        quantity=20,
        symbol="AAPL",
        idempotency_key="b4efcb78-d938-48cf-b75a-bfb5b58c52be",
    )

    assert not result.success
    assert result.code == 400
    assert result.message == "You do not have enough funds."


def test_execute_missing_funds_buy_market():
    mock_client_repo = MagicMock()
    mock_stock_repo = MagicMock()
    mock_order_repo = MagicMock()

    client = ClientProfile(
        first_name="John",
        last_name="Smith",
        address="456 Privett Drive",
        birth_date="1978-01-01",
        email="john_smith@example.com",
        phone_number="123-456-7890",
        status="Active",
        wallet=Wallet(balance=Decimal("10000.00")),
        shares={"AAPL": 100},
    )

    stock = Stock(
        symbol="AAPL",
        previous_close=Decimal("249.12"),
        volume=123456,
        last_price=Decimal("24009.29"),
    )

    mock_client_repo.get_user.return_value = client
    mock_stock_repo.get_stock_by_symbol.return_value = stock

    use_case = PlaceOrderUseCase(
        client_repository=mock_client_repo,
        stock_repository=mock_stock_repo,
        order_repository=mock_order_repo,
    )

    result = use_case.execute(
        email="john_smith@example.com",
        direction="B",
        quantity=20,
        symbol="AAPL",
        idempotency_key="b4efcb78-d938-48cf-b75a-bfb5b58c52be",
    )

    assert not result.success
    assert result.code == 400
    assert result.message == "You do not have enough funds."


def test_execute_invalid_quantity():
    mock_client_repo = MagicMock()
    mock_stock_repo = MagicMock()
    mock_order_repo = MagicMock()

    use_case = PlaceOrderUseCase(
        client_repository=mock_client_repo,
        stock_repository=mock_stock_repo,
        order_repository=mock_order_repo,
    )

    result = use_case.execute(
        email="john_smith@example.com",
        direction="B",
        quantity=0,
        symbol="AAPL",
        idempotency_key="b4efcb78-d938-48cf-b75a-bfb5b58c52be",
    )

    assert not result.success
    assert result.code == 403
    assert result.message == "You have entered invalid data."


def test_execute_invalid_limit():
    mock_client_repo = MagicMock()
    mock_stock_repo = MagicMock()
    mock_order_repo = MagicMock()

    use_case = PlaceOrderUseCase(
        client_repository=mock_client_repo,
        stock_repository=mock_stock_repo,
        order_repository=mock_order_repo,
    )

    result = use_case.execute(
        email="john_smith@example.com",
        direction="B",
        quantity=20,
        symbol="AAPL",
        idempotency_key="b4efcb78-d938-48cf-b75a-bfb5b58c52be",
        limit=Decimal("-10.00"),
    )

    assert not result.success
    assert result.code == 403
    assert result.message == "You have entered invalid data."


def test_execute_client_inactive():
    mock_client_repo = MagicMock()
    mock_stock_repo = MagicMock()
    mock_order_repo = MagicMock()

    client = ClientProfile(
        first_name="John",
        last_name="Smith",
        address="456 Privett Drive",
        birth_date="1978-01-01",
        email="john_smith@example.com",
        phone_number="123-456-7890",
        status="Inactive",
        wallet=Wallet(balance=Decimal("10000.00")),
        shares={"AAPL": 100},
    )

    mock_client_repo.get_user.return_value = client

    use_case = PlaceOrderUseCase(
        client_repository=mock_client_repo,
        stock_repository=mock_stock_repo,
        order_repository=mock_order_repo,
    )

    result = use_case.execute(
        email="john_smith@example.com",
        direction="B",
        quantity=20,
        symbol="AAPL",
        idempotency_key="b4efcb78-d938-48cf-b75a-bfb5b58c52be",
    )

    assert not result.success
    assert result.code == 403
    assert (
        result.message
        == "Your account must be active to place orders. The order was not processed."
    )
