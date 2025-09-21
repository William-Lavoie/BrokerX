from abc import ABC, abstractmethod

from ...domain.entities.user import User


class OTPRepository(ABC):
    @abstractmethod
    def create_passcode(self, user: User):
        pass

    @abstractmethod
    def send_passcode(self, email: str, passcode: str) -> bool:
        pass

    @abstractmethod
    def verify_passcode(self, passcode: str, user: User) -> bool:
        pass

    @abstractmethod
    def register_secret(self, user: User, secret: str):
        pass
