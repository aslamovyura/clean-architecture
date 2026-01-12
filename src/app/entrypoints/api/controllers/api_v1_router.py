from fastapi import APIRouter

from app.entrypoints.api.controllers.allocations.router import create_allocations_router
from app.entrypoints.api.controllers.general.router import create_general_router
from app.setup.config.settings import AppSettings


def create_api_v1_router(settings: AppSettings) -> APIRouter:
    router = APIRouter(prefix="/api/v1")
    router.include_router(create_general_router())
    router.include_router(create_allocations_router(settings))
    return router
