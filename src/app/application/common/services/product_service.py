from __future__ import annotations
from datetime import date
from typing import Optional

from app.application.common.exceptions import InvalidSkuError
from app.application.common.ports import unit_of_work
from app.domain.entities import Product, Batch, OrderLine


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def add_batch(
    ref: str, sku: str, qty: int, eta: Optional[date],
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        product = uow.products.get(sku)
        if product is None:
            product = Product(sku, batches=[])
            uow.products.add(product)
        product.batches.append(Batch(ref, sku, qty, eta))
        uow.commit()


def allocate(
    orderid: str, sku: str, qty: int,
    uow: unit_of_work.AbstractUnitOfWork,
) -> str | None:
    line = OrderLine(orderid, sku, qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSkuError(f"Invalid sku {line.sku}")
        batchref = product.allocate(line)
        uow.commit()
    return batchref