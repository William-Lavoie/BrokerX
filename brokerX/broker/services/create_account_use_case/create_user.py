from ...domain.ports.otp_repository import OTPRepository
from ...domain.ports.user_repository import UserRepository
from ...domain.entities.user import User
from ..commands.create_user_command import CreateUserCommand


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository, otp_repository: OTPRepository):
        self.user_repository = user_repository
        self.otp_repository = otp_repository

    def execute(self, command: CreateUserCommand):

        # Create new User entity
        user = User(
            first_name=command.first_name,
            last_name=command.last_name,
            address=command.address,
            birth_date=command.birth_date,
            email=command.email,
            phone_number=command.phone_number,
            status="pending",
        )

        # Save the new user
        if self.user_repository.add_user(user):
            print("the user was added with success")

        # Send passcode
        self.otp_repository.create_passcode(user)
