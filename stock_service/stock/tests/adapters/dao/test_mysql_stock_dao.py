from decimal import Decimal

import pytest
from stock.adapters.dao.mysql_stock_dao import MySQLStockDAO
from stock.domain.ports.stock_repository import StockDTO
from stock.models import Stock

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def setup_function(db):
    Stock.objects.create(
        symbol="AAPL",
        name="Apple Inc.",
        exchange="NASDAQ",
        currency="USD",
        last_price=Decimal("175.35"),
        open_price=Decimal("174.00"),
        high_price=Decimal("176.20"),
        low_price=Decimal("173.50"),
        close_price=Decimal("175.00"),
        bid_price=Decimal("175.30"),
        bid_size=100,
        ask_price=Decimal("175.40"),
        ask_size=120,
        volume=1500000,
    )
    yield


def test_get_stock_by_symbol():
    dao = MySQLStockDAO()

    stock_dto = dao.get_stock_by_symbol(symbol="AAPL")

    assert stock_dto.success
    assert stock_dto.code == 200
    assert stock_dto.symbol == "AAPL"
    assert stock_dto.name == "Apple Inc."
    assert stock_dto.exchange == "NASDAQ"
    assert stock_dto.currency == "USD"
    assert stock_dto.last_price == Decimal("175.35")
    assert stock_dto.open_price == Decimal("174.00")
    assert stock_dto.high_price == Decimal("176.20")
    assert stock_dto.low_price == Decimal("173.50")
    assert stock_dto.close_price == Decimal("175.00")
    assert stock_dto.bid_price == Decimal("175.30")
    assert stock_dto.bid_size == 100
    assert stock_dto.ask_price == Decimal("175.40")
    assert stock_dto.ask_size == 120
    assert stock_dto.volume == 1500000
    assert stock_dto.active


def test_get_stock_by_symbol_not_existing():
    dao = MySQLStockDAO()

    stock_dto = dao.get_stock_by_symbol(symbol="TEST")

    assert not stock_dto.success
    assert stock_dto.code == 404
    assert not stock_dto.active
