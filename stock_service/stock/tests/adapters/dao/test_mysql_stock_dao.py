from decimal import Decimal

import pytest
from broker.adapters.dao.mysql_stock_dao import MySQLStockDAO
from broker.domain.ports.stock_repository import StockDTO
from broker.models import Stock

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def setup_function(db):
    Stock.objects.create(
        symbol="AAPL",
        volume=123456789,
        previous_close=Decimal("249.15"),
        last_price=Decimal("249.28"),
    )
    yield


def test_get_stock_by_symbol():
    dao = MySQLStockDAO()

    stock_dto = dao.get_stock_by_symbol(symbol="AAPL")

    assert stock_dto.success
    assert stock_dto.code == 200
    assert stock_dto.symbol == "AAPL"
    assert stock_dto.previous_close == Decimal("249.15")
    assert stock_dto.last_price == Decimal("249.28")
    assert stock_dto.volume == 123456789
    assert stock_dto.active


def test_get_stock_by_symbol_not_existing():
    dao = MySQLStockDAO()

    stock_dto = dao.get_stock_by_symbol(symbol="TEST")

    assert not stock_dto.success
    assert stock_dto.code == 404
    assert not stock_dto.active
