from dataclasses import dataclass
from datetime import date
from threading import Event
from typing import Optional


@dataclass
class OutOfStockEvent(Event):
    sku: str