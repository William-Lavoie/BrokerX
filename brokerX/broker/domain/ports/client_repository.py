from abc import abstractmethod

from ...adapters.result import Result
from ..entities.client import ClientProfile


class ClientRepository:
    @abstractmethod
    def add_user(self, client: ClientProfile) -> Result:
        pass

    @abstractmethod
    def update_user_status(self, email: str, new_status: str) -> Result:
        pass

    @abstractmethod
    def client_is_active(self, email: str) -> bool:
        pass
