import copy
from enum import Enum


class User:

    def __init__(self, first_name, last_name, address, birth_date, email, phone_number, status):
        self.first_name : str = first_name
        self.last_name = last_name
        self.address : str = address
        self.birth_date : str = birth_date
        self.email : str = email
        self.phone_number : str = phone_number
        self.status : UserStatus = status

    def to_dict(self):
        return copy.copy(self.__dict__)

class UserStatus(Enum):
        ACTIVE = "active"
        PENDING  = "pending"
        REJECTED = "rejected"


