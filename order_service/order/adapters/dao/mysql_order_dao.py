import json
import logging
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from django.utils import timezone
from order.domain.entities.order import Order as OrderEntity
from order.domain.entities.order import OrderDTO
from order.domain.ports.dao.order_dao import OrderDAO
from order.models import Order as OrderModel
from order.models import OrderAudit, OrderExecution

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
                order = OrderModel.objects.filter(order_id=idempotency_key).first()

                if not order:
                    order = OrderModel(
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
                if created:
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

    def get_orders_by_client(self, client_id: UUID) -> list[OrderDTO]:
        orders = OrderModel.objects.filter(client_id=client_id).exclude(
            status="CANCELLED"
        )
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

    def delete_order(self, client_id: UUID, order_id: UUID) -> OrderDTO:
        try:
            order = OrderModel.objects.get(order_id=order_id, client_id=client_id)

            if order.status in ["EXECUTED", "REJECTED", "CANCELLED"]:
                return OrderDTO(success=False, code=400)

            order.status = "CANCELLED"
            order.save()

            order_dto = OrderDTO(
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

            OrderAudit.objects.create(
                order=order,
                action="ORDER_CANCELLED",
                metadata=json.dumps(order_dto.to_dict()),
            )

            return order_dto

        except ObjectDoesNotExist as e:
            logger.error(
                f"ObjectDoesNotExist exception : {e}",
                exc_info=True,
            )
            return OrderDTO(success=False, code=404)

    def delete_order_rollback(
        self, client_id: UUID, order_id: UUID, previous_status: str
    ) -> None:
        OrderModel.objects.filter(
            order_id=order_id, client_id=client_id, status="CANCELLED"
        ).update(status=previous_status)

    def get_potential_matches(self, order: OrderEntity) -> list[OrderDTO]:
        with transaction.atomic():
            orders = OrderModel.objects.filter(
                stock_symbol=order.symbol,
                order_type=("SELL" if order.order_type == "BUY" else "BUY"),
                status="PENDING" or "PARTIALLY_EXECUTED",
            ).exclude(client_id=order.client_id)
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

    def execute_order(
        self, order: OrderEntity, matching_orders: list[OrderEntity]
    ) -> dict:
        try:
            orders_matched = {}
            with transaction.atomic():

                for match in matching_orders:
                    trade_quantity = min(
                        order.quantity - order.quantity_executed,
                        match.quantity - match.quantity_executed,
                    )

                    order.quantity_executed += trade_quantity
                    match.quantity_executed += trade_quantity

                    if match.quantity_executed == match.quantity:
                        match.status = "EXECUTED"
                        match.executed_at = timezone.now()
                    else:
                        match.status = "PARTIALLY_EXECUTED"

                    if order.quantity_executed == order.quantity:
                        order.status = "EXECUTED"
                        order.executed_at = timezone.now()
                    else:
                        order.status = "PARTIALLY_EXECUTED"

                    match.updated_at = timezone.now()
                    order.updated_at = timezone.now()

                    orders_matched[str(match.order_id)] = {
                        "trade_quantity": trade_quantity,
                        "price": str(match.price) if match.price is not None else None,
                    }

                    matched_order = OrderModel.objects.get(order_id=match.order_id)
                    matched_order.quantity_executed = match.quantity_executed
                    matched_order.status = match.status
                    matched_order.executed_at = match.executed_at
                    matched_order.updated_at = match.updated_at
                    matched_order.save()

                    order_instance = OrderModel.objects.get(order_id=order.order_id)
                    order_instance.quantity_executed = order.quantity_executed
                    order_instance.status = order.status
                    order_instance.executed_at = order.executed_at
                    order_instance.updated_at = order.updated_at
                    order_instance.save()

                    execution = OrderExecution.objects.create(
                        quantity=trade_quantity,
                        price=match.price,
                        buyer_client_id=(
                            order.client_id
                            if order.order_type == "BUY"
                            else match.client_id
                        ),
                        seller_client_id=(
                            order.client_id
                            if order.order_type == "SELL"
                            else match.client_id
                        ),
                    )
                    execution.orders.set([order_instance, matched_order])

            return orders_matched

        except ObjectDoesNotExist as e:
            logger.error(
                f"ObjectDoesNotExist exception : {e}",
                exc_info=True,
            )
            return {}
