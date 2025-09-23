from ...domain.entities.client import ClientStatus
from ...domain.ports.client_repository import ClientRepository
from ...domain.ports.otp_repository import OTPRepository


class VerifyPassCode:
    def __init__(
        self,
        otp_repository: OTPRepository,
        client_repository: ClientRepository,
    ):
        self.otp_repository = otp_repository
        self.client_repository = client_repository

    def execute(self, email: str, passcode: str):

        validated: bool = self.otp_repository.verify_passcode(email, passcode)
        if not validated:
            return False

        self.client_repository.update_user_status(email, ClientStatus.ACTIVE.value)
        return True
