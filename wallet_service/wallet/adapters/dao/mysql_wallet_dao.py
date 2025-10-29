import logging
from decimal import Decimal
from uuid import UUID

from django.db import transaction
from wallet.domain.ports.dao.wallet_dao import WalletDAO, WalletDTO
from wallet.models import Wallet

logger = logging.getLogger("mysql")


class MySQLWalletDAO(WalletDAO):
    def get_balance(self, client_id: UUID) -> WalletDTO:
        with transaction.atomic():
            wallet, created = Wallet.objects.get_or_create(client_id=client_id)

            return WalletDTO(success=True, code=200, balance=wallet.balance)

    def add_funds(self, client_id: UUID, amount: Decimal) -> WalletDTO:
        with transaction.atomic():
            wallet, created = Wallet.objects.get_or_create(client_id=client_id)

            wallet.balance = Decimal(wallet.balance) + Decimal(amount)
            wallet.save()

            return WalletDTO(success=True, code=200, balance=wallet.balance)
