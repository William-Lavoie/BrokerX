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
from ..services.use_case_result import UseCaseResult

logger = logging.getLogger(__name__)


class PlaceOrderUseCase:
    def __init__(
        self,
        client_repository: ClientRepository,
        stock_repository: StockRepository,
        order_repository: OrderRepository,
        wallet_repository: WalletRepository,
    ):
        self.client_repository = client_repository
        self.stock_repository = stock_repository
        self.order_repository = order_repository
        self.wallet_repository = wallet_repository

    def execute(
        self,
        email: str,
        direction: str,
        limit: Optional[Decimal],
        quantity: int,
        symbol: str,
        idempotency_key: uuid.UUID,
    ) -> UseCaseResult:

        direction = direction.lower()

        if (
            quantity < 1
            or (limit and limit < Decimal("0.01"))
            or direction not in ["buy", "sell"]
        ):
            logger.warning(f"User {email} tried placing an order for {symbol} with {quantity} shares with direction {direction} and limit {limit}.")
            return UseCaseResult(
                success=False,
                message="You have entered invalid data",
                code=403,
            )
        try:
            client: Client = self.client_repository.get_user(email)

            # Pre-trade control is embedded within the entities
            if not client.is_active():
                logger.warning(f"Inactive client {email} tried to place an order.")
                return UseCaseResult(
                    success=False,
                    message="Your account must be active to place orders. The order was not processed.",
                    code=403,
                )

            stock: Stock = self.stock_repository.get_stock_by_symbol(symbol)

            if direction == "sell":

                if not client.can_sell_shares(symbol=symbol, quantity=quantity):
                    logger.warning(
                        f"Client {email} tried to place a sell order with {quantity} shares."
                    )
                    return UseCaseResult(
                        success=False,
                        message="You do not have enough shares to sell.",
                        code=400,
                    )

            elif direction == "buy":
                if not client.can_buy_shares(
                    stock=stock, quantity=quantity, limit=limit
                ):
                    logger.warning(
                        f"Client {email} tried to place a sell order with {quantity} shares."
                    )
                    return UseCaseResult(
                        success=False,
                        message="You do not have enough funds.",
                        code=400,
                    )
            order: Order = self.order_repository.add_order(
                client=client,
                stock=stock,
                direction=direction,
                limit=limit,
                initial_quantity=quantity,
                idempotency_key=idempotency_key,
            )
            client.orders.append(order)

            return UseCaseResult(
                success=True,
                message="The order was placed successfully.",
                code=201,
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
