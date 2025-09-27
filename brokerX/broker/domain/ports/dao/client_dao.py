from abc import abstractmethod
from dataclasses import dataclass

from ....adapters.result import Result
from ....domain.entities.client import ClientProfile


@dataclass
class ClientDTO(Result):
    status: str = ""


class ClientDAO:

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
