import pyotp
from django.core.mail import send_mail

from ..adapters.base_otp_repository import BaseOTPRepository
from .dao.mysql_client_otp_dao import MySQLClientOTPDAO


class EmailOTPRepository(BaseOTPRepository):
    def __init__(self, dao=None):
        super().__init__()
        self.dao = dao if dao is not None else MySQLClientOTPDAO()

    def send_passcode(self, email: str, passcode: str) -> bool:
        return (
            send_mail(
                "Subject here",
                passcode,
                "from@example.com",
                [email],
                fail_silently=False,
            )
            == 1
        )

    def verify_passcode(self, user_email: str, passcode: str) -> bool:
        secret = self.dao.get_secret_key(user_email)
        print(secret)
        print(passcode)
        print(user_email)
        if passcode == pyotp.TOTP(s=secret, interval=600, digits=6).now():
            self.dao.delete_passcode(user_email)
            return True  # , "The passcode has been validated successfully."  #FIXME

        else:
            if not self.dao.increment_attempts(user_email):
                return False  # , "The maximum number of attempts has been reached"
            return False  # , "You have entered an incorrect passcode."

    def register_secret(self, email: str, secret: str):
        self.dao.set_secret_key(email, secret)
