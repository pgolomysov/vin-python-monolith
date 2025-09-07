from fastapi import Depends
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models import Request
from app.db.session import get_session

class RequestRepository:
    def __init__(self, db: AsyncSession = Depends(get_session)):
        self.db = db

    def create(self, uuid: UUID4, email: str, vin: str) -> Request | None:
        model = Request(uuid=uuid, email=email, vin=vin)
        self.db.add(model)

        return model

    async def get_by_uuid(self, uuid: UUID4) -> Request | None:
        result = await self.db.execute(
            select(Request).where(Request.uuid == str(uuid))
        )
        return result.scalar_one_or_none()

    async def mark_as_done(self, record: Request) -> Request | None:
        record.done = True

async def get_request_repository(db: AsyncSession = Depends(get_session)):
    return RequestRepository(db)