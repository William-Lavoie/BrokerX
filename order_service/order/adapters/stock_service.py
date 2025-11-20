from decimal import Decimal
import logging

import requests
from order.domain.entities.order import Order
from order.domain.ports.stock_repository import StockException, StockRepository

logger = logging.getLogger("order")


class StockService(StockRepository):
    def update_top_of_book(self, order: Order) -> Decimal:
        try:
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
                    log_message=f"StockException for client {order.client_id}: {response.text}",
                    error_code=400,
                )
            
            return Decimal(str(response.json().get("price", 0.00)))
        
        except requests.Timeout:
            raise StockException(
                user_message="The system was not available or could not be reached.",
                log_message=f"Stock service timed out.",
                error_code=504,
            )
        
        except requests.RequestException as e:
            raise StockException(
                user_message="The system was not available or could not be reached.",
                log_message=f"RequestException for client {order.client_id}: {str(e)}",
                error_code=500,
            )
    
