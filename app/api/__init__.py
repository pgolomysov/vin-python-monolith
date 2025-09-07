from fastapi import APIRouter
from app.controllers.health_controller import router as health_router
from app.controllers.cars_controller import router as cars_router
from app.controllers.requests_controller import router as requests_router

api_router = APIRouter()

api_router.include_router(health_router, prefix="/api")
api_router.include_router(cars_router, prefix="/api")
api_router.include_router(requests_router, prefix="/api")