from ..domain.entities.client import ClientInvalidException, ClientProfile, ClientStatus
from ..domain.ports.client_repository import ClientRepository
from ..domain.ports.dao.client_dao import ClientDTO
from ..exceptions import DataAccessException
from .dao.mysql_client_dao import MySQLClientDAO


class DjangoClientRepository(ClientRepository):
    def __init__(self, dao=None):
        super().__init__()
        self.dao = dao if dao is not None else MySQLClientDAO()

    def get_user(self, email: str) -> ClientProfile:
        client_dto: ClientDTO = self.dao.get_client_by_email(email)
        if not client_dto.success:
            if client_dto.code == 404:
                raise ClientInvalidException(error_code=404)
            else:
                raise DataAccessException(
                    user_message=f"An unexpected error occurred when trying to access client {email}"
                )

        return super().get_client_from_dto(client_dto)

    def add_user(self, client: ClientProfile) -> ClientDTO:
        return self.dao.add_user(client)

    def update_user_status(self, email: str, new_status: str) -> ClientDTO:
        return self.dao.update_status(email, new_status)

    def client_is_active(self, email: str) -> bool:
        client_dto = self.dao.get_status(email)
        return client_dto.status == ClientStatus.ACTIVE.value
