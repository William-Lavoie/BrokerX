from abc import abstractmethod
from dataclasses import dataclass

from ...adapters.result import Result
from ..entities.client import ClientProfile


@dataclass
class ClientDTO(Result):
    first_name: str = ""
    last_name: str = ""
    address: str = ""
    birth_date: str = ""
    email: str = ""
    phone_number: str = ""
    status: str = ""


class ClientRepository:
    @abstractmethod
    def get_user(self, email: str) -> ClientProfile:
        pass

    @abstractmethod
    def add_user(self, client: ClientProfile) -> Result:
        pass

    @abstractmethod
    def update_user_status(self, email: str, new_status: str) -> Result:
        pass

    @abstractmethod
    def client_is_active(self, email: str) -> bool:
        pass

    def get_client_from_dto(cls, dto: ClientDTO) -> "ClientProfile":
        return ClientProfile(
            dto.first_name,
            dto.last_name,
            dto.address,
            dto.birth_date,
            dto.email,
            dto.phone_number,
            dto.status,
        )
