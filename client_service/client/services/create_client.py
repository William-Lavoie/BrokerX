from typing import Optional

from client.domain.entities.client import ClientInvalidException
from client.domain.ports.client_repository import ClientDTO, ClientRepository
from otp.domain.ports.otp_repository import OTPDTO, OTPRepository

from client_service.exceptions import DataAccessException
from client_service.use_case_results import UseCaseResult


class CreateClientUseCaseResult(UseCaseResult):
    def __init__(
        self, success: bool, message: str, code: int, client: Optional[dict] = None
    ):
        super().__init__(success=success, message=message, code=code)
        self.client: Optional[dict] = client

    def to_dict(self):
        dict = super().to_dict()
        if self.client is not None:
            dict.update(self.client)
        return dict


class CreateClientUseCase:
    def __init__(
        self, client_repository: ClientRepository, otp_repository: OTPRepository
    ):
        self.client_repository = client_repository
        self.otp_repository = otp_repository

    def execute(
        self,
        first_name: str,
        last_name: str,
        birth_date: str,
        email: str,
        phone_number: str,
        address: str,
        password: str,
    ) -> UseCaseResult:

        client_dto: ClientDTO = self.client_repository.add_user(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            email=email,
            address=address,
            phone_number=phone_number,
            password=password,
        )

        if not client_dto.success:
            if client_dto.code == 409:
                return UseCaseResult(
                    success=False,
                    message="There is already a user with the same email and/or phone number",
                    code=client_dto.code,
                )
            elif client_dto.code == 500:
                return UseCaseResult(
                    success=False,
                    message="There was an unexpected error. Please try again or contact customer support.",
                    code=client_dto.code,
                )

        otp_result: OTPDTO = self.otp_repository.create_passcode(
            client_id=client_dto.client_id, email=email
        )

        if not otp_result.success:
            return UseCaseResult(
                success=False,
                message="There was an error creating your passcode.",
                code=otp_result.code,
            )

        return UseCaseResult(
            success=True,
            message="The user was successfully created",
            code=otp_result.code,
        )

    def get_client_info(self, email: str):
        try:
            client = self.client_repository.get_client(email=email)
            return CreateClientUseCaseResult(
                success=True,
                message="The information was retrieved successfully.",
                code=200,
                client=client.to_dict(),
            )

        except ClientInvalidException as client_exception:
            return CreateClientUseCaseResult(
                success=False,
                message=client_exception.user_message,
                code=client_exception.error_code,
            )

        except DataAccessException as data_access_exception:
            return CreateClientUseCaseResult(
                success=False,
                message=data_access_exception.user_message,
                code=data_access_exception.error_code,
            )
