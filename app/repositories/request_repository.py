from fastapi import Depends
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import Request
from app.core.db.db_session import get_async_session, get_sync_session


class RequestRepositoryAsync:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, uuid: UUID4, email: str, vin: str) -> Request | None:
        model = Request(uuid=uuid, email=email, vin=vin)
        self.db.add(model)

        return model

    async def get_by_uuid(self, uuid: UUID4) -> Request | None:
        result = await self.db.execute(
            select(Request).where(Request.uuid == str(uuid))
        )
        return result.scalar_one_or_none()

    def mark_as_done(self, record: Request) -> Request | None:
        record.done = True

class RequestRepositorySync:
    def __init__(self, db: Session):
        self.db = db

    def create(self, uuid: UUID4, email: str, vin: str) -> Request | None:
        model = Request(uuid=uuid, email=email, vin=vin)
        self.db.add(model)

        return model

    def get_by_uuid(self, uuid: UUID4) -> Request | None:
        result = self.db.execute(
            select(Request).where(Request.uuid == str(uuid))
        )
        return result.scalar_one_or_none()

    def mark_as_done(self, record: Request) -> Request | None:
        record.done = True

def get_request_repository_async(db: AsyncSession = Depends(get_async_session)):
    return RequestRepositoryAsync(db)

def get_request_repository_sync(db: Session = Depends(get_sync_session)):
    return RequestRepositorySync(db)