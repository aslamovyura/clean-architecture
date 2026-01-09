import abc
from typing import Set

from app.domain.entities import Product


class AbstractProductRepository(abc.ABC):
    def __init__(self):
        self.seen = set()  # type: Set[Product]
    
    def add(self, product: Product):
        self._add(product)
        self.seen.add(product)

    def get(self, sku) -> Product:
        product = self._get(sku)
        if product:
            self.seen.add(product)
        return product
    
    def get_by_batchref(self, batchref) -> Product:
        product = self._get_by_batchref(batchref)
        if product:
            self.seen.add(product)
        return product
    
    
    @abc.abstractmethod
    def _add(self, product: Product):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, sku) -> Product:
        raise NotImplementedError
    
    @abc.abstractmethod
    def _get_by_batchref(self, batchref) -> Product:
        raise NotImplementedError
