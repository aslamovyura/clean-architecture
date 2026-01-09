from dataclasses import dataclass
from datetime import date
from typing import Optional
from app.domain.commands.base import Command


@dataclass
class AllocateCommand(Command):
    orderid: str
    sku: str
    qty: int


@dataclass
class CreateBatchCommand(Command):
    ref: str
    sku: str
    qty: int
    eta: Optional[date] = None


@dataclass
class ChangeBatchQuantityCommand(Command):
    ref: str
    qty: int