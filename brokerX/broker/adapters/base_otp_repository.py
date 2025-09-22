import pyotp

from ..domain.ports.otp_repository import OTPRepository

from ..domain.entities.client import ClientProfile

# Base repositories contain methods common to all adapters of the same port
class BaseOTPRepository(OTPRepository):

    # Template pattern
    def create_passcode(self, client: ClientProfile):
        secret = self.generate_passcode()
        passcode = pyotp.TOTP(s=secret, interval=600, digits=6)

        self.send_passcode(client.email, passcode.now())
        self.register_secret(client, secret)

    def generate_passcode(self) -> str:
        user_secret = pyotp.random_base32()
        return user_secret
