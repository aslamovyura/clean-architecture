from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict
from starlette.requests import Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.application.common import services
from app.application.common.ports import repositories
from app.application.common.services import allocation
from app.domain import entities
from app.domain.exceptions.batch import OutOfStockError
from app.infrastructure.adapters.base_repository import SqlAlchemyRepository
from app.infrastructure.persistence_sqla.mappings import orm
from app.setup.config.settings import AppSettings


class AllocateRequestPydantic(BaseModel):
    model_config = ConfigDict(frozen=True)
    orderid: str
    sku: str
    qty: int


def create_allocation_router(settings: AppSettings) -> APIRouter:
    router = APIRouter()

    orm.map_tables()
    get_session = sessionmaker(bind=create_engine(settings.postgres.dsn))

    @router.post("/allocate")
    async def allocate_endpoint(request: AllocateRequestPydantic) -> dict[str, str]:
        session = get_session()
        repo = SqlAlchemyRepository(session)
        line = entities.OrderLine(request.orderid, request.sku, request.qty)

        try:
            batchref = allocation.allocate(line, repo, session)
        except (OutOfStockError, allocation.InvalidSkuError) as e:
            return {"message": str(e), "status": "400"}

        return {"batchref": batchref, "status": "201"}

    return router
