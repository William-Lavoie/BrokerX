from decimal import Decimal
from typing import Optional
from uuid import UUID

from ...domain.entities.client import Client
from ...domain.entities.stock import Stock


class OrderInvalidException(Exception):
    def __init__(
        self,
        user_message: str = "The order could not be placed.",
        log_message: str = "The order was invalid.",
        error_code: int = 400,
    ):
        super().__init__(user_message)
        self.user_message = user_message
        self.log_message = log_message
        self.error_code = error_code


class Order:
    def __init__(
        self,
        stock: Optional[Stock],
        client: Optional[Client],
        direction: str = "",
        limit: Optional[Decimal] = Decimal("0.00"),
        initial_quantity: int = 0,
        remaining_quantity: int = 0,
        order_id=Optional[UUID],
    ):

        if initial_quantity < 1:
            raise OrderInvalidException(
                user_message="You must choose a quantity of at least 1 share.",
                log_message=f"User tried placing an order with quantity = {initial_quantity}",
            )

        self.stock: Optional[Stock] = stock
        self.client: Optional[Client] = client
        self.direction: str = direction
        self.limit: Optional[Decimal] = limit
        self.initial_quantity: int = initial_quantity
        self.remaining_quantity: int = remaining_quantity
        self.order_id: Optional[UUID] = order_id

    def price_is_acceptable(
        self, offered_price: Decimal, market_price: Decimal
    ) -> bool:
        return (
            self.limit is None and offered_price == market_price
        )  # or (self.limit and )
