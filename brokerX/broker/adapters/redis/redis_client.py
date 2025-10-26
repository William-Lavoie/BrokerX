import json
import logging
from decimal import Decimal
from typing import Optional

from redis import RedisError

from brokerX.redis import redis_client

from ...domain.entities.client import Client

logger = logging.getLogger(__name__)


def redis_set_client(client: Client):
    try:
        client_data_json = json.dumps(
            client.to_dict(),
            default=lambda x: float(x) if isinstance(x, Decimal) else x,
        )
        redis_client.set(f"client:{client.email}", client_data_json)

        logger.info(f"Successfully stored client {client.email} in Redis.")

    except RedisError as re:
        logger.error(f"Redis  error occurred while storing client {client.email}: {re}")


def redis_get_client(email: str) -> Optional[Client]:
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


def redis_update_client_status(email: str, new_status: str):
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
