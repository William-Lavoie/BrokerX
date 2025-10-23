import copy
from decimal import Decimal


class Wallet:
    MAX_WALLET_BALANCE = Decimal("10000.00")

    def __init__(
        self,
        balance: Decimal,
    ):
        self.balance: Decimal = balance

    def can_add_funds(self, amount: Decimal):
        return Decimal(self.balance) + amount <= self.MAX_WALLET_BALANCE

    def to_dict(self):
        return copy.copy(self.__dict__)
    
