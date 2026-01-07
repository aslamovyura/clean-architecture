from typing import Any
from app.application.common.exceptions import ApplicationError


class InvalidSkuError(ApplicationError):
    def __init__(self, sku: Any) -> None:
        message = f"Invalid SKU {sku}"
        super().__init__(message)