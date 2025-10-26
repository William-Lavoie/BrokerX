import json
import logging
from decimal import Decimal
from typing import Optional

from redis import RedisError

from brokerX.redis import redis_client

from ...domain.entities.order import Order

logger = logging.getLogger(__name__)


def redis_set_orders(email: str, orders: list[Order]):
    try:
        order_data_json = json.dumps(
            [order.to_dict() for order in orders],
            default=lambda x: float(x) if isinstance(x, Decimal) else x,
        )
        redis_client.set(f"orders:{email}", order_data_json)

        logger.info(f"Successfully stored orders for {email} in Redis.")

    except RedisError as re:
        logger.error(f"Redis  error occurred while storing orders for {email}: {re}")


def redis_get_orders(email: str) -> Optional[list[Order]]:
    try:
        orders_json = redis_client.get(f"orders:{email}")

        if orders_json:
            orders_data = json.loads(orders_json)
            orders = [Order.from_dict(order) for order in orders_data]
            return orders
        else:
            return None

    except RedisError as re:
        logger.error(f"Redis error occurred while fetching order {email}: {re}")


def redis_add_order(email: str, order: Order):
    try:
        orders_json = redis_client.get(f"orders:{email}")
        if orders_json:
            orders_data = json.loads(orders_json)
        else:
            orders_data = []

        orders_data.append(order.to_dict())

        redis_client.set(
            f"orders:{email}",
            json.dumps(
                orders_data, default=lambda x: float(x) if isinstance(x, Decimal) else x
            ),
        )

        logger.error(f"Successfully added an order for {email} in Redis.")

    except RedisError as re:
        logger.error(f"Redis error occurred while adding order for {email}: {re}")
