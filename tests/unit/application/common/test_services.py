import pytest

from app.application.common.exceptions.batch import InvalidSkuError
from app.application.common.ports.repositories.base import AbstractRepository
from app.application.common.ports.unit_of_work import AbstractUnitOfWork
from app.application.common.services import allocation


class FakeRepository(AbstractRepository):
    def __init__(self, batches):
        self._batches = set(batches)

    def add(self, batch):
        self._batches.add(batch)

    def get(self, reference):
        return next(b for b in self._batches if b.reference == reference)

    def list(self):
        return list(self._batches)


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.batches = FakeRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


def test_add_batch():
    uow = FakeUnitOfWork()
    allocation.add_batch("b1", "CRUNCHY-ARMCHAIR", 100, None, uow)
    assert uow.batches.get("b1") is not None
    assert uow.committed


def test_allocate_returns_allocation():
    uow = FakeUnitOfWork()
    allocation.add_batch("batch1", "COMPLICATED-LAMP", 100, None, uow)
    result = allocation.allocate("o1", "COMPLICATED-LAMP", 10, uow)
    assert result == "batch1"


def test_allocate_errors_for_invalid_sku():
    uow = FakeUnitOfWork()
    allocation.add_batch("b1", "AREALSKU", 100, None, uow)

    with pytest.raises(InvalidSkuError, match="Invalid sku NONEXISTENTSKU"):
        allocation.allocate("o1", "NONEXISTENTSKU", 10, uow)


def test_commits():
    uow = FakeUnitOfWork()
    allocation.add_batch("b1", "OMINOUS-MIRROR", 100, None, uow)
    allocation.allocate("o1", "OMINOUS-MIRROR", 10, uow)
    assert uow.committed is True