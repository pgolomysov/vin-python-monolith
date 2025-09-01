from fastapi import APIRouter, Depends

from app.repositories.car_repository import CarRepository

router = APIRouter()

@router.get("/cars")
async def test_db(
        cars_repository: CarRepository = Depends(CarRepository),
):
    cars = cars_repository.get_all()

    return {"cars": [{"vin": car.vin, "data": car.data, "created_at": car.created_at, "updated_at": car.created_at} for car in cars]}