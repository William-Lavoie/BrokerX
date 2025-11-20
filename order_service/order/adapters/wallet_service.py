import logging
from uuid import UUID

import requests
from order.domain.entities.order import Order
from order.domain.ports.wallet_repository import WalletException, WalletRepository

logger = logging.getLogger("order")


class WalletService(WalletRepository):
    def reserve_funds(self, order: Order) -> None:
        try:
            response = requests.post(
                "http://wallet-app:8003/wallet/reserve",
                json={
                    "client_id": str(order.client_id),
                    "amount": str(order.price*order.quantity),
                    "order_id": str(order.order_id),
                },
                timeout=5.0
            )

            if response.status_code != 200:
                raise WalletException(
                    user_message=response.json().get(
                        "message", "An unexpected error occured."
                    ),
                    log_message=f"WalletException for client {order.client_id}: {response.text}",
                    error_code=400,
                )
            
        except requests.Timeout:
            raise WalletException(
                user_message="The system was not available or could not be reached.",
                log_message=f"Wallet service timed out.",
                error_code=504,
            )
        
        except requests.RequestException as e:
            raise WalletException(
                user_message="The system was not available or could not be reached.",
                log_message=f"RequestException for client {order.client_id}: {str(e)}",
                error_code=500,
            )
        
    def release_funds(self, order_id: UUID, client_id: UUID) -> None:
        try:
            response = requests.delete(
                "http://wallet-app:8003/wallet/reserve",
                json={
                    "client_id": str(client_id),
                    "order_id": str(order_id),
                },
                timeout=5.0
            )

            if response.status_code != 200:
                raise WalletException(
                    user_message=response.json().get(
                        "message", "An unexpected error occured."
                    ),
                    log_message=f"WalletException for client {client_id}: {response.text}",
                    error_code=500,
                )
            
        except requests.Timeout:
            raise WalletException(
                user_message="The system was not available or could not be reached.",
                log_message=f"Wallet service timed out.",
                error_code=504,
            )
        
        except requests.RequestException as e:
            raise WalletException(
                user_message="The system was not available or could not be reached.",
                log_message=f"RequestException for client {client_id}: {str(e)}",
                error_code=500,
            )