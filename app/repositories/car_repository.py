from typing import Sequence, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.models import Car


class CarRepository:
    def __init__(self, db: AsyncSession = Depends(get_session)):
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

    async def update_or_create(self, vin: str, payload: dict or None) -> None:
        car_record = self.get_by_vin(vin)

        if car_record:
            car_record.data = payload
        else:
            car_record = Car()
            car_record.vin = vin
            car_record.data = payload
            self.db.add(car_record)