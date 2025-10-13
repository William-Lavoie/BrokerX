import logging
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from ...domain.ports.dao.wallet_dao import WalletDAO, WalletDTO
from ...models import Client, Wallet

logger = logging.getLogger(__name__)


class MySQLWalletDAO(WalletDAO):
    def get_balance(self, email: str) -> WalletDTO:
        try:
            with transaction.atomic():
                client = Client.objects.get(email=email)
                wallet, created = Wallet.objects.get_or_create(client=client)

                return WalletDTO(success=True, code=200, balance=wallet.balance)

        except ObjectDoesNotExist:
            logger.error(f"There is no user with the email {email}")
            return WalletDTO(success=False, code=404)

    def add_funds(self, email: str, amount: Decimal) -> WalletDTO:
        try:
            with transaction.atomic():
                client = Client.objects.get(email=email)
                wallet, created = Wallet.objects.get_or_create(client=client)
                wallet.balance += amount
                wallet.save()

                return WalletDTO(success=True, code=200, balance=wallet.balance)

        except ObjectDoesNotExist:
            logger.error(f"There is no user with the email {email}")
            return WalletDTO(success=False, code=404)
