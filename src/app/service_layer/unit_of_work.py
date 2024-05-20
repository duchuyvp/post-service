from __future__ import annotations

import abc
import contextlib

import minio
from sqlalchemy import create_engine
from sqlalchemy import orm

from src.app.config import settings
from src.app.adapters import repository
from src.app.domain import model


class AbstractUnitOfWork(abc.ABC):
    posts: repository.AbstractRepository
    comments: repository.AbstractRepository
    fileStorage: repository.AbstractRepository

    @contextlib.contextmanager
    def unit_of_work(self):
        yield self

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


POSTGRES_URI = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
DEFAULT_SESSION_FACTORY = orm.sessionmaker(
    bind=create_engine(
        POSTGRES_URI,
        isolation_level="REPEATABLE READ",
    )
)
DEFAUL_MINIO_CLIENT = minio.Minio(
    endpoint=f"{settings.MINIO_HOST}:{settings.MINIO_PORT}",
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    @contextlib.contextmanager
    def unit_of_work(self):
        try:
            self.session = self.session_factory()
            self.posts = repository.SqlAlchemyRepository(self.session, model.Post)
            self.comments = repository.SqlAlchemyRepository(self.session, model.Comment)
            self.minio = repository.MinioRepository(DEFAUL_MINIO_CLIENT)
            yield self
        except:
            self.rollback()
            raise
        finally:
            self.session.close()

    def __enter__(self):
        self.session = self.session_factory()
        self.posts = repository.SqlAlchemyRepository(self.session, model.Post)
        self.comments = repository.SqlAlchemyRepository(self.session, model.Comment)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
