from decimal import Decimal

from ..domain.entities.wallet import Wallet
from ..adapters.dao.mysql_wallet_dao import MySQLWalletDAO
from ..domain.ports.dao.wallet_dao import WalletDTO
from ..domain.ports.wallet_repository import WalletRepository


class DjangoWalletRepository(WalletRepository):
    def __init__(self, dao=None):
        super().__init__()
        self.dao = dao if dao is not None else MySQLWalletDAO()

    def add_funds(self, email: str, amount: Decimal) -> Decimal:
        return self.dao.add_funds(email, amount)

    def get_wallet(self, email: str) -> Wallet:
        wallet_dto: WalletDTO = self.dao.get_wallet(email)
        return Wallet(balance=Decimal(wallet_dto.balance))
