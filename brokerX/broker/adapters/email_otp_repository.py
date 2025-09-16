from abc import abstractmethod

from ..infrastructure.email_otp_manager import send_email_passcode
from ..domain.ports.otp_repository import OTPRepository
from ..domain.entities.user import User

class EmailOTPRepository(OTPRepository):
    def send_passcode(self, email: str) -> None:
        return send_email_passcode(email)


    @abstractmethod
    def verify_passcode(self, passcode: str, user: User) -> bool:
        pass
