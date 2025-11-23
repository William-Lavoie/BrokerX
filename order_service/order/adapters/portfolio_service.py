import logging
from decimal import Decimal

import requests
from order.domain.entities.order import Order
from order.domain.ports.portfolio_repository import (
    PortfolioException,
    PortfolioRepository,
)

logger = logging.getLogger("order")


class PortfolioService(PortfolioRepository):
    def reserve_holdings(self, order: Order) -> None:
        try:
            response = requests.post(
                "http://portfolio-app:8005/portfolio/reserve/",
                json={
                    "symbol": order.symbol,
                    "quantity": order.quantity,
                },
            )

            if response.status_code != 200:
                raise PortfolioException(
                    user_message=response.json().get(
                        "message", "An unexpected error occured."
                    ),
                    log_message=f"PortfolioException for client {order.client_id}: {response.text}",
                    error_code=400,
                )

            return Decimal(str(response.json().get("price", 0.00)))

        except requests.Timeout:
            raise PortfolioException(
                user_message="The system was not available or could not be reached.",
                log_message=f"Portfolio service timed out.",
                error_code=504,
            )
        except requests.RequestException as e:
            raise PortfolioException(
                user_message="The system was not available or could not be reached.",
                log_message=f"RequestException for client {order.client_id}: {str(e)}",
                error_code=500,
            )

    def release_holdings(self, order: Order) -> None:
        try:
            response = requests.put(
                "http://portfolio-app:8005/portfolio/release",
                json={
                    "symbol": order.symbol,
                    "quantity": order.quantity,
                },
            )

            if response.status_code != 200:
                raise PortfolioException(
                    user_message=response.json().get(
                        "message", "An unexpected error occured."
                    ),
                    log_message=f"PortfolioException for client {order.client_id}: {response.text}",
                    error_code=400,
                )

        except requests.Timeout:
            raise PortfolioException(
                user_message="The system was not available or could not be reached.",
                log_message=f"Portfolio service timed out.",
                error_code=504,
            )
        except requests.RequestException as e:
            raise PortfolioException(
                user_message="The system was not available or could not be reached.",
                log_message=f"RequestException for client {order.client_id}: {str(e)}",
                error_code=500,
            )
