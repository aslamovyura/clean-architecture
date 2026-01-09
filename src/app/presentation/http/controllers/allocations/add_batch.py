from datetime import date, datetime
from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.application.common.services import product_service
from app.infrastructure.adapters.unit_of_work import UnitOfWork
from app.infrastructure.persistence_sqla.mappings import product
from app.setup.config.settings import AppSettings


class AddBatchRequestPydantic(BaseModel):
    model_config = ConfigDict(frozen=True)
    ref: str
    sku: str
    qty: int
    eta: Optional[date]


def create_add_batch_router(settings: AppSettings) -> APIRouter:
    router = APIRouter()

    get_session = sessionmaker(bind=create_engine(settings.postgres.dsn, isolation_level="REPEATABLE READ"))

    @router.post("/add_batch")
    async def add_batch_endpoint(request: AddBatchRequestPydantic) -> dict[str, str]:
        product_service.add_batch(request.ref, request.sku, request.qty, request.eta, 
                             UnitOfWork(get_session))

        return {"status": "201"}

    return router