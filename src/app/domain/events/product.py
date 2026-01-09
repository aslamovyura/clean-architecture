from dataclasses import dataclass
from datetime import date
from threading import Event
from typing import Optional


@dataclass
class BatchCreatedEvent(Event):
    ref: str
    sku: str
    qty: int
    eta: Optional[date] = None


@dataclass
class BatchQuantityChangedEvent(Event):
    ref: str
    qty: int


@dataclass
class AllocationRequiredEvent(Event):
    orderid: str
    sku: str
    qty: int


@dataclass
class OutOfStockEvent(Event):
    sku: str