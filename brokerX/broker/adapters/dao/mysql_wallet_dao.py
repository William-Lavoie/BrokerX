from decimal import Decimal

from ...domain.ports.dao.wallet_dao import WalletDAO, WalletDTO
from ...models import Wallet
from django.contrib.auth.models import User


class MySQLWalletDAO(WalletDAO):
    def get_wallet(self, email: str) -> WalletDTO:
        user = User.objects.get(email=email)
        wallet, created = Wallet.objects.get_or_create(user=user)
        return WalletDTO(wallet.balance)

    def add_funds(self, email: str, amount: Decimal) -> Decimal:
        wallet, created = Wallet.objects.get_or_create(user__email=email)
        wallet.balance = wallet.balance + amount
        wallet.save()

        return wallet.balance
