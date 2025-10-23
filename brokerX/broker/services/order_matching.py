import logging
import uuid
from decimal import Decimal
from typing import Optional

from ..domain.entities.client import Client
from ..domain.entities.order import Order, OrderInvalidException
from ..domain.entities.stock import Stock, StockInvalidException
from ..domain.ports.client_repository import ClientRepository
from ..domain.ports.order_repository import OrderRepository
from ..domain.ports.stock_repository import StockRepository
from ..domain.ports.wallet_repository import WalletRepository
from ..exceptions import DataAccessException
from .use_case_result import UseCaseResult

logger = logging.getLogger(__name__)


class OrderMatchingUseCase:
    def __init__(
        self,
        client_repository: ClientRepository,
        stock_repository: StockRepository,
        order_repository: OrderRepository,
    ):
        self.client_repository = client_repository
        self.stock_repository = stock_repository
        self.order_repository = order_repository

    def execute(
        self,
        order: Order,
    ) -> UseCaseResult:

        try:
            matching_orders: list[Order] = self.order_repository.find_matching_orders(
                order
            )

            potential_matches = []
            for matching_order in matching_orders:

                price = (
                    order.stock.last_price
                    if not matching_order.limit
                    else matching_order
                )

                if order.price_is_acceptable():
                    potential_matches.append(
                        matching_order, price, order.stock.last_price
                    )

        except StockInvalidException as stock_exception:
            logger.error(
                f"StockInvalidException in PlaceOrderUseCase for symbol {symbol}: {stock_exception.log_message} {stock_exception.error_code}",
                exc_info=True,
            )
            return UseCaseResult(
                success=False,
                message=stock_exception.user_message,
                code=stock_exception.error_code,
            )

        except OrderInvalidException as order_exception:
            logger.error(
                f"OrderInvalidException in PlaceOrderUseCase for symbol {symbol}, direction {direction}, limit {limit}, quantity {quantity} : {order_exception.log_message}",
                exc_info=True,
            )
            return UseCaseResult(
                success=False,
                message=order_exception.user_message,
                code=order_exception.error_code,
            )

        except DataAccessException as data_access_exception:
            return UseCaseResult(
                success=False,
                message=data_access_exception.user_message,
                code=data_access_exception.error_code,
            )
