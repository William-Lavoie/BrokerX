from abc import abstractmethod

import pyotp

from ...domain.entities.user import User

class OTPRepository():
    @abstractmethod
    def send_passcode(self, email: str) -> None:
        pass

    @abstractmethod
    def verify_passcode(self, passcode: str, user: User) -> bool:
        pass

    def generate_passcode(self) -> pyotp.TOTP:
        user_secret = pyotp.random_base32()
        return pyotp.TOTP(s="abcdefghijklmnopqrstuvwxyz",
                            interval=600,
                            digits=6)

