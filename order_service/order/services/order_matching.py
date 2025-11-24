import logging
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from order.adapters.kafka.order_event_producer import OrderEventProducer
from order.domain.entities.order import Order, OrderInvalidException

from order_service.exceptions import DataAccessException
from order_service.order.adapters.django_order_repository import DjangoOrderRepository
from order_service.order.services.place_order import PlaceOrderUseCaseResult
from order_service.settings import KAFKA_TOPIC
from order_service.use_case_results import UseCaseResult

logger = logging.getLogger("order")


class OrderMatchingUseCaseResult(UseCaseResult):
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

            sorted_orders = sorted(orders, key=lambda order: (-order.price, order.time))

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
                "event_type": "ORDER_EXECUTED",
                "data": {
                    "order": order.to_dict(),
                    "order_matched": orders_matched,
                    "matching_orders": [order.to_dict() for order in matching_orders],
                },
            }

            try:
                OrderEventProducer().get_instance().send(KAFKA_TOPIC, value=event_data)
                logger.error(f"Message sent successfully to {KAFKA_TOPIC}")
            except Exception as e:
                logger.error(f"Failed to send message: {str(e)}")

            return OrderMatchingUseCaseResult(
                message="The order was placed successfully.",
                code=201,
                orders=[order],
            )

        except OrderInvalidException as order_invalid_exception:
            logger.error(
                f"OrderInvalidException in PlaceOrderUseCase for client_id {client_id}: {order_invalid_exception.log_message}",
                exc_info=True,
            )
            return OrderMatchingUseCaseResult(
                message=order_invalid_exception.user_message,
                code=order_invalid_exception.error_code,
            )

        except DataAccessException as data_access_exception:
            self.wallet_repository.release_funds(
                order_id=order.order_id, client_id=order.client_id
            )
            return OrderMatchingUseCaseResult(
                message=data_access_exception.user_message,
                code=data_access_exception.error_code,
            )
