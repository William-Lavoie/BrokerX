import logging
from decimal import Decimal
from uuid import UUID

from django.db import transaction, IntegrityError
from django.db.models import Sum
from wallet.domain.ports.dao.wallet_dao import WalletDAO, WalletDTO
from wallet.models import ReservedFunds, Wallet

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

    def get_reserved_funds(self, client_id: UUID) -> Decimal:
        reserved_funds = ReservedFunds.objects.filter(client_id=client_id).aggregate(
            total=Sum("amount")
        )["total"]

        return reserved_funds if reserved_funds is not None else Decimal("0.00")

    def reserve_funds(
        self, client_id: UUID, amount: Decimal, order_id: UUID
    ) -> WalletDTO:
        try:
            with transaction.atomic():
                ReservedFunds.objects.create(
                    client_id=client_id, order_id=order_id, amount=amount
                )

                return WalletDTO(success=True, code=201)

        except IntegrityError:
            logger.error(
                f"IntegrityError: client {client_id} already has a reservation for order {order_id},",
                exc_info=True,
            )
            return Wallet(success=False, code=409)
