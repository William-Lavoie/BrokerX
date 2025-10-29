class UseCaseResult:
    def __init__(self, success: bool, message: str, code: int):
        self.success: bool = success
        self.message: str = message
        self.code: int = code

    def to_dict(self):
        return {"success": self.success, "message": self.message}
