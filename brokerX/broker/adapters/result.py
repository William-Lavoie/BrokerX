from dataclasses import dataclass
from typing import Any


@dataclass
class Result:
    """Generic result class to communicate between external sources and the service layer"""

    success: bool
    code: int = 0
    data: Any = None
