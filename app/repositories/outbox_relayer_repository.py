from datetime import timezone, datetime

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.models import Request, OutboxRelayer

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

async def get_outbox_relayer_repository(db: AsyncSession = Depends(get_session)):
    return OutboxRelayerRepository(db)