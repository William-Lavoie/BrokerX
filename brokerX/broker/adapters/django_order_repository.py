from decimal import Decimal
from typing import Optional
from uuid import UUID

from ..adapters.dao.mysql_order_dao import MySQLOrderDAO
from ..domain.entities.client import Client
from ..domain.entities.order import Order
from ..domain.entities.stock import Stock
from ..domain.ports.dao.order_dao import OrderDAO
from ..domain.ports.order_repository import OrderDTO, OrderRepository
from ..exceptions import DataAccessException


class DjangoOrderRepository(OrderRepository):
    def __init__(self, dao: Optional[OrderDAO] = None):
        super().__init__()
        self.dao: OrderDAO = dao if dao is not None else MySQLOrderDAO()

    def add_order(
        self,
        client: Client,
        stock: Stock,
        direction: str,
        initial_quantity: int,
        idempotency_key: UUID,
        limit: Optional[Decimal] = None,
    ) -> Order:
        order_dto: OrderDTO = self.dao.add_order(
            email=client.email,
            symbol=stock.symbol,
            direction=direction,
            initial_quantity=initial_quantity,
            idempotency_key=idempotency_key,
            limit=limit,
        )

        if not order_dto.success:
            raise DataAccessException(
                user_message=f"An unexpected error occurred when trying to access {stock.symbol}"
            )

        order_dto.stock = stock
        order_dto.client = client
        return super().get_order_from_dto(order_dto)

    def find_matching_orders(self, order: Order) -> list[OrderDTO]:
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
        order_dtos = self.dao.get_orders_by_client(email=email)
        for order_dto in order_dtos:
            order_dto.stock = Stock(symbol=order_dto.stock)

        return [
            OrderRepository.get_order_from_dto(order_dto) for order_dto in order_dtos
        ]
