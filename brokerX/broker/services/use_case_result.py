from dataclasses import dataclass


@dataclass
class UseCaseResult:
    success: bool
    message: str
