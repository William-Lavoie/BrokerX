from decimal import Decimal
import logging

import requests
from order.domain.entities.order import Order
from order.domain.ports.stock_repository import StockException, StockRepository

logger = logging.getLogger("order")


class StockService(StockRepository):
    def update_top_of_book(self, order: Order) -> Decimal:
        response = requests.put(
            "http://stock-app:8004/stock/top-of-book",
            json={
                "symbol": order.symbol,
                "quantity": order.quantity,
                "price": str(order.price) if order.price is not None else None,
                "order_type": order.order_type,
            },
        )

        if response.status_code != 200:
            raise StockException(
                user_message=response.json().get(
                    "message", "An unexpected error occured."
                ),
                log_message=f"WalletException for client {order.client_id}: {response.text}",
                error_code=400,
            )

        logger.error(f"Response is {response.json()}")
        return Decimal(str(response.json().get("price", 0.00)))
