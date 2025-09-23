from abc import abstractmethod

from ....domain.entities.client import ClientProfile


class ClientDAO:

    # TODO: decouple the entities from the DAO
    @abstractmethod
    def add_user(self, client: ClientProfile) -> bool:
        pass

    @abstractmethod
    def update_status(self, client: ClientProfile):
        pass

    @abstractmethod
    def get_status(self, email: str) -> str:
        pass
