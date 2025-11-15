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
        quantity: int,
        idempotency_key: UUID,
        price: Optional[Decimal] = None,
    ) -> PlaceOrderUseCaseResult:

        if quantity < 1:
            logger.warning(
                f"Client {client_id} tried placing an order for {symbol} with {quantity} shares."
            )
            return PlaceOrderUseCaseResult(
                success=False,
                message="You have entered invalid data",
                code=422,
            )

        if (order_type not in ["BUY", "SELL"]) or (
            order_style not in ["MARKET", "LIMIT"]
        ):
            logger.warning(
                f"Client {client_id} tried placing an order for {symbol} with invalid order type {order_type} or order style {order_style}."
            )
            return PlaceOrderUseCaseResult(
                success=False,
                message="You have entered invalid data",
                code=422,
            )

        if order_style == "LIMIT" and (price is None or price <= Decimal("0.00")):
            logger.warning(
                f"Client {client_id} tried placing a LIMIT order for {symbol} without a valid price."
            )
            return PlaceOrderUseCaseResult(
                success=False,
                message="You have entered invalid data",
                code=422,
            )

        try:

            if order_type == "SELL":
                pass

            elif order_type == "BUY":
                wallet_dto: WalletDTO = self.wallet_repository.get_balance(
                    email=client.email
                )
                if not client.can_buy_shares(
                    stock=stock,
                    quantity=quantity,
                    limit=limit,
                    balance=wallet_dto.balance,
                ):
                    logger.warning(
                        f"Client {email} tried to place a buy order with {quantity} shares."
                    )
                    return PlaceOrderUseCaseResult(
                        success=False,
                        message="You do not have enough funds.",
                        code=412,
                    )
            order: Order = self.order_repository.add_order(
                client=client,
                stock=stock,
                direction=direction,
                limit=limit,
                initial_quantity=quantity,
                idempotency_key=idempotency_key,
            )

            order_matching_use_case = OrderMatchingUseCase(
                self.client_repository, self.stock_repository, self.order_repository
            )

            thread = threading.Thread(
                target=order_matching_use_case.execute, args=(order,)
            )
            thread.start()

            return PlaceOrderUseCaseResult(
                success=True,
                message="The order was placed successfully.",
                code=201,
            )

        except StockInvalidException as stock_exception:
            logger.error(
                f"StockInvalidException in PlaceOrderUseCase for symbol {symbol}: {stock_exception.log_message} {stock_exception.error_code}",
                exc_info=True,
            )
            return PlaceOrderUseCaseResult(
                success=False,
                message=stock_exception.user_message,
                code=stock_exception.error_code,
            )

        except OrderInvalidException as order_exception:
            logger.error(
                f"OrderInvalidException in PlaceOrderUseCase for symbol {symbol}, direction {direction}, limit {limit}, quantity {quantity} : {order_exception.log_message}",
                exc_info=True,
            )
            return PlaceOrderUseCaseResult(
                success=False,
                message=order_exception.user_message,
                code=order_exception.error_code,
            )

        except DataAccessException as data_access_exception:
            return PlaceOrderUseCaseResult(
                success=False,
                message=data_access_exception.user_message,
                code=data_access_exception.error_code,
            )

    def get_orders(self, email: str):
        try:
            orders = self.order_repository.get_orders_by_client(email=email)
            return PlaceOrderUseCaseResult(
                success=True,
                code=200,
                message="Order fetched successfully",
                orders=orders,
            )

        except ClientInvalidException as client_exception:
            return PlaceOrderUseCaseResult(
                success=False,
                message=client_exception.user_message,
                code=client_exception.error_code,
            )
        except DataAccessException as data_access_exception:
            return PlaceOrderUseCaseResult(
                success=False,
                message=data_access_exception.user_message,
                code=data_access_exception.error_code,
            )
