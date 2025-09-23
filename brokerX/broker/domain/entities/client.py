from enum import Enum

# TODO: integrate with django user authentification class
# TODO: cronjob to delete users after 24h
# User refers strictly to django auth model


class ClientStatus(Enum):
    ACTIVE = "Active"
    PENDING = "Pending"
    REJECTED = "Rejected"


class ClientProfile:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        address: str,
        birth_date: str,
        email: str,
        phone_number: str,
        status: ClientStatus,
        password: str = "",
    ):
        self.first_name: str = first_name
        self.last_name = last_name
        self.address: str = address
        self.birth_date: str = birth_date
        self.email: str = email
        self.phone_number: str = phone_number
        self.status: ClientStatus = status
        self.password: str = password
