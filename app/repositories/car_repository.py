from typing import Sequence, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.core.db.db_session import get_async_session, get_sync_session
from app.models.models import Car

class CarRepositoryAsync:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> Sequence:
        result = await self.db.execute(
            select(Car)
        )

        return result.scalars().all()

    async def get_by_vin(self, vin: str) -> Optional[Car]:
        result = await self.db.execute(
            select(Car).where(Car.vin == vin)
        )

        return result.scalar_one_or_none()

    async def update_or_create(self, vin: str, payload: dict) -> Car:
        car_record = await self.get_by_vin(vin)

        if car_record:
            car_record.data = payload
        else:
            car_record = Car()
            car_record.vin = vin
            car_record.data = payload
            self.db.add(car_record)

        return car_record

class CarRepositorySync:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> Sequence:
        result = self.db.execute(
            select(Car)
        )

        return result.scalars().all()

    def get_by_vin(self, vin: str) -> Optional[Car]:
        result = self.db.execute(
            select(Car).where(Car.vin == vin)
        )

        return result.scalar_one_or_none()

    def update_or_create(self, vin: str, payload: dict) -> Car:
        car_record = self.get_by_vin(vin)

        if car_record:
            car_record.data = payload
        else:
            car_record = Car()
            car_record.vin = vin
            car_record.data = payload
            self.db.add(car_record)

        return car_record

def get_car_repository_async(db: AsyncSession = Depends(get_async_session)):
    return CarRepositoryAsync(db)

def get_car_repository_sync(db: Session = Depends(get_sync_session)):
    return CarRepositorySync(db)