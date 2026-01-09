import abc

from app.application.common.ports import AbstractProductRepository
from app.application.common.messages import messagebus


class AbstractUnitOfWork(abc.ABC):
    products: AbstractProductRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    def collect_new_events(self):
        for product in self.products.seen:
            if hasattr(product, 'events'):  # TODO: temporary solution.
                while product.events:
                    yield product.events.pop(0) 
        
    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError
    
    
    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError