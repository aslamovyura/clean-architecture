import pytest

from app.application.common.exceptions.batch import InvalidSkuError
from app.application.common.ports.repositories.base import AbstractRepository
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


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True


def test_add_batch():
    repo, session = FakeRepository([]), FakeSession()
    allocation.add_batch("b1", "CRUNCHY-ARMCHAIR", 100, None, repo, session)
    assert repo.get("b1") is not None
    assert session.committed


def test_allocate_returns_allocation():
    repo, session = FakeRepository([]), FakeSession()
    allocation.add_batch("batch1", "COMPLICATED-LAMP", 100, None, repo, session)
    result = allocation.allocate("o1", "COMPLICATED-LAMP", 10, repo, session)
    assert result == "batch1"


def test_allocate_errors_for_invalid_sku():
    repo, session = FakeRepository([]), FakeSession()
    allocation.add_batch("b1", "AREALSKU", 100, None, repo, session)

    with pytest.raises(InvalidSkuError, match="Invalid sku NONEXISTENTSKU"):
        allocation.allocate("o1", "NONEXISTENTSKU", 10, repo, FakeSession())


def test_commits():
    repo, session = FakeRepository([]), FakeSession()
    session = FakeSession()
    allocation.add_batch("b1", "OMINOUS-MIRROR", 100, None, repo, session)
    allocation.allocate("o1", "OMINOUS-MIRROR", 10, repo, session)
    assert session.committed is True