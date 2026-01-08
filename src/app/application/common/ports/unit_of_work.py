import abc

from app.application.common.ports.product_repository import AbstractProductRepository


class AbstractUnitOfWork(abc.ABC):
    products: AbstractProductRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError