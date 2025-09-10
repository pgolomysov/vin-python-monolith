from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.core.db.db_session import get_async_session, get_sync_session
from app.core.logging import logger
from app.core.redis.redis_client import RedisSyncClient, RedisAsyncClient
from app.events import base_event
from app.models import OutboxRelayer

redis_sync_client = RedisSyncClient()
redis_async_client = RedisAsyncClient()

class EventServiceAsync:
    def __init__(self, db: AsyncSession):
        self.db = db

    # TODO: make dispatch with callable
    async def dispatch(self, event: base_event):
        outbox_model = OutboxRelayer(payload=event.payload(), event_type=event.event_type())

        self.db.add(outbox_model)
        await self.db.commit()
        await self.db.refresh(outbox_model)

        logger.info(f"💾 Event saved: {str(event.event_type())}, with payload: {event.payload()}")

    async def push_to_channel(self, channel: str, payload: {}):
        await redis_async_client.push_event_to_channel(channel, payload)

class EventServiceSync:
    def __init__(self, db: Session):
        self.db = db

    # TODO: make dispatch with callable
    def dispatch(self, event: base_event):
        outbox_model = OutboxRelayer(payload=event.payload(), event_type=event.event_type())

        self.db.add(outbox_model)
        self.db.commit()
        self.db.refresh(outbox_model)

        logger.info(f"💾 Event saved: {str(event.event_type())}, with payload: {event.payload()}")

    def push_to_channel(self, channel: str, payload: {}):
        redis_sync_client.push_event_to_channel(channel, payload)

def get_async_event_service(db: Session = Depends(get_async_session)) -> EventServiceAsync:
    return EventServiceAsync(db)

def get_sync_event_service(db: Session = Depends(get_sync_session)) -> EventServiceSync:
    return EventServiceSync(db)