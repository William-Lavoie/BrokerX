from ...domain.entities.user import UserStatus
from ...domain.ports.user_repository import UserRepository
from ...domain.ports.otp_repository import OTPRepository


class VerifyPassCode:
    def __init__(
        self,
        otp_repository: OTPRepository,
        user_repository: UserRepository,
    ):
        self.otp_repository = otp_repository
        self.user_repository = user_repository

    def execute(self, user_email: str, passcode: str):

        validated, message = self.otp_repository.verify_passcode(user_email, passcode)
        if not validated:
            print(message)
            return False

        print(message)
        self.user_repository.update_user_status(user_email, UserStatus.ACTIVE.value)
