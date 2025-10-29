import logging
from decimal import Decimal
from typing import Optional
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from order.domain.ports.dao.order_dao import OrderDAO
from order.domain.ports.order_repository import OrderDTO
from order.models import Order

logger = logging.getLogger("mysql")


class MySQLOrderDAO(OrderDAO):
    def add_order(
        self,
        client_id: UUID,
        symbol: str,
        direction: str,
        initial_quantity: int,
        idempotency_key: UUID,
        limit: Optional[Decimal] = None,
    ) -> OrderDTO:
        try:
            with transaction.atomic():
                order, created = Order.objects.get_or_create(
                    order_id=idempotency_key,
                    defaults={
                        "direction": direction,
                        "client_id": client_id,
                        "symbol": symbol,
                        "initial_quantity": initial_quantity,
                        "remaining_quantity": initial_quantity,
                        "limit": limit,
                    },
                )

                code = 200 if created else 201
                return OrderDTO(
                    success=True,
                    code=code,
                    direction=order.direction,
                    limit=order.limit,
                    initial_quantity=order.initial_quantity,
                    remaining_quantity=order.remaining_quantity,
                )

        except ObjectDoesNotExist as e:
            logger.error(
                f"ObjectDoesNotExist exception : {e}",
                exc_info=True,
            )
            return OrderDTO(success=False, code=404)

    def find_matching_orders(
        self,
        client_id: UUID,
        symbol: str,
        direction: str,
        quantity: int,
        limit: Decimal,
    ):
        try:
            new_direction = "B" if direction == "sell" else "S"

            with transaction.atomic():
                orders = Order.objects.filter(
                    symbol=symbol, direction=new_direction
                ).exclude(client_id=client_id)
                return [
                    OrderDTO(
                        success=True,
                        code=200,
                        direction=order.direction,
                        limit=order.limit,
                        initial_quantity=order.initial_quantity,
                        remaining_quantity=order.remaining_quantity,
                        order_id=order.order_id,
                    )
                    for order in orders
                ]

        except ObjectDoesNotExist as e:
            logger.error(
                f"ObjectDoesNotExist exception : {e}",
                exc_info=True,
            )
            return OrderDTO(success=False, code=404)

    def get_orders_by_client(self, client_id: UUID) -> list[OrderDTO]:
        try:
            orders = Order.objects.filter(client_id=client_id)
            return [
                OrderDTO(
                    success=True,
                    code=200,
                    direction=order.direction,
                    limit=order.limit,
                    initial_quantity=order.initial_quantity,
                    remaining_quantity=order.remaining_quantity,
                    order_id=order.order_id,
                )
                for order in orders
            ]

        except ObjectDoesNotExist as e:
            logger.error(
                f"ObjectDoesNotExist exception : {e}",
                exc_info=True,
            )
            return OrderDTO(success=False, code=404)
