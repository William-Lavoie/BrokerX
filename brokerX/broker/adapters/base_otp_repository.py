import pyotp

from ..domain.entities.client import Client
from ..domain.ports.otp_repository import OTPDTO, OTPRepository


# Base repositories contain methods common to all adapters of the same port
class BaseOTPRepository(OTPRepository):

    # Template pattern
    def create_passcode(self, client: Client) -> OTPDTO:
        secret = self.generate_passcode()
        passcode = pyotp.TOTP(s=secret, interval=600, digits=6)

        if not self.send_passcode(client.email, passcode.now()):
            return OTPDTO(success=False, code=500)

        if not self.register_secret(client.email, secret):
            return OTPDTO(success=False, code=500)

        return OTPDTO(success=True, code=201, secret=secret, attempts=0)

    def generate_passcode(self) -> str:
        user_secret = pyotp.random_base32()
        return user_secret
