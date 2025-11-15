import logging
import threading
from decimal import Decimal
from typing import Optional
from uuid import UUID

from order.domain.entities.order import Order, OrderInvalidException
from order.domain.ports.order_repository import OrderRepository

from order_service.exceptions import DataAccessException
from order_service.use_case_results import UseCaseResult

logger = logging.getLogger("order")


class PlaceOrderUseCaseResult(UseCaseResult):
    def __init__(
        self,
        message: str,
        code: int,
        orders: Optional[list[Order]] = None,
    ):
        super().__init__(message=message, code=code)
        self.orders: Optional[list[Order]] = orders

    def to_dict(self):
        data = super().to_dict()
        if self.orders is not None:
            data["orders"] = [order.to_dict() for order in self.orders]
        else:
            data["orders"] = []
        return data


class PlaceOrderUseCase:
    def __init__(
        self,
        order_repository: OrderRepository,
    ):
        self.order_repository = order_repository

    def execute(
        self,
        client_id: UUID,
        symbol: str,
        order_type: str,
        order_style: str,
        order_duration: str,
        quantity: int,
        idempotency_key: UUID,
        price: Optional[Decimal] = None,
        end_date: Optional[str] = None,
    ) -> PlaceOrderUseCaseResult:

        try:
            order = Order(
                client_id=client_id,
                symbol=symbol,
                order_type=order_type,
                order_style=order_style,
                order_duration=order_duration,
                quantity=quantity,
                price=price,
                end_date=end_date,
            )

            # TODO: call wallet
            # TODO: call stocks

            self.order_repository.add_order(
                order=order, idempotency_key=idempotency_key
            )
            return PlaceOrderUseCaseResult(
                message="The order was placed successfully.",
                code=201,
                orders=[order],
            )

        except OrderInvalidException as order_invalid_exception:
            logger.error(
                f"OrderInvalidException in PlaceOrderUseCase for client_id {client_id}: {order_invalid_exception.log_message}",
                exc_info=True,
            )
            return PlaceOrderUseCaseResult(
                message=order_invalid_exception.user_message,
                code=order_invalid_exception.error_code,
            )

        except DataAccessException as data_access_exception:
            return PlaceOrderUseCaseResult(
                message=data_access_exception.user_message,
                code=data_access_exception.error_code,
            )

    def get_orders(self, client_id: str):
        try:
            orders = self.order_repository.get_orders_by_client(client_id=client_id)
            return PlaceOrderUseCaseResult(
                code=200,
                message="Orders fetched successfully",
                orders=orders,
            )

        except DataAccessException as data_access_exception:
            return PlaceOrderUseCaseResult(
                success=False,
                message=data_access_exception.user_message,
                code=data_access_exception.error_code,
            )
