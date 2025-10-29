from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from client.adapters.result import Result


@dataclass
class OTPDTO(Result):
    secret: str = ""
    attempts: int = 0
    validated: bool = False


class OTPRepository(ABC):
    @abstractmethod
    def create_passcode(self, client_id: Optional[UUID], email: str) -> OTPDTO:
        pass

    @abstractmethod
    def send_passcode(
        self, client_id: Optional[UUID], email: str, passcode: str
    ) -> bool:
        pass

    @abstractmethod
    def verify_passcode(self, client_id: UUID, passcode: str) -> OTPDTO:
        pass

    @abstractmethod
    def register_secret(self, client_id: Optional[UUID], secret: str) -> bool:
        pass
