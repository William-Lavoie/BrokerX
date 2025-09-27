from abc import ABC, abstractmethod
from dataclasses import dataclass

from ...adapters.result import Result
from ..entities.client import ClientProfile


@dataclass
class OTPDTO(Result):
    secret: str = ""
    attempts: int = 0


class OTPRepository(ABC):
    @abstractmethod
    def create_passcode(self, client: ClientProfile):
        pass

    @abstractmethod
    def send_passcode(self, email: str, passcode: str) -> bool:
        pass

    @abstractmethod
    def verify_passcode(self, email: str, passcode: str) -> bool:
        pass

    @abstractmethod
    def register_secret(self, email: str, secret: str):
        pass
