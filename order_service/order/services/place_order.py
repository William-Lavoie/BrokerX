import json
import logging
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import Optional
from uuid import UUID

from order.adapters.kafka.order_event_producer import OrderEventProducer
from order.domain.entities.order import Order, OrderInvalidException
from order.domain.ports.order_repository import OrderRepository
from order.domain.ports.portfolio_repository import (
    PortfolioException,
    PortfolioRepository,
)
from order.domain.ports.stock_repository import StockException, StockRepository
from order.domain.ports.wallet_repository import WalletException, WalletRepository

from order_service.exceptions import DataAccessException
from order_service.settings import KAFKA_TOPIC
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

        return data


class PlaceOrderUseCase:
    def __init__(
        self,
        order_repository: OrderRepository,
        portfolio_repository: Optional[PortfolioRepository] = None,
        stock_repository: Optional[StockRepository] = None,
        wallet_repository: Optional[WalletRepository] = None,
    ):
        self.order_repository = order_repository
        self.portfolio_repository = portfolio_repository
        self.stock_repository = stock_repository
        self.wallet_repository = wallet_repository

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
    ) -> PlaceOrderUseCaseResult:

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

            base_price = self.stock_repository.update_top_of_book(order=order)

            # Adding 5% to market price to account for volatility
            if order_style == "MARKET":
                digits = -base_price.as_tuple().exponent
                quantizer = Decimal("1").scaleb(-digits)

                # multiply and round
                order.price = (base_price * Decimal("1.05")).quantize(
                    quantizer, rounding=ROUND_HALF_UP
                )

            if order_type == "BUY":
                self.wallet_repository.reserve_funds(order=order)
            elif order_type == "SELL":
                self.portfolio_repository.reserve_holdings(order=order)

            self.order_repository.add_order(
                order=order, idempotency_key=idempotency_key
            )

            event_data = {
                "event": "OrderCreated",
                "order_id": str(order.order_id),
                "client_id": str(order.client_id),
                "price": str(order.price),
                "quantity": order.quantity,
                "symbol": order.symbol,
                "order_type": order.order_type,
                "order_style": order.order_style,
                "order_duration": order.order_duration,
                "end_date": order.end_date,
            }

            serialized_data = json.dumps(event_data).encode("utf-8")
            logger.error(f"Serialized event data size: {len(serialized_data)} bytes")

            try:
                OrderEventProducer().get_instance().send(KAFKA_TOPIC, value=event_data)
                logger.error(f"Message sent successfully to {KAFKA_TOPIC}")
            except Exception as e:
                logger.error(f"Failed to send message: {str(e)}")

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

        except WalletException as wallet_exception:
            logger.error(wallet_exception.log_message, exc_info=True)
            return PlaceOrderUseCaseResult(
                message=wallet_exception.user_message,
                code=wallet_exception.error_code,
            )

        except StockException as stock_exception:
            logger.error(stock_exception.log_message, exc_info=True)
            return PlaceOrderUseCaseResult(
                message=stock_exception.user_message,
                code=stock_exception.error_code,
            )

        except PortfolioException as portfolio_exception:
            logger.error(portfolio_exception.log_message, exc_info=True)
            return PlaceOrderUseCaseResult(
                message=portfolio_exception.user_message,
                code=portfolio_exception.error_code,
            )

        except DataAccessException as data_access_exception:
            self.wallet_repository.release_funds(
                order_id=order.order_id, client_id=order.client_id
            )
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
                message=data_access_exception.user_message,
                code=data_access_exception.error_code,
            )

    def delete_order(self, client_id: UUID, order_id: UUID):
        try:
            logger.error(f"delete order client {client_id} et {order_id}")
            order = self.order_repository.delete_order(
                client_id=client_id, order_id=order_id
            )
            self.wallet_repository.release_funds(order_id=order_id, client_id=client_id)

            return PlaceOrderUseCaseResult(
                message="The order was successfully cancelled.", code=200
            )

        except OrderInvalidException as order_exception:
            logger.error(order_exception.log_message, exc_info=True)
            return PlaceOrderUseCaseResult(
                message=order_exception.user_message,
                code=order_exception.error_code,
            )

        except WalletException as wallet_exception:
            logger.error(wallet_exception.log_message, exc_info=True)

            self.order_repository.delete_order_rollback(
                client_id=client_id, order_id=order_id, previous_status=order.status
            )

            return PlaceOrderUseCaseResult(
                message=wallet_exception.user_message,
                code=wallet_exception.error_code,
            )
