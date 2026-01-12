from fastapi import APIRouter

from app.entrypoints.api.controllers.general.health import (
    create_health_router,
)


def create_general_router() -> APIRouter:
    router = APIRouter(tags=["General"])
    router.include_router(create_health_router())
    return router
