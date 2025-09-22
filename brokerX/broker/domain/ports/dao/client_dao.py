from abc import abstractmethod
from ....domain import ClientProfile


class ClientDAO:

    # TODO: decouple the entities from the DAO
    @abstractmethod
    def add_user(self, client: ClientProfile):
        pass

    @abstractmethod
    def update_status(self, client: ClientProfile):
        pass
