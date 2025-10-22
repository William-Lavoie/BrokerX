from decimal import Decimal

from ..adapters.dao.mysql_wallet_dao import MySQLWalletDAO
from ..domain.ports.dao.wallet_dao import WalletDTO
from ..domain.ports.wallet_repository import WalletRepository


class DjangoWalletRepository(WalletRepository):
    def __init__(self, dao=None):
        super().__init__()
        self.dao = dao if dao is not None else MySQLWalletDAO()

    def add_funds(self, email: str, amount: Decimal) -> WalletDTO:
        return self.dao.add_funds(email, amount)

    def get_balance(self, email: str) -> WalletDTO:
        return self.dao.get_balance(email)
