from datetime import date, datetime
from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.application.common.services import allocation
from app.infrastructure.adapters.base_repository import SqlAlchemyRepository
from app.infrastructure.persistence_sqla.mappings import orm
from app.setup.config.settings import AppSettings


class AddBatchRequestPydantic(BaseModel):
    model_config = ConfigDict(frozen=True)
    ref: str
    sku: str
    qty: int
    eta: Optional[date]


def create_add_batch_router(settings: AppSettings) -> APIRouter:
    router = APIRouter()

    # orm.map_tables()
    get_session = sessionmaker(bind=create_engine(settings.postgres.dsn))

    @router.post("/add_batch")
    async def add_batch_endpoint(request: AddBatchRequestPydantic) -> dict[str, str]:
        session = get_session()
        repo = SqlAlchemyRepository(session)

        allocation.add_batch(request.ref, request.sku, request.qty, request.eta, repo, session)

        return {"status": "201"}

    return router