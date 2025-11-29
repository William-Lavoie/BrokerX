"""
Kafka order event producer
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import json
import logging

from kafka import KafkaProducer
from portfolio_service.singleton import Singleton

logger = logging.getLogger("wallet")


class OrderEventProducer(metaclass=Singleton):

    def __init__(self, kafka_host="kafka:9092"):
        """Initialize KafkaProducer"""
        self.kafka_host = kafka_host
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.kafka_host,
                value_serializer=lambda dict: json.dumps(dict).encode("utf-8"),
            )

        except Exception as e:
            logger.error(f"Failed to initialize Kafka producer: {e}")
            raise

    def get_instance(self):
        return self.producer
