import logging
from decimal import Decimal
from typing import Any, Dict
from uuid import UUID

from django.db import transaction
from wallet.adapters.kafka.order_event_producer import OrderEventProducer
from wallet.event_management.base_handler import EventHandler

from wallet_service.settings import KAFKA_TOPIC

logger = logging.getLogger("wallet")


class OrderExecutedHandler(EventHandler):
    """Handles OrderExecuted events"""

    def __init__(self):
        self.order_producer = OrderEventProducer()
        super().__init__()

    def get_event_type(self) -> str:
        """Get event type name"""
        return "OrderExecuted"

    def handle(self, event_data: Dict[str, Any]) -> None:
        from wallet.services.process_payment_use_case import ProcessPaymentUseCase

        """Execute every time the event is published"""
        order_event_producer = OrderEventProducer()
        try:
            logger.error(f"Handling OrderExecuted event: {event_data}")

            if (
                not "order" in event_data
                or not "orders_matched" in event_data
                or not "matching_orders" in event_data
            ):
                event_data["event"] = "OrdersPaymentFailed"
                return

            order = event_data.get("order", {})

            payments = []
            transfers = []

            # Calculate the total price
            total_price = Decimal("0.00")
            orders_matched = event_data.get("orders_matched", {})
            for transaction_info in orders_matched.values():
                try:
                    trade_quantity = Decimal(transaction_info.get("trade_quantity", 0))
                    price = Decimal(transaction_info.get("price", 0))
                    total_price += trade_quantity * price
                except (ValueError, TypeError) as e:
                    logger.error(
                        f"Error processing transaction_info: {transaction_info}. Error: {e}"
                    )

            # Determine payments and transfers based on order type
            if order.get("order_type") == "BUY":
                # For BUY order, the payment is for the buyer
                payments = [
                    {
                        "order_id": UUID(order["order_id"]),
                        "client_id": UUID(order["client_id"]),
                        "amount": total_price,
                    }
                ]

                transfers = [
                    {
                        "client_id": UUID(matching_order["client_id"]),
                        "amount": Decimal(matching_order.get("quantity", 0))
                        * Decimal(matching_order.get("price", 0)),
                    }
                    for matching_order in event_data.get("matching_orders", [])
                ]

            elif order.get("order_type") == "SELL":
                # For SELL order, the transfer is for the seller
                transfers = [
                    {"client_id": UUID(order["client_id"]), "amount": total_price}
                ]

                # For matching orders, payment is to the seller
                payments = [
                    {
                        "order_id": UUID(matching_order["order_id"]),
                        "client_id": UUID(matching_order["client_id"]),
                        "amount": Decimal(
                            orders_matched.get(matching_order["order_id"], {}).get(
                                "quantity", 0
                            )
                        )
                        * Decimal(
                            orders_matched.get(matching_order["order_id"], {}).get(
                                "price", 0
                            )
                        ),
                    }
                    for matching_order in event_data.get("matching_orders", [])
                ]

            if payments and transfers:
                with transaction.atomic():
                    # Process payments and transfers within an atomic transaction
                    ProcessPaymentUseCase().process_transfers(orders_info=transfers)
                    ProcessPaymentUseCase().process_payments(orders_info=payments)

            # Set event type after processing
            event_data["event"] = "OrderPaymentProcessed"

        except Exception as e:

            # Si la mise à jour du stock a échoué, déclenchez StockDecreaseFailed.
            event_data["event"] = "OrdersPaymentFailed"
            event_data["error"] = str(e)
        finally:
            order_event_producer.get_instance().send(KAFKA_TOPIC, value=event_data)
