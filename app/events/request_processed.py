from typing import Any

from app.events.base_event import BaseEvent

class RequestProcessed(BaseEvent):
    def __init__(self, payload: dict[str, Any]):
        self._payload = payload or {}

    def event_type(self) -> str:
        return "public.request_processed"

    def payload(self) -> dict[str, Any]:
        return self._payload