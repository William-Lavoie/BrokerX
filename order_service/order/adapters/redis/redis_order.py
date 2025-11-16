import json
import logging
from decimal import Decimal
from typing import Optional
from uuid import UUID

from order.domain.entities.order import Order
from redis import RedisError

from order_service.redis import redis_client

logger = logging.getLogger("redis")


class RedisOrder:
    def set_orders_by_client(self, client_id: UUID, orders: list[Order]):
        try:
            order_data_json = json.dumps(
                [order.to_dict() for order in orders],
                default=lambda x: float(x) if isinstance(x, Decimal) else x,
            )
            redis_client.set(f"orders:{client_id}", order_data_json)

            logger.info(f"Successfully stored orders for {client_id} in Redis.")

        except RedisError as re:
            logger.error(
                f"Redis  error occurred while storing orders for {client_id}: {re}"
            )

    def get_orders_by_client(self, client_id: UUID) -> Optional[list[Order]]:
        try:
            orders_json = redis_client.get(f"orders:{client_id}")

            if orders_json:
                orders_data = json.loads(orders_json)
                orders = [Order.from_dict(order) for order in orders_data]
                return orders
            else:
                return None

        except RedisError as re:
            logger.error(f"Redis error occurred while fetching order {client_id}: {re}")
            return None

    def redis_get_orders_by_stock(self, symbol: str) -> Optional[list[Order]]:
        try:
            orders_json = redis_client.get(f"orders:{symbol}")

            if orders_json:
                orders_data = json.loads(orders_json)
                orders = [Order.from_dict(order) for order in orders_data]
                return orders
            else:
                return None

        except RedisError as re:
            logger.error(f"Redis error occurred while fetching order {symbol}: {re}")
            return None

    def set_order(self, client_id: UUID, order: Order):
        try:
            orders_client_json = redis_client.get(f"orders:{client_id}")
            if orders_client_json:
                orders_data = json.loads(orders_client_json)
            else:
                orders_data = []

            orders_data.append(order.to_dict())

            redis_client.set(
                f"orders:{client_id}",
                json.dumps(
                    orders_data,
                    default=lambda x: float(x) if isinstance(x, Decimal) else x,
                ),
            )

            orders_stock_json = redis_client.get(f"orders:{order.symbol}")
            if orders_stock_json:
                orders_data = json.loads(orders_stock_json)
            else:
                orders_data = []

            redis_client.set(
                f"orders:{order.symbol}",
                json.dumps(
                    orders_data,
                    default=lambda x: float(x) if isinstance(x, Decimal) else x,
                ),
            )

            logger.error(f"Successfully added an order for {client_id} in Redis.")

        except RedisError as re:
            logger.error(
                f"Redis error occurred while adding order for {client_id}: {re}"
            )
