from typing import Optional
from uuid import UUID

from django.db import transaction
from order.adapters.dao.mysql_order_dao import MySQLOrderDAO
from order.adapters.redis.redis_order import RedisOrder
from order.domain.entities.order import Order, OrderDTO
from order.domain.ports.dao.order_dao import OrderDAO
from order.domain.ports.order_repository import OrderRepository

from order_service.exceptions import DataAccessException


class DjangoOrderRepository(OrderRepository):
    def __init__(self, dao: Optional[OrderDAO] = None, redis=None):
        super().__init__()
        self.dao: OrderDAO = dao if dao is not None else MySQLOrderDAO()
        self.redis = redis if redis is not None else RedisOrder()

    def add_order(self, order: Order, idempotency_key: UUID) -> None:
        with transaction.atomic():
            order_dto: OrderDTO = self.dao.add_order(
                client_id=order.client_id,
                symbol=order.symbol,
                order_type=order.order_type,
                order_style=order.order_style,
                order_duration=order.order_duration,
                quantity=order.quantity,
                idempotency_key=idempotency_key,
                price=order.price,
                end_date=order.end_date,
            )

            if not order_dto.success:
                raise DataAccessException(
                    user_message=f"An unexpected error occurred when trying to place the order."
                )

            order.update_from_dto(order_dto=order_dto)
            self.redis.set_order(order.client_id, order)

    def find_matching_orders(self, order: Order) -> list[OrderDTO]:
        redis_orders = redis_get_orders_by_stock(order.stock.symbol)
        if redis_orders:
            return redis_orders

        matching_order_dtos = self.dao.find_matching_orders(
            email=order.client.email,
            symbol=order.stock.symbol,
            direction=order.direction,
            limit=order.limit,
        )

        return [
            super().get_order_from_dto(order_dto) for order_dto in matching_order_dtos
        ]

    def get_orders_by_client(self, client_id: UUID) -> list[Order]:
        redis_orders = self.redis.get_orders_by_client(client_id=client_id)
        if redis_orders:
            return redis_orders

        order_dtos = self.dao.get_orders_by_client(client_id=client_id)

        orders = [
            OrderRepository.get_order_from_dto(order_dto) for order_dto in order_dtos
        ]

        self.redis.set_orders_by_client(client_id=client_id, orders=orders)
        return orders
