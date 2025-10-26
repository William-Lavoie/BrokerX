from abc import abstractmethod
from dataclasses import dataclass

from ....domain.ports.otp_repository import OTPDTO


class ClientOTPDAO:
    @abstractmethod
    def set_secret_key(self, email: str, secret: str) -> OTPDTO:
        pass

    @abstractmethod
    def get_secret_key(self, email: str) -> OTPDTO:
        pass

    # TODO: use a database constraint instead?
    @abstractmethod
    def delete_passcode(self, email: str) -> OTPDTO:
        """Expire a passcode after 3 attemps, 10 mins or upon validation to prevent brute-forcing"""
        pass

    @abstractmethod
    def increment_attempts(self, email: str) -> OTPDTO:
        pass
