import abc

from app.domain.entities import Product


class AbstractProductRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, product: Product):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, sku) -> Product:
        raise NotImplementedError