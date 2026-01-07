from fastapi import APIRouter
from starlette.requests import Request


def create_allocation_router() -> APIRouter:
    router = APIRouter()

    @router.get("/allocate")
    async def allocate_endpoint(_: Request) -> dict[str, str]:
        """
        - Open to everyone.
        - Returns `200 OK` if the API is alive.
        """

        
        return {"status": "ok"}

    return router
