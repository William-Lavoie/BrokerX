import logging
from decimal import Decimal
from typing import Optional

from redis import RedisError

from brokerX.redis import redis_client

from ...domain.entities.client import Client

logger = logging.getLogger(__name__)


def redis_set_wallet_balance(email: str, balance: Decimal):
    try:
        redis_client.set(f"balance:{email}", str(balance))

        logger.info(f"Successfully stored balance for {email} in Redis.")

    except RedisError as re:
        logger.error(f"Redis  error occurred while storing balance for {email}: {re}")


def redis_get_wallet_balance(email: str) -> Optional[Decimal]:
    try:
        data = redis_client.get(f"balance:{email}")
        balance = Decimal(data.decode("utf-8"))

        if balance:
            logger.error(f"Successfully fetched balance for {email} in Redis.")
            return Decimal(balance)
        else:
            return None

    except RedisError as re:
        logger.error(f"Redis error occurred while fetching balance for {email}: {re}")
