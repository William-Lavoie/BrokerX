from abc import abstractmethod
from uuid import UUID

from otp.domain.ports.otp_repository import OTPDTO


class OTPDAO:
    @abstractmethod
    def set_secret_key(self, client_id: UUID, secret: str) -> OTPDTO:
        pass

    @abstractmethod
    def get_secret_key(self, client_id: UUID) -> OTPDTO:
        pass

    @abstractmethod
    def delete_passcode(self, client_id: UUID) -> OTPDTO:
        pass

    @abstractmethod
    def increment_attempts(self, client_id: UUID) -> OTPDTO:
        pass
