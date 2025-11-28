import logging
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from order.adapters.django_order_repository import DjangoOrderRepository
from order.domain.entities.order import Order, OrderInvalidException

from order_service.exceptions import DataAccessException
from order_service.use_case_results import UseCaseResult

logger = logging.getLogger("order")


class OrderMatchingUseCaseResult(UseCaseResult):
    def __init__(
        self,
        message: str,
        code: int,
        orders: Optional[list[Order]] = None,
        event_data: Optional[dict] = None,
    ):
        super().__init__(message=message, code=code)
        self.orders: Optional[list[Order]] = orders
        self.event_data: Optional[dict] = event_data

    def to_dict(self):
        data = super().to_dict()
        if self.orders is not None:
            data["orders"] = [order.to_dict() for order in self.orders]

        if self.event_data is not None:
            data["event_data"] = self.event_data

        return data


class OrderMatchingUseCase:

    order_repository = DjangoOrderRepository()

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
        end_date: Optional[datetime] = None,
    ) -> OrderMatchingUseCaseResult:

        try:
            order = Order(
                client_id=client_id,
                order_id=idempotency_key,
                symbol=symbol,
                order_type=order_type,
                order_style=order_style,
                order_duration=order_duration,
                quantity=quantity,
                price=price,
                end_date=end_date,
            )

            order.validate_data()

            orders = self.order_repository.get_potential_matches(order)

            if not orders:
                return OrderMatchingUseCaseResult(
                    message="No matching orders found.",
                    code=200,
                    orders=[],
                )

            sorted_orders = sorted(
                orders, key=lambda order: (-order.price, order.created_at)
            )

            for existing_order in sorted_orders:
                logger.debug(
                    f"Found matching order: {existing_order.to_dict()}"
                )

            matching_orders = []
            total_quantity = 0

            # Collect matching orders until the requested quantity is fulfilled
            for matching_order in sorted_orders:
                matching_orders.append(matching_order)
                total_quantity += (
                    matching_order.quantity - matching_order.quantity_executed
                )
                if total_quantity >= order.quantity:
                    break

            orders_matched = self.order_repository.execute_order(
                order=order, matching_orders=matching_orders
            )

            event_data = {
                "event": "OrderMatched",
                "order": order.to_dict(),
                "orders_matched": orders_matched,
                "matching_orders": [order.to_dict() for order in matching_orders],
            }

            return OrderMatchingUseCaseResult(
                message="The order was placed successfully.",
                code=201,
                orders=[order],
                event_data=event_data,
            )

        except OrderInvalidException as order_invalid_exception:
            logger.error(
                f"OrderInvalidException in OrderMatchingUseCase for client_id {client_id}: {order_invalid_exception.log_message}",
                exc_info=True,
            )
            return OrderMatchingUseCaseResult(
                message=order_invalid_exception.user_message,
                code=order_invalid_exception.error_code,
            )

        except DataAccessException as data_access_exception:
            logger.error(
                f"DataAccessException in OrderMatchingUseCase for client_id {client_id}: {data_access_exception.log_message}",
                exc_info=True,
            )
            return OrderMatchingUseCaseResult(
                message=data_access_exception.user_message,
                code=data_access_exception.error_code,
            )
