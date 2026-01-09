from __future__ import annotations
from typing import List, Dict, Callable, Type, TYPE_CHECKING

from app.application.common.messages.handlers.product import add_batch, allocate, change_batch_quantity, send_out_of_stock_notification
from app.application.common.ports.unit_of_work import AbstractUnitOfWork
from app.domain.events import Event, AllocationRequiredEvent, BatchCreatedEvent, BatchQuantityChangedEvent, OutOfStockEvent


def handle(
    event: Event,
    uow: AbstractUnitOfWork,
):
    results = []
    queue = [event]
    while queue:
        event = queue.pop(0)
        for handler in HANDLERS[type(event)]:
            results.append(handler(event, uow=uow))
            queue.extend(uow.collect_new_events())
    return results


HANDLERS = {
    BatchCreatedEvent: [add_batch],
    BatchQuantityChangedEvent: [change_batch_quantity],
    AllocationRequiredEvent: [allocate],
    OutOfStockEvent: [send_out_of_stock_notification],
}  # type: Dict[Type[Event], List[Callable]]