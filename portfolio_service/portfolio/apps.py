from django.apps import AppConfig
from portfolio.adapters.kafka.order_payment_processed_handler import (
    OrderPaymentProcessedHandler,
)
from portfolio.event_management.handler_registry import HandlerRegistry

from portfolio_service.order_event_consumer import OrderEventConsumer
from portfolio_service.settings import KAFKA_GROUP_ID, KAFKA_HOST, KAFKA_TOPIC


class PortfolioConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "portfolio"

    def ready(self):

        # Register handlers for the Kafka consumer
        registry = HandlerRegistry()
        registry.register(OrderPaymentProcessedHandler())

        # Set up the Kafka consumer
        consumer_service = OrderEventConsumer(
            bootstrap_servers=KAFKA_HOST,
            topic=KAFKA_TOPIC,
            group_id=KAFKA_GROUP_ID,
            registry=registry,
        )

        # Start consuming messages
        consumer_service.start()
