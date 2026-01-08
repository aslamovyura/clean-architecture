from app.application.common.ports.unit_of_work import AbstractUnitOfWork
from app.infrastructure.adapters.base_repository import BatchRepository


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, 
                #  session_factory=DEFAULT_SESSION_FACTORY):
                 session_factory):
                 self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.batches = BatchRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()