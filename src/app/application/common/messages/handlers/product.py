from __future__ import annotations

from app.application.common.exceptions.batch import InvalidSkuError
from app.application.common.ports.unit_of_work import AbstractUnitOfWork
from app.application.common.services import email
from app.domain.commands.product import AllocateCommand, ChangeBatchQuantityCommand, CreateBatchCommand
from app.domain.entities import Product, Batch, OrderLine
from app.domain.events.product import OutOfStockEvent



def add_batch(
    cmd: CreateBatchCommand,
    uow: AbstractUnitOfWork,
):
    with uow:
        product = uow.products.get(sku=cmd.sku)
        if product is None:
            product = Product(cmd.sku, batches=[])
            uow.products.add(product)
        product.batches.append(
            Batch(cmd.ref, cmd.sku, cmd.qty, cmd.eta)
        )
        uow.commit()


def allocate(
    cmd: AllocateCommand,
    uow: AbstractUnitOfWork,
) -> str | None:
    line = OrderLine(cmd.orderid, cmd.sku, cmd.qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSkuError(f"Invalid sku {line.sku}")
        batchref = product.allocate(line)
        uow.commit()
        return batchref


def change_batch_quantity(
    cmd: ChangeBatchQuantityCommand,
    uow: AbstractUnitOfWork,
):
    with uow:
        product = uow.products.get_by_batchref(batchref=cmd.ref)
        product.change_batch_quantity(ref=cmd.ref, qty=cmd.qty)
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