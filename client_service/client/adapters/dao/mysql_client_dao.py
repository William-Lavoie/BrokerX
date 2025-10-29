import logging

from client.domain.ports.dao.client_dao import ClientDAO, ClientDTO
from client.models import Client, User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q

logger = logging.getLogger("mysql")


class MySQLClientDAO(ClientDAO):
    def get_client_by_email(self, email: str) -> ClientDTO:
        try:
            client = Client.objects.get(email=email)

            return ClientDTO(
                success=True,
                code=200,
                first_name=client.first_name,
                last_name=client.last_name,
                address=client.address,
                birth_date=str(client.birth_date),
                phone_number=client.phone_number,
                email=client.email,
                status=client.status,
                client_id=client.client_id,
            )
        except ObjectDoesNotExist:
            logger.error(
                f"ObjectDoesNotExist exception : There is no client with the email {email}",
                exc_info=True,
            )
            return ClientDTO(success=False, code=404)

    def add_user(
        self,
        first_name: str,
        last_name: str,
        birth_date: str,
        email: str,
        phone_number: str,
        address: str,
        password: str,
    ) -> ClientDTO:
        try:
            existing_user = Client.objects.filter(
                Q(email=email) | Q(phone_number=phone_number)
            ).exists()

            if existing_user:
                logger.warning(
                    f"There is already a user with the same email address ({email}) or phone number ({phone_number})"
                )
                return ClientDTO(success=False, code=409)

            with transaction.atomic():
                user = User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=email,
                )
                user.set_password(password)
                user.save()

                client = Client.objects.create(
                    user=user,
                    client_id=user.uuid,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    birth_date=birth_date,
                    address=address,
                    status="P",
                )

            return ClientDTO(
                success=True,
                code=201,
                first_name=client.first_name,
                last_name=client.last_name,
                address=client.address,
                birth_date=client.birth_date,
                email=client.email,
                phone_number=client.phone_number,
                status=client.status,
                client_id=client.client_id,
            )

        except AttributeError as e:
            logger.error(f"The request is invalid: {e}")
            return ClientDTO(success=False, code=400)

    def update_status(self, email: str, new_status: str) -> ClientDTO:
        with transaction.atomic():
            updated_rows = Client.objects.filter(email=email).update(status=new_status)

        if updated_rows == 0:
            logger.error(f"There is no user with the email {email}")
            return ClientDTO(success=False, code=404)
        return ClientDTO(success=True, code=200)

    def get_status(self, email: str) -> ClientDTO:
        try:
            status = Client.objects.only("status").get(user__email=email).status
            return ClientDTO(success=True, code=200, status=status)

        except ObjectDoesNotExist:
            logger.error(f"There is no user with the email {email}")
            return ClientDTO(success=False, code=404)
