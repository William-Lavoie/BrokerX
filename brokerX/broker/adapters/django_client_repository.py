from ..adapters.redis.redis_client import (
    redis_get_client,
    redis_set_client,
    redis_update_client_status,
)
from ..domain.entities.client import Client, ClientInvalidException, ClientStatus
from ..domain.ports.client_repository import ClientRepository
from ..domain.ports.dao.client_dao import ClientDTO
from ..exceptions import DataAccessException
from .dao.mysql_client_dao import MySQLClientDAO


class DjangoClientRepository(ClientRepository):
    def __init__(self, dao=None):
        super().__init__()
        self.dao = dao if dao is not None else MySQLClientDAO()

    def get_client(self, email: str) -> Client:
        redis_client = redis_get_client(email=email)
        if redis_client:
            return redis_client

        else:
            client_dto: ClientDTO = self.dao.get_client_by_email(email)
            if not client_dto.success:
                if client_dto.code == 404:
                    raise ClientInvalidException(error_code=404)
                elif client_dto.code == 500:
                    raise DataAccessException(
                        user_message=f"An unexpected error occurred when trying to access client {email}"
                    )
            client = super().get_client_from_dto(client_dto)
            redis_set_client(client)

            return client

    def add_user(self, client: Client) -> ClientDTO:
        client_dto = self.dao.add_user(client)
        if client_dto.success:
            redis_set_client(client=client)

        return client_dto

    def update_user_status(self, email: str, new_status: str) -> ClientDTO:
        client_dto = self.dao.update_status(email, new_status)
        if client_dto.success:
            redis_update_client_status(email, new_status)

    def client_is_active(self, email: str) -> bool:
        redis_client = redis_get_client(email=email)
        if redis_client:
            return redis_client.status == ClientStatus.ACTIVE.value

        client_dto = self.dao.get_status(email)

        return client_dto.status == ClientStatus.ACTIVE.value
