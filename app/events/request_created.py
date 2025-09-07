from typing import Any

from app.events.base_event import BaseEvent

class RequestCreated(BaseEvent):
    def __init__(self, payload: dict[str, Any]):
        self._payload = payload or {}

    def event_type(self) -> str:
        return "request_created"

    def payload(self) -> dict[str, Any]:
        return self._payload