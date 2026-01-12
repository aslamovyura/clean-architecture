from dataclasses import dataclass
from threading import Event


@dataclass
class OutOfStockEvent(Event):
    sku: str