from fastapi import APIRouter

from app.presentation.http.controllers.general.router import create_general_router


def create_api_v1_router() -> APIRouter:
    router = APIRouter(prefix="/api/v1")
    router.include_router(create_general_router())
    return router
