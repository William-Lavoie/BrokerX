import logging
from decimal import Decimal
from typing import Any, Dict
from uuid import UUID

from portfolio.adapters.kafka.order_event_producer import OrderEventProducer
from portfolio.event_management.base_handler import EventHandler

from portfolio_service.settings import KAFKA_TOPIC

logger = logging.getLogger("portfolio")


class OrderPaymentProcessedHandler(EventHandler):
    """Handles OrderPaymentProcessed events"""

    def __init__(self):
        self.order_producer = OrderEventProducer()
        super().__init__()

    def get_event_type(self) -> str:
        """Get event type name"""
        return "OrderPaymentProcessed"

    def handle(self, event_data: Dict[str, Any]) -> None:
        from portfolio.services.process_exchange_use_case import ProcessExchangeUseCase

        """Execute every time the event is published"""
        order_event_producer = OrderEventProducer()
        try:

            logger.info(f"Handling OrderPaymentProcessed event: {event_data}")

            if (
                not "order" in event_data
                or not "orders_matched" in event_data
                or not "matching_orders" in event_data
            ):
                event_data["event"] = "OrdersPaymentFailed"
                return

            order = event_data.get("order", {})

            acquisitions = []
            transfers = []

            if order.get("order_type") == "BUY":

                buying_price = 0
                total_quantity = 0
                for order_matched in event_data.get("orders_matched", {}).values():
                    buying_price += Decimal(order_matched.get("price", 0)) * int(
                        order_matched.get("trade_quantity", 0)
                    )
                    total_quantity += int(order_matched.get("trade_quantity", 0))

                if total_quantity > 0:
                    buying_price = buying_price / total_quantity

                acquisitions.append(
                    {
                        "client_id": UUID(order.get("client_id")),
                        "symbol": order.get("symbol"),
                        "quantity": total_quantity,
                        "buying_price": buying_price,
                        "name": order.get("name"),
                        "current_price": (
                            Decimal(order.get("current_price"))
                            if order.get("current_price")
                            else None
                        ),
                    }
                )

                transfers = [
                    {
                        "client_id": UUID(matched_order.get("client_id")),
                        "symbol": matched_order.get("symbol"),
                        "quantity": int(
                            event_data.get("orders_matched")
                            .get(matched_order.get("order_id"))
                            .get("trade_quantity", 0)
                        ),
                    }
                    for matched_order in event_data.get("matching_orders", [])
                ]

            else:  # SELL order
                transfers.append(
                    {
                        "client_id": UUID(order.get("client_id")),
                        "symbol": order.get("symbol"),
                        "quantity": int(order.get("quantity")),
                    }
                )

                acquisitions = [
                    {
                        "client_id": UUID(matched_order.get("client_id")),
                        "symbol": matched_order.get("symbol"),
                        "quantity": int(
                            event_data.get("orders_matched")
                            .get(matched_order.get("order_id"))
                            .get("trade_quantity", 0)
                        ),
                        "buying_price": Decimal(
                            event_data.get("orders_matched")
                            .get(matched_order.get("order_id"))
                            .get("price", 0)
                        ),
                        "name": matched_order.get("name"),
                        "current_price": (
                            Decimal(matched_order.get("current_price"))
                            if matched_order.get("current_price")
                            else None
                        ),
                    }
                    for matched_order in event_data.get("matching_orders", [])
                ]

            ProcessExchangeUseCase().process_acquisitions(
                orders_info=acquisitions,
            )
            ProcessExchangeUseCase().process_transfers(
                orders_info=transfers,
            )

            event_data["event"] = "OrderHoldingsExchanged"
        except Exception as e:

            logger.error(
                f"Error processing OrderPaymentProcessed event: {e}", exc_info=True
            )

            # Si la mise à jour du stock a échoué, déclenchez StockDecreaseFailed.
            event_data["event"] = "OrdersPaymentFailed"
            event_data["error"] = str(e)
        finally:
            logger.info(f"Publishing event to Kafka topic {KAFKA_TOPIC}: {event_data}")
            order_event_producer.get_instance().send(KAFKA_TOPIC, value=event_data)
