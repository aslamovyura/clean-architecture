from app.application.common.ports import AbstractProductRepository
from app.domain.entities import Product


class ProductRepository(AbstractProductRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, product):
        self.session.add(product)

    def _get(self, sku) -> Product | None:
        return self.session.query(Product).filter_by(sku=sku).first()