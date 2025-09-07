from fastapi import APIRouter, Depends

from app.repositories.car_repository import get_car_repository, CarRepository

router = APIRouter()

@router.get("/cars")
async def get_cars(cars_repository: CarRepository = Depends(get_car_repository)):
    cars = await cars_repository.get_all()

    return {
        "cars": [
            {
                "vin": car.vin,
                "data": car.data,
                "created_at": car.created_at,
                "updated_at": car.updated_at,
            }
            for car in cars
        ]
    }