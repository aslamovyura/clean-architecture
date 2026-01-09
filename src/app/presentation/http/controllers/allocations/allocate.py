from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.application.common.services import product_service
from app.domain.exceptions.batch import OutOfStockError
from app.infrastructure.adapters.unit_of_work import UnitOfWork
from app.setup.config.settings import AppSettings


class AllocateRequestPydantic(BaseModel):
    model_config = ConfigDict(frozen=True)
    orderid: str
    sku: str
    qty: int


def create_allocate_router(settings: AppSettings) -> APIRouter:
    router = APIRouter()

    get_session = sessionmaker(bind=create_engine(settings.postgres.dsn, isolation_level="REPEATABLE READ"))

    @router.post("/allocate")
    async def allocate_endpoint(request: AllocateRequestPydantic) -> dict[str, str]:
        try:
            batchref = product_service.allocate(request.orderid, request.sku, request.qty, UnitOfWork(get_session))
        except (OutOfStockError, product_service.InvalidSkuError) as e:
            return {"message": str(e), "status": "400"}

        return {"batchref": batchref, "status": "201"}

    return router
