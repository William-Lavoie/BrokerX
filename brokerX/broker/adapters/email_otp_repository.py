import pyotp

from ..models import User
from ..adapters.dao.mysql_user_otp_dao import MySQLUserOTPDAO

from django.core.mail import send_mail
from ..adapters.base_otp_repository import BaseOTPRepository


class EmailOTPRepository(BaseOTPRepository):
    def __init__(self):
        super().__init__()
        self.dao = MySQLUserOTPDAO()

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

    def verify_passcode(self, user_email: str, passcode: str) -> {bool, str}:
        secret = self.dao.get_secret_key(user_email)

        if passcode == pyotp.TOTP(s=secret, interval=600, digits=6).now():
            self.dao.delete_passcode(user_email)
            return {True, "The passcode has been validated successfully."}

        else:
            if not self.dao.increment_attempts(user_email):
                return {False, "The maximum number of attempts has been reached"}
            return {False, "You have entered an incorrect passcode."}

    def register_secret(self, user: User, secret: str):
        self.dao.set_secret_key(user.email, secret)
