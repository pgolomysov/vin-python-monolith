from datetime import timezone, datetime

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db.db_session import get_sync_session
from app.models.models import Request, OutboxRelayer


class OutboxRelayerRepository:
    def __init__(self, db: get_sync_session()):
        self.db = db

    def get(self, count: int) -> list[OutboxRelayer] | None:
        result = self.db.execute(
            select(OutboxRelayer)
            .where(OutboxRelayer.consumed_at.is_(None))
            .order_by(OutboxRelayer.id.asc())
            .limit(count)
            .with_for_update(skip_locked=True)
        )

        return result.scalars().all()

    def mark_consumed(self, model: OutboxRelayer) -> Request | None:
        model.consumed_at = datetime.now(timezone.utc)

def get_outbox_relayer_repository(db: Session = Depends(get_sync_session)):
    return OutboxRelayerRepository(db)