"""Abstraction to hide exceptions from external sources (e.g DB connection)"""


class DataAccessException(Exception):
    def __init__(
        self,
        user_message: str = "There was an unexpected error.",
        error_code: int = 500,
    ):
        self.user_message = user_message
        self.error_code = error_code
        super().__init__(user_message)
