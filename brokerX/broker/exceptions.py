"""Abstraction to hide exceptions from external sources (e.g DB connection)"""


class DataAccessException(Exception):
    def __init__(self, user_message="There was an unexpected error.", error_code=500):
        self.error_code = error_code
        super().__init__(user_message)
