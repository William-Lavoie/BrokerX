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
