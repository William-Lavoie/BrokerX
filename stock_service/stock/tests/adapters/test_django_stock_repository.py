from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from stock.adapters.django_stock_repository import DjangoStockRepository
from stock.domain.entities.stock import StockInvalidException
from stock.domain.ports.stock_repository import StockDTO

from stock_service.exceptions import DataAccessException

pytestmark = pytest.mark.django_db


def test_get_stock_by_symbol():
    mock_dao = MagicMock()
    mock_redis = MagicMock()

    mock_dao.get_stock_by_symbol.return_value = StockDTO(
        success=True,
        code=200,
        symbol="AAPL",
    )
    mock_redis.get_stock.return_value = None

    repo = DjangoStockRepository(dao=mock_dao, redis=mock_redis)

    stock = repo.get_stock_by_symbol("AAPL")

    assert stock.symbol == "AAPL"

    mock_dao.get_stock_by_symbol.assert_called_once_with("AAPL")


def test_get_stock_by_symbol_not_found():
    mock_dao = MagicMock()
    mock_redis = MagicMock()

    mock_dao.get_stock_by_symbol.return_value = StockDTO(success=False, code=404)
    mock_redis.get_stock.return_value = None

    repo = DjangoStockRepository(dao=mock_dao, redis=mock_redis)

    with pytest.raises(StockInvalidException) as exc_info:
        stock = repo.get_stock_by_symbol("AAPL")

    assert exc_info.type is StockInvalidException
    assert exc_info.value.error_code == 404

    mock_dao.get_stock_by_symbol.assert_called_once_with("AAPL")


def test_get_stock_by_symbol_server_error():
    mock_dao = MagicMock()
    mock_redis = MagicMock()

    mock_dao.get_stock_by_symbol.return_value = StockDTO(success=False, code=500)
    mock_redis.get_stock.return_value = None

    repo = DjangoStockRepository(dao=mock_dao, redis=mock_redis)

    with pytest.raises(DataAccessException) as exc_info:
        stock = repo.get_stock_by_symbol("AAPL")

    assert exc_info.type is DataAccessException
    assert exc_info.value.error_code == 500
    assert (
        exc_info.value.user_message
        == "An unexpected error occurred when trying to access AAPL"
    )

    mock_dao.get_stock_by_symbol.assert_called_once_with("AAPL")
