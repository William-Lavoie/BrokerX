class UseCaseResult:
    def __init__(self, message: str, code: int):
        self.message: str = message
        self.code: int = code

    def to_dict(self):
        return {"message": self.message}
