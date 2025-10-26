from client.adapters.dao.mysql_client_dao import MySQLClientDAO
from client.adapters.redis.redis_client import RedisClient

#
from client.domain.entities.client import Client, ClientInvalidException, ClientStatus
from client.domain.ports.client_repository import ClientRepository
from client.domain.ports.dao.client_dao import ClientDTO

from client_service.exceptions import DataAccessException


class DjangoClientRepository(ClientRepository):
    def __init__(self, dao=None, redis=None):
        super().__init__()
        self.dao = dao if dao is not None else MySQLClientDAO()
        self.redis = redis if redis is not None else RedisClient()

    def get_client(self, email: str) -> Client:
        redis_client = self.redis.get_client(email=email)
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
            self.redis.set_client(client)

            return client

    def add_user(
        self,
        first_name: str,
        last_name: str,
        birth_date: str,
        address: str,
        email: str,
        phone_number: str,
        status: str,
        password: str,
    ) -> ClientDTO:

        client_dto = self.dao.add_user(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            email=email,
            address=address,
            phone_number=phone_number,
            status=status,
            password=password,
        )
        if client_dto.success:
            client = Client(
                first_name=first_name,
                last_name=last_name,
                birth_date=birth_date,
                email=email,
                address=address,
                phone_number=phone_number,
                status=status,
                client_id=client_dto.client_id,
            )
            self.redis.set_client(client=client)

        return client_dto

    def update_user_status(self, email: str, new_status: str) -> ClientDTO:
        client_dto = self.dao.update_status(email, new_status)
        if client_dto.success:
            self.redis.update_client_status(email, new_status)

        return client_dto

    def client_is_active(self, email: str) -> bool:
        redis_client: Client = self.redis.get_client(email=email)
        if redis_client:
            return redis_client.status == ClientStatus.ACTIVE.value

        client_dto: ClientDTO = self.dao.get_status(email)

        return client_dto.status == ClientStatus.ACTIVE.value
