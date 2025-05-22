from fastapi import APIRouter

from .guests.router import router as guests_router
from .tables.router import router as tables_router
from .tables.router import router_stats as tables_stats_router

api_routers = APIRouter()


api_routers.include_router(
    guests_router,
    tags=["GuestLists"],
    prefix="/guest_lists",
)

api_routers.include_router(
    tables_router,
    tags=["Tables"],
    prefix="/tables",
)

api_routers.include_router(
    tables_stats_router,
    tags=["Tables"],
    prefix="/tables_stats",
)