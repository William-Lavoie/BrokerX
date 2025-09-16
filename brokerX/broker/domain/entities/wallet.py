from brokerX.broker.domain.core.user import User


class Wallet:
    def __init__(self, user, balance):
        self.user : User = user
        self.balance : float = balance