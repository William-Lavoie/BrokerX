import logging

import requests
from order.domain.entities.order import Order
from order.domain.ports.wallet_repository import WalletException, WalletRepository

logger = logging.getLogger("order")


class WalletService(WalletRepository):
    def reserve_funds(self, order: Order) -> int:
        response = requests.post(
            "http://wallet-app:8003/wallet/reserve",
            json={
                "client_id": str(order.client_id),
                "amount": float(1000000.0),
                "order_id": str(order.order_id),
            },
        )

        if response.status_code != 200:
            raise WalletException(
                user_message=response.json().get(
                    "message", "An unexpected error occured."
                ),
                log_message=f"WalletException for client {order.client_id}: {response.text}",
                error_code=400,
            )

        return response.status_code
