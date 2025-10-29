from decimal import Decimal
from typing import Optional
from uuid import UUID

from order.adapters.dao.mysql_order_dao import MySQLOrderDAO
from order.adapters.redis.redis_order import (
    redis_add_order,
    redis_get_orders,
    redis_get_orders_by_stock,
    redis_set_orders,
)
from order.domain.entities.order import Order
from order.domain.ports.dao.order_dao import OrderDAO
from order.domain.ports.order_repository import OrderDTO, OrderRepository

from order_service.exceptions import DataAccessException


class DjangoOrderRepository(OrderRepository):
    def __init__(self, dao: Optional[OrderDAO] = None):
        super().__init__()
        self.dao: OrderDAO = dao if dao is not None else MySQLOrderDAO()

    def add_order(
        self,
        client_id: UUID,
        symbol: str,
        direction: str,
        initial_quantity: int,
        idempotency_key: UUID,
        limit: Optional[Decimal] = None,
    ) -> Order:
        order_dto: OrderDTO = self.dao.add_order(
            client_id=client_id,
            symbol=symbol,
            direction=direction,
            initial_quantity=initial_quantity,
            idempotency_key=idempotency_key,
            limit=limit,
        )

        if not order_dto.success:
            raise DataAccessException(
                user_message=f"An unexpected error occurred when trying to access {}"
            )

        order = super().get_order_from_dto(order_dto)
        redis_add_order(client_id, order)
        return order

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

    def get_orders_by_client(self, email: str) -> list[Order]:
        redis_orders = redis_get_orders(email=email)
        if redis_orders:
            return redis_orders

        order_dtos = self.dao.get_orders_by_client(email=email)
        for order_dto in order_dtos:
            order_dto.stock = Stock(symbol=order_dto.stock)

        orders = [
            OrderRepository.get_order_from_dto(order_dto) for order_dto in order_dtos
        ]

        redis_set_orders(email=email, orders=orders)
        return orders
