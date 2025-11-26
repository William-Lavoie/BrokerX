import logging
from typing import Any, Dict
from uuid import UUID

from order.adapters.kafka.order_event_producer import OrderEventProducer
from order.event_management.base_handler import EventHandler

from order_service.settings import KAFKA_TOPIC

logger = logging.getLogger("order")


class OrderCreatedHandler(EventHandler):
    """Handles OrderCreated events"""

    def __init__(self):
        self.order_producer = OrderEventProducer()
        super().__init__()

    def get_event_type(self) -> str:
        """Get event type name"""
        return "OrderCreated"

    def handle(self, event_data: Dict[str, Any]) -> None:
        """Execute every time the event is published"""
        from order.services.order_matching import OrderMatchingUseCase

        try:
            logger.error(f"Handling OrderCreated event: {event_data}")

            result = OrderMatchingUseCase().execute(
                client_id=UUID(event_data["client_id"]),
                symbol=event_data["symbol"],
                order_type=event_data["order_type"],
                order_style=event_data["order_style"],
                order_duration=event_data["order_duration"],
                quantity=event_data["quantity"],
                idempotency_key=UUID(event_data["order_id"]),
                price=event_data.get("price"),
                end_date=event_data.get("end_date"),
            )

            event_data = result.event_data

            if event_data["orders_matched"] == []:
                event_data["event"] = "OrderExecutionCompleted"
            else:
                event_data["event"] = "OrderExecutionMatched"

        except Exception as e:
            event_data["event"] = "OrderExecutionCompleted"
        finally:
            self.order_producer.get_instance().send(KAFKA_TOPIC, value=event_data)
