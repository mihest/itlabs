from fastapi import APIRouter

from .guests.router import router as guests_router
from .tables.router import router as tables_router

api_routers = APIRouter()


api_routers.include_router(
    guests_router,
    tags=["Guests"],
    prefix="/guests",
)

api_routers.include_router(
    tables_router,
    tags=["Tables"],
    prefix="/tables",
)