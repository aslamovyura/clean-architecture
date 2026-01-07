from fastapi import APIRouter

from app.presentation.http.controllers.allocations.allocation import create_allocation_router
from app.setup.config.settings import AppSettings


def create_allocations_router(settings: AppSettings) -> APIRouter:
    router = APIRouter(tags=["General"])
    router.include_router(create_allocation_router(settings))
    return router
