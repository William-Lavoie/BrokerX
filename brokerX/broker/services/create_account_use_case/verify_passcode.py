from ...domain.ports.otp_repository import OTPRepository


class VerifyPassCode:
    def __init__(self, otp_repository: OTPRepository):
        self.otp_repository = otp_repository

    def execute(self, user_email: str, passcode: str):

        validated, message = self.otp_repository.verify_passcode(user_email, passcode)
        if not validated:
            print(message)
        print(message)
