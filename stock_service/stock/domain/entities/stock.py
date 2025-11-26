import copy
import logging
from decimal import Decimal
from typing import Optional

logger = logging.getLogger("stock")


class StockInvalidException(Exception):
    def __init__(
        self,
        user_message: str = "The stock you have selected does not exist or has been retired.",
        log_message: str = "Stock instance was found found or is not active.",
        error_code: int = 400,
    ):
        super().__init__(user_message)
        self.user_message = user_message
        self.log_message = log_message
        self.error_code = error_code


class Stock:
    def __init__(
        self,
        symbol: str = "",
        name: Optional[str] = None,
        exchange: Optional[str] = "",
        currency: Optional[str] = "CAD",
        band: Optional[Decimal] = Decimal("5.00"),
        tick_size: Optional[Decimal] = Decimal("0.01"),
        last_price: Optional[Decimal] = Decimal("0.00"),
        open_price: Optional[Decimal] = Decimal("0.00"),
        high_price: Optional[Decimal] = Decimal("0.00"),
        low_price: Optional[Decimal] = Decimal("0.00"),
        close_price: Optional[Decimal] = Decimal("0.00"),
        bid_price: Optional[Decimal] = Decimal("0.00"),
        bid_size: Optional[int] = 0,
        ask_price: Optional[Decimal] = Decimal("0.00"),
        ask_size: Optional[int] = 0,
        volume: Optional[int] = 0,
        timestamp: Optional[str] = None,
        active: bool = True,
    ):
        if not active or not symbol or not symbol.isalpha():
            raise StockInvalidException()

        # Metadata
        self.symbol = symbol
        self.name = name
        self.exchange = exchange
        self.currency = currency
        self.band = band
        self.tick_size = tick_size

        # Prices
        self.last_price = last_price
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price

        # Top of book
        self.bid_price = bid_price
        self.bid_size = bid_size
        self.ask_price = ask_price
        self.ask_size = ask_size

        # Volume and timestamp
        self.volume = volume
        self.timestamp = timestamp

        self.active = active

    def validate_order(
        self, quantity: int, type: str, price: Optional[Decimal]
    ) -> None:

        # Quantity is larger than the volume
        if quantity > self.volume:
            raise StockInvalidException(
                user_message="The order quantity cannot be greater than the total volume of shares.",
                log_message=f"Order quantity {quantity} is invalid. Stock has only {self.volume} shares available.",
                error_code=400,
            )

        # Tick size is not respected
        if price and not price % self.tick_size.normalize() == 0:
            raise StockInvalidException(
                user_message=f"The price cannot be more precise than ${self.tick_size.normalize()}.",
                log_message=f"Price {price} is invalid. Tick size is {self.tick_size}.",
                error_code=400,
            )

        # Band size
        price_band = Decimal(self.band / 100)
        if type == "BUY":

            if price and not (
                Decimal(price) >= Decimal(self.bid_price * (1 - price_band))
                and Decimal(price) <= Decimal(self.bid_price * (1 + price_band))
            ):
                raise StockInvalidException(
                    user_message=f"The price cannot differ from the market price by more than {self.band}%.",
                    log_message=f"Order price {price} is invalid for band {self.band}.",
                    error_code=400,
                )

        elif type == "SELL":
            if price and not (
                price >= self.ask_price * (1 - self.band)
                and price <= self.ask_price(1 + self.band)
            ):
                raise StockInvalidException(
                    user_message=f"The price cannot differ from the market price by more than {price_band}%.",
                    log_message=f"Order price {price} is invalid for band {self.band}.",
                    error_code=400,
                )

    def to_dict(self) -> dict:
        return copy.deepcopy(self.__dict__)

    @classmethod
    def from_dict(cls, data: dict) -> "Stock":
        return cls(
            symbol=data.get("symbol", ""),
            name=data.get("name", ""),
            exchange=data.get("exchange", ""),
            currency=data.get("currency", "CAD"),
            band=Decimal(str(data.get("band", "5.00"))),
            tick_size=Decimal(str(data.get("tick_size", "0.01"))),
            last_price=Decimal(str(data.get("last_price", "0.00"))),
            open_price=Decimal(str(data.get("open_price", "0.00"))),
            high_price=Decimal(str(data.get("high_price", "0.00"))),
            low_price=Decimal(str(data.get("low_price", "0.00"))),
            close_price=Decimal(str(data.get("close_price", "0.00"))),
            bid_price=Decimal(str(data.get("bid_price", "0.00"))),
            bid_size=data.get("bid_size", 0),
            ask_price=Decimal(str(data.get("ask_price", "0.00"))),
            ask_size=data.get("ask_size", 0),
            volume=data.get("volume", 0),
            timestamp=data.get("timestamp"),
            active=data.get("active", True),
        )
