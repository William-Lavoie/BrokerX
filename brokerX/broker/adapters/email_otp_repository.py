import logging

import pyotp
from django.core.mail import send_mail

from ..adapters.base_otp_repository import BaseOTPRepository
from ..domain.ports.otp_repository import OTPDTO
from .dao.mysql_client_otp_dao import MySQLClientOTPDAO

logger = logging.getLogger(__name__)


class EmailOTPRepository(BaseOTPRepository):
    def __init__(self, dao=None):
        super().__init__()
        self.dao = dao if dao is not None else MySQLClientOTPDAO()

    def send_passcode(self, email: str, passcode: str) -> bool:
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

    def verify_passcode(self, user_email: str, passcode: str) -> OTPDTO:
        result = self.dao.get_secret_key(user_email)

        if not result.success or not result.secret:
            logger.error(
                f"The secret key could not be retrieved for user {user_email}."
            )
            return OTPDTO(success=False, code=500)

        if passcode == pyotp.TOTP(s=result.secret, interval=600, digits=6).now():
            return self.dao.delete_passcode(user_email)

        else:
            return self.dao.increment_attempts(user_email)

    def register_secret(self, email: str, secret: str) -> bool:
        return self.dao.set_secret_key(email, secret).success
