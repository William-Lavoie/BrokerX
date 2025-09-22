from typing import Optional

from .dao.mysql_client_dao import MySQLClientDAO
from ..domain.ports.client_repository import ClientRepository
from ..domain.entities.client import ClientProfile


class DjangoClientRepository(ClientRepository):
    def __init__(self, dao=None):
        super().__init__()
        self.dao = dao if dao is not None else MySQLClientDAO()

    def add_user(self, client: ClientProfile) -> bool:
        return self.dao.add_user(client)

    def update_user_status(self, email: str, new_status: str):
        self.dao.update_status(email, new_status)

    def find_by_email(self, email: str) -> Optional[ClientProfile]:
        pass
