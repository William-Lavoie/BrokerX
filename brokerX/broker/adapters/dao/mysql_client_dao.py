import logging

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q

from ...adapters.result import Result
from ...domain.entities.client import ClientProfile
from ...models import Client

logger = logging.getLogger(__name__)


class MySQLClientDAO:
    def add_user(self, client: ClientProfile) -> Result:
        try:
            existing_user = Client.objects.filter(
                Q(user__email=client.email) | Q(phone_number=client.phone_number)
            ).exists()

            if existing_user:
                logger.warning(
                    f"There is already a user with the same email address ({client.email}) or phone number ({client.phone_number})"
                )
                return Result(success=False, code=409)

            with transaction.atomic():
                user = User.objects.create_user(  # type: ignore[attr-defined]
                    first_name=client.first_name,
                    last_name=client.last_name,
                    email=client.email,
                    username=client.email,
                    password=client.password,
                )

                Client.objects.create(
                    user=user,
                    phone_number=client.phone_number,
                    birth_date=client.birth_date,
                    address=client.address,
                    status=client.status,
                )

            return Result(success=True, code=201)

        except Exception as e:
            logger.error(f"MySQL raised the following error: {e}")
            return Result(success=False, code=500)

    def update_status(self, email: str, new_status: str) -> Result:
        try:
            client = Client.objects.get(user__email=email)
            client.status = new_status
            client.save()

            return Result(success=True, code=200)

        except ObjectDoesNotExist:
            logger.error(f"There is no user with the email {email}")
            return Result(success=False, code=404)

    def get_status(self, email: str) -> Result:
        try:
            status = Client.objects.only("status").get(user__email=email).status
            return Result(success=True, code=200, data=status)

        except ObjectDoesNotExist:
            logger.error(f"There is no user with the email {email}")
            return Result(success=False, code=404, data=None)
