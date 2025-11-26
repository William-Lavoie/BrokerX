"""
Handler registry
SPDX-License-Identifier: LGPL-3.0-or-later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import logging
from typing import Dict

from wallet.event_management.base_handler import EventHandler

logger = logging.getLogger("kafka")


class HandlerRegistry:
    """Registry for mapping event types to their handlers"""

    def __init__(self):
        self._handlers: Dict[str, EventHandler] = {}

    def register(self, handler: EventHandler) -> None:
        """Register a new event handler"""
        event_type = handler.get_event_type()
        self._handlers[event_type] = handler
        logger.debug(f"Handler enregistré pour le type: {event_type}")

    def get_handler(self, event_type: str) -> EventHandler:
        """Get handler for a specific event type"""
        return self._handlers.get(event_type)

    def has_handler(self, event_type: str) -> bool:
        """Check if a handler exists for an event type"""
        return event_type in self._handlers

    def get_supported_events(self) -> list:
        """Get list of supported event types"""
        return list(self._handlers.keys())
