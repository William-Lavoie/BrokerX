import json
import logging
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from order.domain.entities.order import OrderDTO
from order.domain.ports.dao.order_dao import OrderDAO
from order.models import Order, OrderAudit

logger = logging.getLogger("mysql")


class MySQLOrderDAO(OrderDAO):
    def add_order(
        self,
        client_id: UUID,
        symbol: str,
        order_type: str,
        order_style: str,
        order_duration: str,
        quantity: int,
        idempotency_key: UUID,
        end_date: Optional[datetime] = None,
        price: Optional[Decimal] = None,
    ) -> OrderDTO:
        try:
            with transaction.atomic():
                created = False
                order = Order.objects.filter(order_id=idempotency_key).first()

                if not order:
                    order = Order(
                        order_id=idempotency_key,
                        client_id=client_id,
                        stock_symbol=symbol,
                        order_type=order_type,
                        order_style=order_style,
                        order_duration=order_duration,
                        quantity=quantity,
                        price=price,
                        order_end_date=end_date,
                    )
                    created = True
                    order.full_clean()
                    order.save()

                code = 201 if created else 200
                order_dto = OrderDTO(
                    success=True,
                    code=code,
                    order_id=order.order_id,
                    client_id=order.client_id,
                    symbol=order.stock_symbol,
                    order_type=order.order_type,
                    order_style=order.order_style,
                    order_duration=order.order_duration,
                    quantity=order.quantity,
                    quantity_executed=order.quantity_executed,
                    price=order.price,
                    end_date=order.order_end_date,
                    status=order.status,
                    created_at=order.created_at,
                    updated_at=order.updated_at,
                    executed_at=order.executed_at,
                )

                OrderAudit.objects.create(
                    order=order,
                    action="ORDER_PLACED",
                    metadata=json.dumps(order_dto.to_dict()),
                )

                return order_dto

        except ValidationError as e:
            logger.error(
                "ValidationError occurred while adding order for client {client_id}.",
                exc_info=True,
            )
            return OrderDTO(success=False, code=400)

        except Exception as e:
            logger.error(
                f"Exception occurred while adding order for client {client_id}: {e}",
                exc_info=True,
            )
            return OrderDTO(success=False, code=500)

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
                    order_id=order.order_id,
                    client_id=order.client_id,
                    symbol=order.stock_symbol,
                    order_type=order.order_type,
                    order_style=order.order_style,
                    order_duration=order.order_duration,
                    quantity=order.quantity,
                    quantity_executed=order.quantity_executed,
                    price=order.price,
                    end_date=order.order_end_date,
                    status=order.status,
                    created_at=order.created_at,
                    updated_at=order.updated_at,
                    executed_at=order.executed_at,
                )
                for order in orders
            ]

        except ObjectDoesNotExist as e:
            logger.error(
                f"ObjectDoesNotExist exception : {e}",
                exc_info=True,
            )
            return OrderDTO(success=False, code=404)
