import logging

from django.core.exceptions import ObjectDoesNotExist
from stock.domain.ports.stock_repository import StockDTO
from stock.models import Stock

logger = logging.getLogger("mysql")


class MySQLStockDAO:
    def get_stock_by_symbol(self, symbol: str) -> StockDTO:
        try:
            stock = Stock.objects.get(symbol=symbol)
            return StockDTO(
                success=True,
                code=200,
                symbol=stock.symbol,
                name=stock.name,
                exchange=stock.exchange,
                currency=stock.currency,
                last_price=stock.last_price,
                open_price=stock.open_price,
                high_price=stock.high_price,
                low_price=stock.low_price,
                close_price=stock.close_price,
                bid_price=stock.bid_price,
                bid_size=stock.bid_size,
                ask_price=stock.ask_price,
                ask_size=stock.ask_size,
                volume=stock.volume,
                active=True,
            )

        except ObjectDoesNotExist:
            logger.error(
                f"ObjectDoesNotExist exception : There is no stock with the symbol {symbol}",
                exc_info=True,
            )
            return StockDTO(success=False, code=404, active=False)
