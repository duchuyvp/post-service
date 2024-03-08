from __future__ import annotations

import abc

from sqlalchemy import create_engine
from sqlalchemy import orm
from sqlalchemy.orm import session

from src.app import config
from src.app.adapters import repository


class AbstractUnitOfWork(abc.ABC):
    posts: repository.AbstractRepository
    comments: repository.AbstractRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    def collect_new_events(self):
        for post in self.posts.seen:
            while post.events:
                yield post.events.pop(0)

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


DEFAULT_SESSION_FACTORY = orm.sessionmaker(
    bind=create_engine(
        config.settings.POSTGRES_URI,
        isolation_level="REPEATABLE READ",
    )
)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.posts = repository.SqlAlchemyPostRepository(self.session)
        self.comments = repository.SqlAlchemyCommentRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
