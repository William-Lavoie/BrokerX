from abc import abstractmethod

from ....adapters.result import Result
from ....domain.entities.client import ClientProfile, ClientStatus
from ....domain.ports.client_repository import ClientDTO


class ClientDAO:
    @abstractmethod
    def get_client_by_email(self, email: str) -> ClientDTO:
        pass

    # TODO: decouple the entities from the DAO
    @abstractmethod
    def add_user(self, client: ClientProfile) -> ClientDTO:
        pass

    @abstractmethod
    def update_status(self, email: str, new_status: str) -> ClientDTO:
        pass

    @abstractmethod
    def get_status(self, email: str) -> ClientDTO:
        pass
