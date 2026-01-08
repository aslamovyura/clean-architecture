from app.application.common.ports import AbstractUnitOfWork
from app.infrastructure.adapters import ProductRepository


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, 
                 session_factory):
                 self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.products = ProductRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()