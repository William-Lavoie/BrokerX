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
        # redis_balance = self.redis.get_wallet_balance(client_id=client_id)
        # if redis_balance:
        #   return WalletDTO(success=True, code=200, balance=Decimal(redis_balance))

        wallet_dto = self.dao.get_balance(client_id)
        self.redis.set_wallet_balance(client_id, wallet_dto.balance)
        return wallet_dto

    def get_effective_balance(self, client_id: UUID) -> Decimal:
        balance = self.get_balance(client_id).balance
        reserved_funds = self.dao.get_reserved_funds(client_id)

        return balance - reserved_funds

    def reserve_funds(
        self, client_id: UUID, amount: Decimal, order_id: UUID
    ) -> WalletDTO:
        return self.dao.reserve_funds(
            client_id=client_id, amount=amount, order_id=order_id
        )

    def release_funds(self, client_id: UUID, order_id: UUID) -> WalletDTO:
        return self.dao.release_funds(client_id=client_id, order_id=order_id).success

    def process_payments(self, orders_info: list[dict]) -> None:
        wallet_dto = self.dao.process_payments(orders_info=orders_info)

        if not wallet_dto or not wallet_dto.success:
            raise Exception("Error processing payment.")

    def process_transfers(self, orders_info: list[dict]) -> None:
        wallet_dto = self.dao.process_transfers(orders_info=orders_info)

        if not wallet_dto.success:
            raise Exception("Error processing transfer.")
