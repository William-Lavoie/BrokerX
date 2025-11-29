import logging
from decimal import Decimal
from typing import Any, Dict
from uuid import UUID

from django.db import transaction
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
        """Execute every time the event is published"""
        order_event_producer = OrderEventProducer()
        try:
            pass
        except Exception as e:

            # Si la mise à jour du stock a échoué, déclenchez StockDecreaseFailed.
            event_data["event"] = "OrdersPaymentFailed"
            event_data["error"] = str(e)
        finally:
            order_event_producer.get_instance().send(KAFKA_TOPIC, value=event_data)
