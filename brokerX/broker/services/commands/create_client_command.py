class CreateClientCommand:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        address: str,
        birth_date: str,
        email: str,
        phone_number: str,
        password: str,
    ):
        self.first_name: str = first_name
        self.last_name = last_name
        self.address: str = address
        self.birth_date: str = birth_date
        self.email: str = email
        self.phone_number: str = phone_number
        self.password: str = password
