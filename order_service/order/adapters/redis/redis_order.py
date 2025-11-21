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

    def delete_order(self, order_id: UUID, client_id: UUID) -> None:
        try:
            orders_client_json = redis_client.get(f"orders:{client_id}")
            if orders_client_json:
                orders_data = json.loads(orders_client_json)
            else:
                logger.warning(f"No orders found for client {client_id}.")
                return

            order_found = False
            for order in orders_data:
                if order.get("order_id") == order_id:
                    order["status"] = "CANCELLED"
                    order_found = True
                    break

            if not order_found:
                logger.warning(f"Order {order_id} not found for client {client_id}.")
                return

            redis_client.set(
                f"orders:{client_id}",
                json.dumps(
                    orders_data,
                    default=lambda x: str(x) if isinstance(x, Decimal) else x,
                ),
            )

            # Also update the stock-specific orders if needed
            symbol = next(
                (
                    order.get("symbol")
                    for order in orders_data
                    if order.get("id") == order_id
                ),
                None,
            )
            if symbol:
                orders_stock_json = redis_client.get(f"orders:{symbol}")
                if orders_stock_json:
                    orders_stock_data = json.loads(orders_stock_json)
                    for order in orders_stock_data:
                        if order.get("order_id") == order_id:
                            order["status"] = "CANCELLED"
                            break
                    redis_client.set(
                        f"orders:{symbol}",
                        json.dumps(
                            orders_stock_data,
                            default=lambda x: float(x) if isinstance(x, Decimal) else x,
                        ),
                    )

            logger.info(
                f"Order {order_id} updated successfully for client {client_id}."
            )
            return

        except Exception as e:
            logger.error(
                f"Failed to update order {order_id} for client {client_id}: {e}"
            )
            return
