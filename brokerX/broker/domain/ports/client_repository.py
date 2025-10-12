from abc import abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal

from ...adapters.result import Result
from ...domain.entities.wallet import Wallet
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
    wallet: dict = field(default_factory=dict)
    shares: dict[str, int] = field(default_factory=dict)


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

    def get_client_from_dto(self, dto: ClientDTO) -> "ClientProfile":
        return ClientProfile(
            first_name=dto.first_name,
            last_name=dto.last_name,
            address=dto.address,
            birth_date=dto.birth_date,
            email=dto.email,
            phone_number=dto.phone_number,
            status=dto.status,
            wallet=Wallet(balance=dto.wallet.get("balance", Decimal("0.00"))),
            shares=dto.shares,
        )
