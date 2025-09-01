from datetime import timezone, datetime

from fastapi import Depends
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.events.base_event import BaseEvent
from app.models.models import Request, OutboxRelayer
from app.db.session import get_session


class OutboxRelayerRepository:
    def __init__(self, db: AsyncSession = Depends(get_session)):
        self.db = db

    async def get(self, count: int) -> list[OutboxRelayer] | None:
        result = await self.db.execute(
            select(OutboxRelayer)
            .where(OutboxRelayer.consumed_at.is_(None))
            .order_by(OutboxRelayer.id.asc())
            .limit(count)
            .with_for_update(skip_locked=True)
        )
        return result.scalars().all()

    async def mark_consumed(self, model: OutboxRelayer) -> Request | None:
        model.consumed_at = datetime.now(timezone.utc)