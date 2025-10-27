import logging
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from otp.domain.ports.dao.otp_dao import OTPDAO
from otp.domain.ports.otp_repository import OTPDTO
from otp.models import OTP

logger = logging.getLogger("mysql")


class MySQLOTPDAO(OTPDAO):
    def set_secret_key(self, client_id: UUID, secret: str) -> OTPDTO:
        with transaction.atomic():
            OTP.objects.update_or_create(
                client_id=client_id, defaults={"secret": secret, "number_attempts": 0}
            )
        return OTPDTO(success=True, code=200)

    def get_secret_key(self, client_id: UUID) -> OTPDTO:
        try:
            secret: str = OTP.objects.only("secret").get(client_id=client_id).secret
            return OTPDTO(success=True, code=200, secret=secret)

        except ObjectDoesNotExist:
            logger.error(f"There is no user with the id {client_id}")
            return OTPDTO(success=False, code=404)

    def delete_passcode(self, client_id: UUID) -> OTPDTO:
        try:
            with transaction.atomic():
                OTP.objects.get(client_id=client_id).delete()
                return OTPDTO(success=True, code=200, validated=True)

        except ObjectDoesNotExist:
            logger.error(f"There is no user with the id {client_id}")
            return OTPDTO(success=False, code=404)

    def increment_attempts(self, client_id: UUID) -> OTPDTO:
        try:
            with transaction.atomic():
                otp = OTP.objects.get(client_id=client_id)
                otp.number_attempts += 1
                attempts: int = otp.number_attempts

                if attempts >= 2:
                    otp.delete()
                    return OTPDTO(success=False, code=401, attempts=attempts)

                else:
                    otp.save()
                    return OTPDTO(success=False, code=401, attempts=attempts)

        except ObjectDoesNotExist:
            logger.error(f"There is no user with the id {client_id}")
            return OTPDTO(success=False, code=404)
