from dataclasses import dataclass


@dataclass
class Result:
    """Generic result class to communicate between external sources and the service layer"""

    success: bool
    code: int
