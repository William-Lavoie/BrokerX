from abc import abstractmethod
from dataclasses import dataclass
from decimal import Decimal

from client.adapters.result import Result
from client.domain.entities.client import Client


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
    def get_client(self, email: str) -> Client:
        pass

    @abstractmethod
    def add_user(
        self,
        first_name: str,
        last_name: str,
        birth_date: str,
        address: str,
        email: str,
        phone_number: str,
        status: str,
        password: str,
    ) -> Result:
        pass

    @abstractmethod
    def update_user_status(self, email: str, new_status: str) -> Result:
        pass

    @abstractmethod
    def client_is_active(self, email: str) -> bool:
        pass

    def get_client_from_dto(self, dto: ClientDTO) -> "Client":
        return Client(
            first_name=dto.first_name,
            last_name=dto.last_name,
            address=dto.address,
            birth_date=dto.birth_date,
            email=dto.email,
            phone_number=dto.phone_number,
            status=dto.status,
        )
