import abc

from app.application.common.ports import AbstractProductRepository
from app.application.common.services import messagebus


class AbstractUnitOfWork(abc.ABC):
    products: AbstractProductRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()
        self.publish_events()


    def publish_events(self):
        for product in self.products.seen:
            if hasattr(product, 'events'):  # TODO: temporary solution.
                while product.events:
                    event = product.events.pop(0)
                    messagebus.handle(event)
        
        
    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError
    
    
    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError