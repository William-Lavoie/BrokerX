import logging
from decimal import Decimal
from typing import Optional
from uuid import UUID

from redis import RedisError

from wallet_service.redis import redis_client

logger = logging.getLogger("redis")


class RedisWallet:
    def set_wallet_balance(self, client_id: UUID, balance: Decimal) -> None:
        try:
            redis_client.set(f"balance:{client_id}", str(balance))

            logger.info(f"Successfully stored balance for {client_id} in Redis.")

        except RedisError as re:
            logger.error(
                f"Redis  error occurred while storing balance for {client_id}: {re}"
            )

    def get_wallet_balance(self, client_id: UUID) -> Optional[Decimal]:
        try:
            data = redis_client.get(f"balance:{client_id}")

            if data:
                balance = Decimal(data.decode("utf-8"))

                logger.error(f"Successfully fetched balance for {client_id} in Redis.")
                return Decimal(balance)
            else:
                return None

        except RedisError as re:
            logger.error(
                f"Redis error occurred while fetching balance for {client_id}: {re}"
            )
            return None
