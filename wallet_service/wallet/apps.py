from django.apps import AppConfig
from wallet.adapters.kafka.order_executed_handler import OrderExecutedHandler
from wallet.event_management.handler_registry import HandlerRegistry

from wallet_service.order_event_consumer import OrderEventConsumer
from wallet_service.settings import KAFKA_GROUP_ID, KAFKA_HOST, KAFKA_TOPIC


class WalletConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wallet"

    def ready(self):

        # Register handlers for the Kafka consumer
        registry = HandlerRegistry()
        registry.register(OrderExecutedHandler())

        # Set up the Kafka consumer
        consumer_service = OrderEventConsumer(
            bootstrap_servers=KAFKA_HOST,
            topic=KAFKA_TOPIC,
            group_id=KAFKA_GROUP_ID,
            registry=registry,
        )

        # Start consuming messages
        consumer_service.start()
