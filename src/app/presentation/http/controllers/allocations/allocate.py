from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.application.common.exceptions.batch import InvalidSkuError
from app.application.common.messages import messagebus
from app.application.common.messages.handlers import product
from app.domain.events.product import AllocationRequiredEvent
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
    async def allocate_endpoint(request: AllocateRequestPydantic) -> dict[str, str | None]:
        try:
            event = AllocationRequiredEvent(request.orderid, request.sku, request.qty)
            results = messagebus.handle(event, UnitOfWork(get_session))
            batchref = results.pop(0)
        except InvalidSkuError as e:
            return {"message": str(e), "status": "400"}

        return {"batchref": batchref, "status": "201"}

    return router
