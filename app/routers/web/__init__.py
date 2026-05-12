from fastapi import APIRouter
from .views import router as views_router

web_router = APIRouter()
web_router.include_router(views_router)