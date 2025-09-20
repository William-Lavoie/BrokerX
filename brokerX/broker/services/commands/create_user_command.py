class CreateUserCommand():
    def __init__(self, first_name, last_name, address, birth_date, email, phone_number):
        self.first_name : str = first_name
        self.last_name = last_name
        self.address : str = address
        self.birth_date : str = birth_date
        self.email : str = email
        self.phone_number : str = phone_number