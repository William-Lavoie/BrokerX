from abc import abstractmethod

from ....adapters.result import Result
from ....domain.entities.client import ClientProfile


class ClientDAO:

    # TODO: decouple the entities from the DAO
    @abstractmethod
    def add_user(self, client: ClientProfile) -> Result:
        pass

    @abstractmethod
    def update_status(self, client: ClientProfile) -> Result:
        pass

    @abstractmethod
    def get_status(self, email: str) -> Result:
        pass
