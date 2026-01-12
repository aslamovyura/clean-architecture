from fastapi import APIRouter

from app.entrypoints.api.controllers.allocations import (
    create_add_batch_router, 
    create_allocate_router
    )
from app.setup.config.settings import AppSettings


def create_allocations_router(settings: AppSettings) -> APIRouter:
    router = APIRouter(tags=["General"])
    router.include_router(create_allocate_router(settings))
    router.include_router(create_add_batch_router(settings))
    return router
