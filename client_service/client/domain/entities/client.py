import logging
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from uuid import UUID

logger = logging.getLogger(__name__)


class ClientInvalidException(Exception):
    def __init__(
        self,
        user_message: str = "Your account has been deactivated or could not be found.",
        log_message: str = "Client instance was not found",
        error_code: int = 400,
    ):
        super().__init__(user_message)
        self.user_message = user_message
        self.log_message = log_message
        self.error_code = error_code


class ClientStatus(Enum):
    ACTIVE = "Active"
    PENDING = "Pending"
    REJECTED = "Rejected"


@dataclass
class Client:
    first_name: str
    last_name: str
    address: str
    birth_date: str
    email: str
    phone_number: str
    status: str
    client_id: Optional[UUID]
    password: str = ""

    def is_active(self) -> bool:
        return self.status == ClientStatus.ACTIVE.value

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address,
            "birth_date": self.birth_date,
            "email": self.email,
            "phone_number": self.phone_number,
            "status": self.status,
            "password": self.password,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            address=data.get("address", ""),
            birth_date=data.get("birth_date", ""),
            email=data.get("email", ""),
            phone_number=data.get("phone_number", ""),
            status=data.get("status", ""),
            password=data.get("password", ""),
        )
