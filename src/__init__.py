from fastapi import APIRouter

from .guests.router import router as guests_router
from .tables.router import router as tables_router

api_routers = APIRouter()

