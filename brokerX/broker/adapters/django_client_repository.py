from ..adapters.result import Result
from ..domain.entities.client import ClientProfile, ClientStatus
from ..domain.ports.client_repository import ClientRepository
from .dao.mysql_client_dao import MySQLClientDAO


class DjangoClientRepository(ClientRepository):
    def __init__(self, dao=None):
        super().__init__()
        self.dao = dao if dao is not None else MySQLClientDAO()

    def add_user(self, client: ClientProfile) -> Result:
        return self.dao.add_user(client)

    def update_user_status(self, email: str, new_status: str) -> Result:
        return self.dao.update_status(email, new_status)

    def client_is_active(self, email: str) -> bool:
        return self.dao.get_status(email).data == ClientStatus.ACTIVE.value
