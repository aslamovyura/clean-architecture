from fastapi import APIRouter

from app.presentation.http.controllers.allocations.allocation import create_allocation_router


def create_allocations_router() -> APIRouter:
    router = APIRouter(tags=["General"])
    router.include_router(create_allocation_router())
    return router
