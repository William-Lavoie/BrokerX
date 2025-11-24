import logging
from typing import Any, Dict

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
        order_event_producer = OrderEventProducer()
        try:
            logger.error(f"Handling OrderCreated event: {event_data}")

            event_data["event"] = "StockDecreased"
        except Exception as e:

            # Si la mise à jour du stock a échoué, déclenchez StockDecreaseFailed.
            event_data["event"] = "StockDecreaseFailed"
            event_data["error"] = str(e)
        finally:
            order_event_producer.get_instance().send(KAFKA_TOPIC, value=event_data)
