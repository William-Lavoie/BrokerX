"""
Event Handler base class
SPDX-License-Identifier: LGPL-3.0-or-later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict


class EventHandler(ABC):
    """Base class for all event handlers"""

    def __init__(self):
        """Constructor method"""
        self.logger = logging.getLogger("kafka")

    @abstractmethod
    def handle(self, event_data: Dict[str, Any]) -> None:
        """Process the event data"""
        pass

    @abstractmethod
    def get_event_type(self) -> str:
        """Return the event type this handler processes"""
        pass
