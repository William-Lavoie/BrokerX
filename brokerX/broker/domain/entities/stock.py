import copy
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
        previous_close: Decimal = Decimal("0.00"),
        volume: int = 0,
        last_price: Decimal = Decimal("0.00"),
        active: bool = True,
    ):
        if not active or not symbol or not symbol.isalpha():
            raise StockInvalidException()

        self.symbol = symbol
        self.previous_close = previous_close
        self.volume = volume
        self.last_price = last_price
        self.active = True

    def to_dict(self):
        return copy.copy(self.__dict__)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            symbol=data.get("symbol", ""),
            previous_close=Decimal(str(data.get("previous_close", "0.00"))),
            volume=data.get("volume", 0),
            last_price=Decimal(str(data.get("last_price", "0.00"))),
            active=data.get("active", True),
        )
