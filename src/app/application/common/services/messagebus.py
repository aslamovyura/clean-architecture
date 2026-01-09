from typing import List, Dict, Callable, Type

from app.application.common.services.email_service import send_mail
from app.domain.events import Event, OutOfStockEvent


def handle(event: Event):
    for handler in HANDLERS[type(event)]:
        handler(event)


def send_out_of_stock_notification(event: OutOfStockEvent):
    send_mail(
        "stock@made.com",
        f"Out of stock for {event.sku}",
    )


HANDLERS = {
    OutOfStockEvent: [send_out_of_stock_notification],
}  # type: Dict[Type[Event], List[Callable]]