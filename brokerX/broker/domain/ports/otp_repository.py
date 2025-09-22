from abc import ABC, abstractmethod

from ..entities.client import ClientProfile


class OTPRepository(ABC):
    @abstractmethod
    def create_passcode(self, client: ClientProfile):
        pass

    @abstractmethod
    def send_passcode(self, email: str, passcode: str) -> bool:
        pass

    @abstractmethod
    def verify_passcode(self, passcode: str, client: ClientProfile) -> bool:
        pass

    @abstractmethod
    def register_secret(self, email: str, secret: str):
        pass
