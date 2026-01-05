from typing import Any
from app.domain.exceptions.base import DomainError

class OutOfStockError(DomainError):
    def __init__(self, sku: Any) -> None:
        message = f"Out of stock for sku {sku}"
        super().__init__(message)
