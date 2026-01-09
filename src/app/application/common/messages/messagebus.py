# pylint: disable=broad-except
from __future__ import annotations
import logging
from threading import Event
from typing import List, Dict, Callable, Type, Union
from app.application.common.messages.handlers.product import add_batch, allocate, change_batch_quantity, send_out_of_stock_notification
from app.application.common.ports.unit_of_work import AbstractUnitOfWork
from app.domain.commands.base import Command
from app.domain.commands.product import AllocateCommand, ChangeBatchQuantityCommand, CreateBatchCommand
from app.domain.events.product import OutOfStockEvent

logger = logging.getLogger(__name__)

Message = Union[Command, Event]


def handle(
    message: Message,
    uow: AbstractUnitOfWork,
):
    results = []
    queue = [message]
    while queue:
        message = queue.pop(0)
        if isinstance(message, Event):
            handle_event(message, queue, uow)
        elif isinstance(message, Command):
            cmd_result = handle_command(message, queue, uow)
            results.append(cmd_result)
        else:
            raise Exception(f"{message} was not an Event or Command")
    return results


def handle_event(
    event: Event,
    queue: List[Message],
    uow: AbstractUnitOfWork,
):
    for handler in EVENT_HANDLERS[type(event)]:
        try:
            logger.debug("handling event %s with handler %s", event, handler)
            handler(event, uow=uow)
            queue.extend(uow.collect_new_events())
        except Exception:
            logger.exception("Exception handling event %s", event)
            continue


def handle_command(
    command: Command,
    queue: List[Message],
    uow: AbstractUnitOfWork,
):
    logger.debug("handling command %s", command)
    try:
        handler = COMMAND_HANDLERS[type(command)]
        result = handler(command, uow=uow)
        queue.extend(uow.collect_new_events())
        return result
    except Exception:
        logger.exception("Exception handling command %s", command)
        raise


EVENT_HANDLERS = {
    OutOfStockEvent: [send_out_of_stock_notification],
}  # type: Dict[Type[Event], List[Callable]]

COMMAND_HANDLERS = {
    AllocateCommand: allocate,
    CreateBatchCommand: add_batch,
    ChangeBatchQuantityCommand: change_batch_quantity,
}  # type: Dict[Type[Command], Callable]