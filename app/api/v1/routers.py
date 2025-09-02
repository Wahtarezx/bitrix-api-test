from fastapi import APIRouter
from .endpoints import router as leads_router

v1_router = APIRouter(prefix="/v1", tags=["v1"])

v1_router.include_router(leads_router)
