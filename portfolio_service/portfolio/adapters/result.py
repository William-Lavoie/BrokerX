from dataclasses import dataclass
from uuid import UUID


@dataclass
class Result:
    """Generic result class to communicate between external sources and the service layer"""
    client_id: UUID
    code: int
    success: bool = True
