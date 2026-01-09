from __future__ import annotations

from app.application.common.exceptions.batch import InvalidSkuError
from app.application.common.ports.unit_of_work import AbstractUnitOfWork
from app.application.common.services import email
from app.domain.entities import Product, Batch, OrderLine
from app.domain.events.product import BatchCreatedEvent, AllocationRequiredEvent, BatchQuantityChangedEvent, OutOfStockEvent



def add_batch(
    event: BatchCreatedEvent,
    uow: AbstractUnitOfWork,
):
    with uow:
        product = uow.products.get(sku=event.sku)
        if product is None:
            product = Product(event.sku, batches=[])
            uow.products.add(product)
        product.batches.append(
            Batch(event.ref, event.sku, event.qty, event.eta)
        )
        uow.commit()


def allocate(
    event: AllocationRequiredEvent,
    uow: AbstractUnitOfWork,
) -> str | None:
    line = OrderLine(event.orderid, event.sku, event.qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSkuError(f"Invalid sku {line.sku}")
        batchref = product.allocate(line)
        uow.commit()
        return batchref


def change_batch_quantity(
    event: BatchQuantityChangedEvent,
    uow: AbstractUnitOfWork,
):
    with uow:
        product = uow.products.get_by_batchref(batchref=event.ref)
        product.change_batch_quantity(ref=event.ref, qty=event.qty)
        uow.commit()


# pylint: disable=unused-argument


def send_out_of_stock_notification(
    event: OutOfStockEvent,
    uow: AbstractUnitOfWork,
):
    email.send(
        "stock@made.com",
        f"Out of stock for {event.sku}",
    )