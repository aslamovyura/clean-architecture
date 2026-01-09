from typing import List
from app.domain.entities.batch import OrderLine, Batch
from app.domain.events import Event, OutOfStockEvent
from app.domain.events.product import AllocationRequiredEvent

class Product:
    def __init__(self, sku: str, batches: List[Batch], version_number: int = 0):
        self.sku = sku
        self.batches = batches
        self.version_number = version_number
        self.events = []  # type: List[Event]

    def allocate(self, line: OrderLine) -> str | None:
        try:
            batch = next(b for b in sorted(self.batches) if b.can_allocate(line))
            batch.allocate(line)
            self.version_number += 1
            return batch.reference
        except StopIteration:
            self.events.append(OutOfStockEvent(line.sku))
            return None
        
    def change_batch_quantity(self, ref: str, qty: int):
        batch = next(b for b in self.batches if b.reference == ref)
        batch._purchased_quantity = qty
        while batch.available_quantity < 0:
            line = batch.deallocate_one()
            self.events.append(
                AllocationRequiredEvent(line.orderid, line.sku, line.qty)
            )