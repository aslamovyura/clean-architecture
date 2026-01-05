from typing import List
from app.domain.entities import OrderLine, Batch
from app.domain.exceptions import OutOfStockError


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStockError(line.sku)