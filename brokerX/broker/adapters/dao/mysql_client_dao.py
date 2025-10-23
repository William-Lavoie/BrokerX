import logging
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q

from ...domain.entities.client import Client
from ...domain.ports.dao.client_dao import ClientDAO, ClientDTO
from ...models import Client as ClientModel

logger = logging.getLogger(__name__)


class MySQLClientDAO(ClientDAO):
    def get_client_by_email(self, email: str) -> ClientDTO:
        try:
            client = ClientModel.objects.prefetch_related("wallets", "shares").get(
                email=email
            )

            wallet: dict = {}
            wallet_instance = client.wallets.first()
            if wallet_instance:
                wallet = {"balance": Decimal(wallet_instance.balance)}
            shares: dict[str, int] = {}

            for share in client.shares.all():
                shares[share.stock_symbol] = share.quantity

            return ClientDTO(
                success=True,
                code=200,
                first_name=client.first_name,
                last_name=client.last_name,
                address=client.address,
                birth_date=client.birth_date,
                phone_number=client.phone_number,
                email=client.email,
                status=client.status,
                wallet=wallet,
                shares=shares,
            )
        except ObjectDoesNotExist:
            logger.error(
                f"ObjectDoesNotExist exception : There is no client with the email {email}",
                exc_info=True,
            )
            return ClientDTO(success=False, code=404)

    def add_user(self, client: Client) -> ClientDTO:
        try:
            existing_user = ClientModel.objects.filter(
                Q(user__email=client.email) | Q(phone_number=client.phone_number)
            ).exists()

            if existing_user:
                logger.warning(
                    f"There is already a user with the same email address ({client.email}) or phone number ({client.phone_number})"
                )
                return ClientDTO(success=False, code=409)

            with transaction.atomic():
                user = User.objects.create_user(  # type: ignore[attr-defined]
                    first_name=client.first_name,
                    last_name=client.last_name,
                    email=client.email,
                    username=client.email,
                    password="TBD",
                )

                ClientModel.objects.create(
                    user=user,
                    first_name=client.first_name,
                    last_name=client.last_name,
                    email=client.email,
                    phone_number=client.phone_number,
                    birth_date=client.birth_date,
                    address=client.address,
                    status=client.status,
                )

            return ClientDTO(success=True, code=201)

        except AttributeError as e:
            logger.error(f"The request is invalid: {e}")
            return ClientDTO(success=False, code=400)

    def update_status(self, email: str, new_status: str) -> ClientDTO:
        try:
            client = ClientModel.objects.get(user__email=email)
            client.status = new_status
            client.save()

            return ClientDTO(success=True, code=200)

        except ObjectDoesNotExist:
            logger.error(f"There is no user with the email {email}")
            return ClientDTO(success=False, code=404)

    def get_status(self, email: str) -> ClientDTO:
        try:
            status = ClientModel.objects.only("status").get(user__email=email).status
            return ClientDTO(success=True, code=200, status=status)

        except ObjectDoesNotExist:
            logger.error(f"There is no user with the email {email}")
            return ClientDTO(success=False, code=404)
