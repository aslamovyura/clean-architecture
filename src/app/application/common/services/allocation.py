from __future__ import annotations
from datetime import date
from typing import Optional

from app.application.common.exceptions import InvalidSkuError
from app.application.common.ports.repositories.base import AbstractRepository
from app.domain import entities


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def add_batch(
    ref: str, sku: str, qty: int, eta: Optional[date],
    repo: AbstractRepository, session,
) -> None:
    repo.add(entities.Batch(ref, sku, qty, eta))
    session.commit()
    

def allocate(
    orderid: str, sku: str, qty: int,
    repo: AbstractRepository, session
) -> str:
    line = entities.OrderLine(orderid, sku, qty)
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSkuError(f"Invalid sku {line.sku}")
    batchref = entities.allocate(line, batches)
    session.commit()
    return batchref