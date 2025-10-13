import logging
from abc import abstractmethod
from decimal import Decimal
from typing import Optional
from uuid import UUID

from django.db import IntegrityError, transaction

from ...domain.ports.dao.order_dao import OrderDAO
from ...domain.ports.order_repository import OrderDTO
from ...models import Client, Order, Stock

logger = logging.getLogger(__name__)


class MySQLOrderDAO(OrderDAO):
    def add_order(
        self,
        email: str,
        symbol: str,
        type: str,
        initial_quantity: int,
        idempotency_key: UUID,
        limit: Optional[Decimal],
    ) -> OrderDTO:
        try:
            direction: str = type
            model_type: str = "M" if limit is None else "L"

            client = Client.objects.get(email=email)
            stock = Stock.objects.get(symbol=symbol)

            with transaction.atomic():
                order, created = Order.objects.get_or_create(
                    client=client,
                    order_id=idempotency_key,
                    defaults={
                        "direction": direction,
                        "type": model_type,
                        "stock": stock,
                        "initial_quantity": initial_quantity,
                        "remaining_quantity": initial_quantity,
                        "limit": limit,
                    },
                )
                return OrderDTO(
                    success=True,
                    code=200,
                    type=order.type,
                    limit=order.limit,
                    initial_quantity=order.initial_quantity,
                    remaining_quantity=order.remaining_quantity,
                )

        except IntegrityError as e:
            logger.error(
                f"IntegrityError exception : {e}",
                exc_info=True,
            )
            return OrderDTO(success=False, code=500)
