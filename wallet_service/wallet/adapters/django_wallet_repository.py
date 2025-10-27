from decimal import Decimal

from ..adapters.dao.mysql_wallet_dao import MySQLWalletDAO
from ..adapters.redis.redis_wallet import (
    redis_get_wallet_balance,
    redis_set_wallet_balance,
)
from ..domain.ports.dao.wallet_dao import WalletDTO
from ..domain.ports.wallet_repository import WalletRepository


class DjangoWalletRepository(WalletRepository):
    def __init__(self, dao=None):
        super().__init__()
        self.dao = dao if dao is not None else MySQLWalletDAO()

    def add_funds(self, email: str, amount: Decimal) -> WalletDTO:
        wallet_dto = self.dao.add_funds(email, amount)
        if wallet_dto.success:
            redis_set_wallet_balance(email=email, balance=wallet_dto.balance)

        return wallet_dto

    def get_balance(self, email: str) -> WalletDTO:
        redis_balance = redis_get_wallet_balance(email=email)
        if redis_balance:
            return WalletDTO(success=True, code=200, balance=Decimal(redis_balance))

        wallet_dto = self.dao.get_balance(email)
        redis_set_wallet_balance(email, wallet_dto.balance)
        return wallet_dto
