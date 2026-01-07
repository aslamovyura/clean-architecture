from fastapi import APIRouter

from app.presentation.http.controllers.allocations.router import create_allocations_router
from app.presentation.http.controllers.general.router import create_general_router


def create_api_v1_router() -> APIRouter:
    router = APIRouter(prefix="/api/v1")
    router.include_router(create_general_router())
    router.include_router(create_allocations_router())
    return router
