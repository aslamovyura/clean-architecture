from __future__ import annotations

from app.application.common.exceptions import InvalidSkuError
from app.application.common.ports.repositories.base import AbstractRepository
from app.domain import entities


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def allocate(line: entities.OrderLine, repo: AbstractRepository, session) -> str:
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSkuError(f"Invalid sku {line.sku}")
    batchref = entities.allocate(line, batches)
    session.commit()
    return batchref