from ..adapters.dao.mysql_user_otp_dao import MySQLUserOTPDAO

from ..domain.entities.user import User
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

    def verify_passcode(self, passcode: str, user: User) -> bool:
        raise NotImplementedError

    def register_secret(self, user, secret):
        self.dao.set_secret_key(user, secret)
