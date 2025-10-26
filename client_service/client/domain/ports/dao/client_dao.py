from abc import abstractmethod

from client.domain.ports.client_repository import ClientDTO


class ClientDAO:
    @abstractmethod
    def get_client_by_email(self, email: str) -> ClientDTO:
        pass

    @abstractmethod
    def add_user(
        self,
        first_name: str,
        last_name: str,
        birth_date: str,
        email: str,
        phone_number: str,
        address: str,
        status: str,
        password: str,
    ) -> ClientDTO:
        pass

    @abstractmethod
    def update_status(self, email: str, new_status: str) -> ClientDTO:
        pass

    @abstractmethod
    def get_status(self, email: str) -> ClientDTO:
        pass
