from app.application.common.ports.product_repository import AbstractProductRepository
from app.domain.entities import Product


class ProductRepository(AbstractProductRepository):
    def __init__(self, session):
        self.session = session

    def add(self, product):
        self.session.add(product)

    def get(self, sku):
        return self.session.query(Product).filter_by(sku=sku).one()