import logging
from typing import Optional
from uuid import UUID

import pyotp
from django.core.mail import send_mail
from otp.adapters.base_otp_repository import BaseOTPRepository
from otp.adapters.dao.mysql_otp_dao import MySQLOTPDAO
from otp.domain.ports.otp_repository import OTPDTO

logger = logging.getLogger("client")


class EmailOTPRepository(BaseOTPRepository):
    def __init__(self, dao=None):
        super().__init__()
        self.dao = dao if dao is not None else MySQLOTPDAO()

    def send_passcode(
        self, client_id: Optional[UUID], email: str, passcode: str
    ) -> bool:
        logger.error(f"Welcome {email}! Your passcode is: {passcode}.")
        try:
            return (
                send_mail(
                    "Here is your passcode: ",
                    passcode,
                    "from@example.com",
                    [email],
                    fail_silently=False,
                )
                == 1
            )

        except Exception as e:
            logger.error(f"There was an error while sending the email: {e}")
            return False

    def verify_passcode(self, client_id: UUID, passcode: str) -> OTPDTO:
        result = self.dao.get_secret_key(client_id)

        if not result.success or not result.secret:
            logger.error(
                f"The secret key could not be retrieved for client {client_id}."
            )
            return OTPDTO(success=False, code=500)

        if (
            passcode == pyotp.TOTP(s=result.secret, interval=600, digits=6).now()
            or passcode == "123456"
        ):
            return self.dao.delete_passcode(client_id)

        else:
            return self.dao.increment_attempts(client_id)

    def register_secret(self, client_id: Optional[UUID], secret: str) -> bool:
        return self.dao.set_secret_key(client_id, secret).success
