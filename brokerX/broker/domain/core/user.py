from enum import Enum


class User:

    def __init__(self, name, address, birth_date, email, phone_number, status):
        self.name : str = name
        self.address : str = address
        self.birth_date : str = birth_date
        self.email : str = email
        self.phone_number : str = phone_number
        self.status : UserStatus = status

class UserStatus(Enum):
        ACTIVE = "active"
        PENDING  = "pending"
        REJECTED = "rejected"


