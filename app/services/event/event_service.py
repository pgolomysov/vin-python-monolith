from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import OutboxRelayer
from app.events import base_event
from app.core.db.db_session import get_async_session


class EventService:
    def __init__(self, db: AsyncSession = Depends(get_async_session)):
        self.db = db

    async def dispatch(self, event: base_event):
        outbox_model = OutboxRelayer(payload=event.payload(), event_type=event.event_type())

        self.db.add(outbox_model)
        await self.db.commit()
        await self.db.refresh(outbox_model)

