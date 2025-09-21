import pyotp

from ..domain.ports.otp_repository import OTPRepository

from ..domain.entities.user import User

# Base repositories contain methods common to all adapters of the same port
class BaseOTPRepository(OTPRepository):

    # Template pattern
    def create_passcode(self, user: User):
        secret = self.generate_passcode()
        passcode = pyotp.TOTP(s=secret, interval=600, digits=6)

        self.send_passcode(user.email, passcode.now())
        self.register_secret(user, secret)

    def generate_passcode(self) -> str:
        user_secret = pyotp.random_base32()
        return user_secret
