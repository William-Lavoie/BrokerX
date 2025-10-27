from decimal import Decimal
from uuid import UUID

from wallet.adapters.dao.mysql_wallet_dao import MySQLWalletDAO
from wallet.adapters.redis.redis_wallet import RedisWallet
from wallet.domain.ports.dao.wallet_dao import WalletDTO
from wallet.domain.ports.wallet_repository import WalletRepository


class DjangoWalletRepository(WalletRepository):
    def __init__(self, dao=None, redis=None):
        super().__init__()
        self.dao = dao if dao is not None else MySQLWalletDAO()
        self.redis = redis if redis is not None else RedisWallet()

    def add_funds(self, client_id: UUID, amount: Decimal) -> WalletDTO:
        wallet_dto = self.dao.add_funds(client_id, amount)
        if wallet_dto.success:
            self.redis.set_wallet_balance(
                client_id=client_id, balance=wallet_dto.balance
            )

        return wallet_dto

    def get_balance(self, client_id: UUID) -> WalletDTO:
        redis_balance = self.redis.get_wallet_balance(client_id=client_id)
        if redis_balance:
            return WalletDTO(success=True, code=200, balance=Decimal(redis_balance))

        wallet_dto = self.dao.get_balance(client_id)
        self.redis.set_wallet_balance(client_id, wallet_dto.balance)
        return wallet_dto
