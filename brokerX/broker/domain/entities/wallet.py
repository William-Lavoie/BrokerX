from ...domain.entities.client import ClientProfile


class Wallet:
    def __init__(self, client, balance):
        self.client : ClientProfile = client
        self.balance : float = balance