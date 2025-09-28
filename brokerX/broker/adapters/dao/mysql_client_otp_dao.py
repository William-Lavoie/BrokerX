import logging

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from ...adapters.result import Result
from ...domain.ports.dao.client_otp_dao import ClientOTPDAO
from ...domain.ports.otp_repository import OTPDTO
from ...models import ClientOTP

logger = logging.getLogger(__name__)


# TODO: handle connection errors
class MySQLClientOTPDAO(ClientOTPDAO):
    def set_secret_key(self, email: str, secret: str) -> OTPDTO:
        try:
            with transaction.atomic():
                user: User = User.objects.get(email=email)
                ClientOTP.objects.update_or_create(
                    user=user, defaults={"secret": secret, "number_attempts": 0}
                )
            return OTPDTO(success=True, code=200)

        except ObjectDoesNotExist:
            logger.error(f"There is no user with the email {email}")
            return OTPDTO(success=False, code=404)

    def get_secret_key(self, email: str) -> OTPDTO:
        try:
            secret: str = ClientOTP.objects.only("secret").get(user__email=email).secret
            return OTPDTO(success=True, code=200, secret=secret)

        except ObjectDoesNotExist:
            logger.error(f"There is no user with the email {email}")
            return OTPDTO(success=False, code=404)

    def delete_passcode(self, email: str) -> OTPDTO:
        try:
            with transaction.atomic():
                ClientOTP.objects.get(user__email=email).delete()
                return OTPDTO(success=True, code=200, validated=True)

        except ObjectDoesNotExist:
            logger.error(f"There is no user with the email {email}")
            return OTPDTO(success=False, code=404)

    def increment_attempts(self, email: str) -> OTPDTO:
        try:
            with transaction.atomic():
                otp = ClientOTP.objects.get(user__email=email)
                otp.number_attempts += 1
                attempts: int = otp.number_attempts

                if attempts >= 2:
                    otp.delete()
                    return OTPDTO(success=True, code=200, attempts=attempts)

                else:
                    otp.save()
                    return OTPDTO(success=True, code=200, attempts=attempts)

        except ObjectDoesNotExist:
            logger.error(f"There is no user with the email {email}")
            return OTPDTO(success=False, code=404)
