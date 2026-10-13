from fastapi import APIRouter

from api.v1.tenders.endpoints import tenders_router

api_v1_router = APIRouter(prefix="/v1")

api_v1_router.include_router(tenders_router)
