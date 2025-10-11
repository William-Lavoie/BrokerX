import logging

from django.core.exceptions import ObjectDoesNotExist

from ...domain.ports.stock_repository import StockDTO
from ...models import Stock

logger = logging.getLogger(__name__)


class MySQLStockDAO:
    def get_stock_by_symbol(self, symbol: str) -> StockDTO:
        try:
            stock = Stock.objects.get(symbol=symbol)
            return StockDTO(
                success=True,
                code=200,
                symbol=stock.symbol,
                previous_close=stock.previous_close,
                volume=stock.volume,
                last_price=stock.last_price,
            )
        except ObjectDoesNotExist:
            logger.error(
                f"ObjectDoesNotExist exception : There is no stock with the symbol {symbol}",
                exc_info=True,
            )
            return StockDTO(success=False, code=404, active=False)
