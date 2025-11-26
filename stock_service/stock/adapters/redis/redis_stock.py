import json
import logging
from decimal import Decimal
from typing import Optional

from redis import RedisError
from stock.domain.entities.stock import Stock

from stock_service.redis import redis_client

logger = logging.getLogger("redis")


class RedisStock:
    def set_stock(self, stock: Stock):
        try:
            stock_json = json.dumps(
                stock.to_dict(),
                default=lambda x: str(x) if isinstance(x, Decimal) else x,
            )
            redis_client.set(f"stock:{stock.symbol}", stock_json)

            logger.info(f"Successfully stored stock {stock.symbol} in Redis.")

        except RedisError as re:
            logger.error(
                f"Redis error occurred while storing stock {stock.symbol}: {re}"
            )

    def get_stock(self, symbol: str) -> Optional[Stock]:
        try:
            stock_json = redis_client.get(f"stock:{symbol}")

            if stock_json:
                stock_dict = json.loads(
                    stock_json.decode(),
                    object_hook=lambda d: {
                        k: Decimal(str(v)) if isinstance(v, float) else v
                        for k, v in d.items()
                    },
                )

                return Stock.from_dict(stock_dict)
            else:
                return None

        except RedisError as re:
            logger.error(f"Redis error occurred while fetching stock {symbol}: {re}")
            return None
