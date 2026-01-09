# pylint: disable=no-self-use
from datetime import date
from unittest import mock
import pytest

from app.application.common.exceptions.batch import InvalidSkuError
from app.application.common.messages import messagebus
from app.application.common.ports.product_repository import AbstractProductRepository
from app.application.common.ports.unit_of_work import AbstractUnitOfWork
from app.domain.commands.product import AllocateCommand, ChangeBatchQuantityCommand, CreateBatchCommand


class FakeRepository(AbstractProductRepository):
    def __init__(self, products):
        super().__init__()
        self._products = set(products)

    def _add(self, product):
        self._products.add(product)

    def _get(self, sku):
        return next((p for p in self._products if p.sku == sku), None)

    def _get_by_batchref(self, batchref):
        return next(
            (p for p in self._products for b in p.batches if b.reference == batchref),
            None,
        )


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.products = FakeRepository([])
        self.committed = False

    def _commit(self):
        self.committed = True

    def rollback(self):
        pass


class TestAddBatch:
    def test_for_new_product(self):
        uow = FakeUnitOfWork()
        messagebus.handle(
            CreateBatchCommand("b1", "CRUNCHY-ARMCHAIR", 100, None), uow
        )
        assert uow.products.get("CRUNCHY-ARMCHAIR") is not None
        assert uow.committed

    def test_for_existing_product(self):
        uow = FakeUnitOfWork()
        messagebus.handle(CreateBatchCommand("b1", "GARISH-RUG", 100, None), uow)
        messagebus.handle(CreateBatchCommand("b2", "GARISH-RUG", 99, None), uow)
        assert "b2" in [b.reference for b in uow.products.get("GARISH-RUG").batches]


class TestAllocate:
    def test_allocates(self):
        uow = FakeUnitOfWork()
        messagebus.handle(
            CreateBatchCommand("batch1", "COMPLICATED-LAMP", 100, None), uow
        )
        results = messagebus.handle(
            AllocateCommand("o1", "COMPLICATED-LAMP", 10), uow
        )
        assert results.pop(0) == "batch1"
        [batch] = uow.products.get("COMPLICATED-LAMP").batches
        assert batch.available_quantity == 90

    def test_errors_for_invalid_sku(self):
        uow = FakeUnitOfWork()
        messagebus.handle(CreateBatchCommand("b1", "AREALSKU", 100, None), uow)

        with pytest.raises(InvalidSkuError, match="Invalid sku NONEXISTENTSKU"):
            messagebus.handle(AllocateCommand("o1", "NONEXISTENTSKU", 10), uow)

    def test_commits(self):
        uow = FakeUnitOfWork()
        messagebus.handle(
            CreateBatchCommand("b1", "OMINOUS-MIRROR", 100, None), uow
        )
        messagebus.handle(AllocateCommand("o1", "OMINOUS-MIRROR", 10), uow)
        assert uow.committed

    def test_sends_email_on_out_of_stock_error(self):
        uow = FakeUnitOfWork()
        messagebus.handle(
            CreateBatchCommand("b1", "POPULAR-CURTAINS", 9, None), uow
        )

        with mock.patch("app.application.common.services.email.send") as mock_send_mail:
            messagebus.handle(AllocateCommand("o1", "POPULAR-CURTAINS", 10), uow)
            assert mock_send_mail.call_args == mock.call(
                "stock@made.com", f"Out of stock for POPULAR-CURTAINS"
            )


class TestChangeBatchQuantity:
    def test_changes_available_quantity(self):
        uow = FakeUnitOfWork()
        messagebus.handle(
            CreateBatchCommand("batch1", "ADORABLE-SETTEE", 100, None), uow
        )
        [batch] = uow.products.get(sku="ADORABLE-SETTEE").batches
        assert batch.available_quantity == 100

        messagebus.handle(ChangeBatchQuantityCommand("batch1", 50), uow)

        assert batch.available_quantity == 50

    def test_reallocates_if_necessary(self):
        uow = FakeUnitOfWork()
        history = [
            CreateBatchCommand("batch1", "INDIFFERENT-TABLE", 50, None),
            CreateBatchCommand("batch2", "INDIFFERENT-TABLE", 50, date.today()),
            AllocateCommand("order1", "INDIFFERENT-TABLE", 20),
            AllocateCommand("order2", "INDIFFERENT-TABLE", 20),
        ]
        for msg in history:
            messagebus.handle(msg, uow)
        [batch1, batch2] = uow.products.get(sku="INDIFFERENT-TABLE").batches
        assert batch1.available_quantity == 10
        assert batch2.available_quantity == 50

        messagebus.handle(ChangeBatchQuantityCommand("batch1", 25), uow)

        # order1 or order2 will be deallocated, so we'll have 25 - 20
        assert batch1.available_quantity == 5
        # and 20 will be reallocated to the next batch
        assert batch2.available_quantity == 30