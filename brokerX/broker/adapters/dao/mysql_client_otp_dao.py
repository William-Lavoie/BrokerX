import logging

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError, transaction

from ...adapters.result import Result
from ...domain.ports.dao.client_otp_dao import ClientOTPDAO
from ...models import ClientOTP

logger = logging.getLogger(__name__)

# TODO: handle connection errors
class MySQLClientOTPDAO(ClientOTPDAO):
    def set_secret_key(self, email: str, secret: str) -> Result:
        try:
            with transaction.atomic():
                user: User = User.objects.get(email=email)
                ClientOTP.objects.update_or_create(
                    user=user, defaults={"secret": secret, "number_attempts": 0}
                )
            return Result(success=True, code=200)

        except ObjectDoesNotExist:
            logger.error(f"There is no user with the email {email}")
            return Result(success=False, code=404)

    def get_secret_key(self, email: str) -> Result:
        try:
            secret: str = ClientOTP.objects.only("secret").get(user__email=email).secret
            return Result(success=True, code=200, data=secret)

        except ObjectDoesNotExist:
            logger.error(f"There is no user with the email {email}")
            return Result(success=False, code=404)

    def delete_passcode(self, email: str) -> Result:
        try:
            ClientOTP.objects.get(user__email=email).delete()
            return Result(success=True, code=200)

        except ObjectDoesNotExist:
            logger.error(f"There is no user with the email {email}")
            return Result(success=False, code=404)

    def increment_attempts(self, email: str) -> Result:
        try:
            otp = ClientOTP.objects.get(user__email=email)
            otp.number_attempts += 1
            attempts: int = otp.number_attempts

            if attempts >= 2:
                otp.delete()
                return Result(success=True, code=200, data=attempts)

            else:
                otp.save()
                return Result(success=True, code=200, data=attempts)

        except ObjectDoesNotExist:
            logger.error(f"There is no user with the email {email}")
            return Result(success=False, code=404)
