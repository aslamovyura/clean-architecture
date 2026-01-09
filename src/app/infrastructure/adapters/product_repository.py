from app.application.common.ports import AbstractProductRepository
from app.domain.entities import Product, Batch
from app.infrastructure.persistence_sqla.mappings import batches


class ProductRepository(AbstractProductRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, product):
        self.session.add(product)

    def _get(self, sku) -> Product | None:
        return (
            self.session.query(Product)
            .filter_by(sku=sku)
            .first()
        )
    
    def _get_by_batchref(self, batchref):
        return (
            self.session.query(Product)
            .join(Batch)
            .filter(batches.c.reference == batchref)
            .first()
        )