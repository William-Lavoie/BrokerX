from abc import abstractmethod
from typing import Optional

from ..entities.client import ClientProfile


class ClientRepository:
    @abstractmethod
    def add_user(self, client: ClientProfile) -> None:
        pass

    @abstractmethod
    def update_user_status(self, email: str, new_status: str):
        pass

    @abstractmethod
    def client_is_active(self, email: str) -> str:
        pass
