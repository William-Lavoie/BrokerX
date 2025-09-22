from ...domain.ports.otp_repository import OTPRepository
from ...domain.ports.client_repository import ClientRepository
from ...domain.entities.client import ClientProfile
from ..commands.create_client_command import CreateClientCommand


class CreateClientUseCase:
    def __init__(self, client_repository: ClientRepository, otp_repository: OTPRepository):
        self.client_repository = client_repository
        self.otp_repository = otp_repository

    def execute(self, command: CreateClientCommand):

        # Create new ClientProfile entity
        client = ClientProfile(
            first_name=command.first_name,
            last_name=command.last_name,
            address=command.address,
            birth_date=command.birth_date,
            email=command.email,
            phone_number=command.phone_number,
            status="pending",
        )

        # Save the new user
        if self.client_repository.add_user(client):
            print("the user was added with success")

        # Send passcode
        self.otp_repository.create_passcode(client)
