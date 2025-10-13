from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from broker.adapters.django_stock_repository import DjangoStockRepository
from broker.domain.entities.stock import StockInvalidException
from broker.domain.ports.stock_repository import StockDTO
from broker.exceptions import DataAccessException

pytestmark = pytest.mark.django_db


def test_get_stock_by_symbol():
    mock_dao = MagicMock()
    mock_dao.get_stock_by_symbol.return_value = StockDTO(
        success=True,
        code=200,
        symbol="AAPL",
        previous_close=Decimal("249.17"),
        volume=12345,
        last_price=Decimal("249.28"),
    )

    repo = DjangoStockRepository(dao=mock_dao)

    stock = repo.get_stock_by_symbol("AAPL")

    assert stock.symbol == "AAPL"
    assert stock.previous_close == Decimal("249.17")
    assert stock.volume == 12345
    assert stock.last_price == Decimal("249.28")

    mock_dao.get_stock_by_symbol.assert_called_once_with("AAPL")


def test_get_stock_by_symbol_not_found():
    mock_dao = MagicMock()
    mock_dao.get_stock_by_symbol.return_value = StockDTO(success=False, code=404)

    repo = DjangoStockRepository(dao=mock_dao)

    with pytest.raises(StockInvalidException) as exc_info:
        stock = repo.get_stock_by_symbol("AAPL")

    assert exc_info.type is StockInvalidException
    assert exc_info.value.error_code == 404

    mock_dao.get_stock_by_symbol.assert_called_once_with("AAPL")


def test_get_stock_by_symbol_server_error():
    mock_dao = MagicMock()
    mock_dao.get_stock_by_symbol.return_value = StockDTO(success=False, code=500)

    repo = DjangoStockRepository(dao=mock_dao)

    with pytest.raises(DataAccessException) as exc_info:
        stock = repo.get_stock_by_symbol("AAPL")

    assert exc_info.type is DataAccessException
    assert exc_info.value.error_code == 500
    assert (
        exc_info.value.user_message
        == "An unexpected error occurred when trying to access AAPL"
    )

    mock_dao.get_stock_by_symbol.assert_called_once_with("AAPL")
