import copy
from datetime import datetime
from decimal import Decimal


class StockInvalidException(Exception):
    def __init__(
        self,
        user_message: str = "The stock you have selected does not exist or has been retired.",
        log_message: str = "Stock instance has been created with active = False",
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
        name: str = "",
        exchange: str = "",
        currency: str = "CAD",
        last_price: Decimal = Decimal("0.00"),
        open_price: Decimal = Decimal("0.00"),
        high_price: Decimal = Decimal("0.00"),
        low_price: Decimal = Decimal("0.00"),
        close_price: Decimal = Decimal("0.00"),
        bid_price: Decimal = Decimal("0.00"),
        bid_size: int = 0,
        ask_price: Decimal = Decimal("0.00"),
        ask_size: int = 0,
        volume: int = 0,
        timestamp: datetime = None,
        active: bool = True,
    ):
        if not active or not symbol or not symbol.isalpha():
            raise StockInvalidException()

        # Metadata
        self.symbol = symbol
        self.name = name
        self.exchange = exchange
        self.currency = currency

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
        self.timestamp = timestamp or datetime.utcnow()

        self.active = active

    def to_dict(self):
        return copy.deepcopy(self.__dict__)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            symbol=data.get("symbol", ""),
            name=data.get("name", ""),
            exchange=data.get("exchange", ""),
            currency=data.get("currency", "CAD"),
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
