from fastapi import APIRouter
from api.routes import flipt

api_router = APIRouter()
api_router.include_router(flipt.router, prefix="/flipt", tags=["Flipt APIs"])
