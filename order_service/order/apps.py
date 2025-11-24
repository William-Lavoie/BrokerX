import logging

from django.apps import AppConfig
from order.adapters.kafka.order_created_handler import OrderCreatedHandler
from order.event_management.handler_registry import HandlerRegistry

from order_service.order_event_consumer import OrderEventConsumer
from order_service.settings import KAFKA_GROUP_ID, KAFKA_HOST, KAFKA_TOPIC

logger = logging.getLogger("order")


class OrderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "order"

    def ready(self):

        # Register handlers for the Kafka consumer
        registry = HandlerRegistry()
        registry.register(OrderCreatedHandler())

        # Set up the Kafka consumer
        consumer_service = OrderEventConsumer(
            bootstrap_servers=KAFKA_HOST,
            topic=KAFKA_TOPIC,
            group_id=KAFKA_GROUP_ID,
            registry=registry,
        )

        # Start consuming messages
        consumer_service.start()
