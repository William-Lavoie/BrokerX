from abc import ABC, abstractmethod
from dataclasses import dataclass

from client.adapters.result import Result


@dataclass
class OTPDTO(Result):
    secret: str = ""
    attempts: int = 0
    validated: bool = False


class OTPRepository(ABC):
    @abstractmethod
    def create_passcode(self, email: str) -> OTPDTO:
        pass

    @abstractmethod
    def send_passcode(self, email: str, passcode: str) -> bool:
        pass

    @abstractmethod
    def verify_passcode(self, email: str, passcode: str) -> OTPDTO:
        pass

    @abstractmethod
    def register_secret(self, email: str, secret: str) -> bool:
        pass
