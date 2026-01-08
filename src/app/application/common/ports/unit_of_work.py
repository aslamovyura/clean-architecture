import abc

from app.application.common.ports.repositories.base import AbstractRepository


class AbstractUnitOfWork(abc.ABC):
    batches: AbstractRepository

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