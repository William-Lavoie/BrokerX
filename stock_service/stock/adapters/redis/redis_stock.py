import json
import logging
from decimal import Decimal
from typing import Optional

from redis import RedisError

from brokerX.redis import redis_client

from ...domain.entities.client import Client
from ...domain.entities.stock import Stock

logger = logging.getLogger(__name__)


def redis_set_stock(stock: Stock):
    try:
        stock_json = json.dumps(
            stock.to_dict(),
            default=lambda x: float(x) if isinstance(x, Decimal) else x,
        )
        redis_client.set(f"stock:{stock.symbol}", stock_json)

        logger.info(f"Successfully stored stock {stock.symbol} in Redis.")

    except RedisError as re:
        logger.error(f"Redis error occurred while storing stock {stock.symbol}: {re}")


def redis_get_stock(symbol: str) -> Optional[Stock]:
    try:
        stock_json = redis_client.get(f"stock:{symbol}")

        if stock_json:
            stock_dict = json.loads(stock_json.decode())
            return Stock.from_dict(stock_dict)
        else:
            return None

    except RedisError as re:
        logger.error(f"Redis error occurred while fetching stock {symbol}: {re}")
