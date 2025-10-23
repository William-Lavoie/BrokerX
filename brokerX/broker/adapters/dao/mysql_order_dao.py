import logging
from abc import abstractmethod
from decimal import Decimal
from typing import Optional
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
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
        direction: str,
        initial_quantity: int,
        idempotency_key: UUID,
        limit: Optional[Decimal] = None,
    ) -> OrderDTO:
        try:
            type: str = "M" if limit is None else "L"

            client = Client.objects.get(email=email)
            stock = Stock.objects.get(symbol=symbol)

            with transaction.atomic():
                order, created = Order.objects.get_or_create(
                    order_id=idempotency_key,
                    defaults={
                        "direction": direction,
                        "client": client,
                        "type": type,
                        "stock": stock,
                        "initial_quantity": initial_quantity,
                        "remaining_quantity": initial_quantity,
                        "limit": limit,
                    },
                )
                return OrderDTO(
                    success=True,
                    code=200,
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
        self, email: str, symbol: str, direction: str, quantity: int, limit: Decimal
    ):
        try:
            new_direction = "B" if direction == "sell" else "S"

            with transaction.atomic():
                orders = Order.objects.filter(
                    symbol=symbol, direction=new_direction
                ).exclude(email=email)
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
        
    def get_orders_by_client(self, email: str) -> list[OrderDTO]:
        try:
            orders = Order.objects.filter(client__email=email)
            return [
                OrderDTO(
                    success=True,
                    code=200,
                    direction=order.direction,
                    limit=order.limit,
                    initial_quantity=order.initial_quantity,
                    remaining_quantity=order.remaining_quantity,
                    order_id=order.order_id,
                    stock=order.stock.symbol
                )
                for order in orders
            ]

        except ObjectDoesNotExist as e:
            logger.error(
                f"ObjectDoesNotExist exception : {e}",
                exc_info=True,
            )
            return OrderDTO(success=False, code=404)
