import json
import logging
from decimal import Decimal
from typing import Optional

from redis import RedisError

from client_service.redis import redis_client

from ...domain.entities.client import Client

logger = logging.getLogger("redis")

class RedisClient():
    def set_client(self, client: Client) -> None:
        try:
            client_data_json = json.dumps(
                client.to_dict(),
                default=lambda x: float(x) if isinstance(x, Decimal) else x,
            )
            redis_client.set(f"client:{client.email}", client_data_json)

            logger.info(f"Successfully stored client {client.email} in Redis.")

        except RedisError as re:
            logger.error(f"Redis  error occurred while storing client {client.email}: {re}")


    def get_client(self, email: str) -> Optional[Client]:
        try:
            client_json = redis_client.get(f"client:{email}")

            if client_json:
                client_dict = json.loads(client_json.decode())
                logger.error("REDIS WORKS")
                return Client.from_dict(client_dict)
            else:
                return None

        except RedisError as re:
            logger.error(f"Redis error occurred while fetching client {email}: {re}")


    def update_client_status(self, email: str, new_status: str) -> None:
        try:
            client_json = redis_client.get(f"client:{email}")

            if client_json:
                client_dict = json.loads(client_json.decode())
                client_dict["status"] = new_status

                client_data_json = json.dumps(
                    client_dict, default=lambda x: float(x) if isinstance(x, Decimal) else x
                )
                redis_client.set(f"client:{email}", client_data_json)
            else:
                return None

        except RedisError as re:
            logger.error(f"Redis error occurred while updating client {email}: {re}")
