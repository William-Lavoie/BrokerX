from abc import abstractmethod

from ..domain.ports.otp_repository import OTPRepository
from ..domain.entities.user import User
from django.core.mail import send_mail

class EmailOTPRepository(OTPRepository):
    def send_passcode(self, email: str) -> None:
        passcode = self.generate_passcode()
        send_mail(
            "Subject here",
            passcode.now(),
            "from@example.com",
            [email],
            fail_silently=False,
        )

    @abstractmethod
    def verify_passcode(self, passcode: str, user: User) -> bool:
        pass
