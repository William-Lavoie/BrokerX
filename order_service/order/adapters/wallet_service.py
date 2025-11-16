import requests
from order.domain.entities.order import Order
from order.domain.ports.wallet_repository import WalletRepository


class WalletService(WalletRepository):
    def reserve_funds(self, order: Order) -> None:
        response = requests.post(
            "http://wallet-service/reserve",
            json={
                "client_id": str(order.client_id),
                "amount": float(10.0),
                "order_id": str(order.order_id),
            },
        )
