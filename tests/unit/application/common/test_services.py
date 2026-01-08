import pytest

from app.application.common.exceptions.batch import InvalidSkuError
from app.application.common.ports.product_repository import AbstractProductRepository
from app.application.common.ports.unit_of_work import AbstractUnitOfWork
from app.application.common.services import product_service

class FakeRepository(AbstractProductRepository):
    def __init__(self, products):
        self._products = set(products)

    def add(self, product):
        self._products.add(product)

    def get(self, sku):
        return next((p for p in self._products if p.sku == sku), None)


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.products = FakeRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass

def test_add_batch_for_new_product():
    uow = FakeUnitOfWork()
    product_service.add_batch("b1", "CRUNCHY-ARMCHAIR", 100, None, uow)
    assert uow.products.get("CRUNCHY-ARMCHAIR") is not None
    assert uow.committed


def test_allocate_returns_allocation():
    uow = FakeUnitOfWork()
    product_service.add_batch("batch1", "COMPLICATED-LAMP", 100, None, uow)
    result = product_service.allocate("o1", "COMPLICATED-LAMP", 10, uow)
    assert result == "batch1"


def test_allocate_errors_for_invalid_sku():
    uow = FakeUnitOfWork()
    product_service.add_batch("b1", "AREALSKU", 100, None, uow)

    with pytest.raises(InvalidSkuError, match="Invalid sku NONEXISTENTSKU"):
        product_service.allocate("o1", "NONEXISTENTSKU", 10, uow)


def test_commits():
    uow = FakeUnitOfWork()
    product_service.add_batch("b1", "OMINOUS-MIRROR", 100, None, uow)
    product_service.allocate("o1", "OMINOUS-MIRROR", 10, uow)
    assert uow.committed is True