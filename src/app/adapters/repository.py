"""
This module contains the AbstractRepository class and its subclasses.
"""

import abc
import datetime
import tempfile
import typing as t

from sqlalchemy import orm

from src.app.domain import model
import minio


class AbstractRepository(abc.ABC):
    def __init__(self):
        """
        Initialize the AbstractRepository class.
        """
        self.seen = set()  # type: set[model.Table]

    def add(self, r: model.Table) -> None:
        """
        Add a record to the repository.
        """
        self._add(r)
        self.seen.add(r)

    def get(self, id: str) -> model.Table:
        """
        Get a record from the repository by ID.
        """
        r = self._get(id)
        if r:
            self.seen.add(r)
        return r

    def edit(self, r: model.Table, _new: dict) -> None:
        """
        Edit a record in the repository.
        """
        self._edit(r, _new)
        self.seen.add(r)

    def delete(self, r: model.Table) -> None:
        """
        Delete a record from the repository.
        """
        self._delete(r)
        self.seen.remove(r)

    def query(self, **kwargs) -> list[model.Table]:
        """
        Query the repository.
        """
        rcs = self._query(**kwargs)
        self.seen.update(rcs)
        return rcs

    @property
    @abc.abstractmethod
    def _q(self):
        """
        Abstract method to add a record to the repository.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, r: model.Table):
        """
        Abstract method to add a record to the repository.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, id):
        """
        Abstract method to get a record from the repository by ID.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _edit(self, r: model.Table, _new: dict):
        """
        Abstract method to edit a record in the repository.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _delete(self, r: model.Table):
        """
        Abstract method to delete a record from the repository.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _query(self, **kwargs):
        """
        Abstract method to query the repository.
        """
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: orm.Session, model: t.Type[model.Table]):
        """
        Initialize the SqlAlchemyRepository class.
        """
        super().__init__()
        self.session = session
        self.model = model

    def _add(self, r: model.Table):
        """
        Add a record Table to the SQL Alchemy repository.
        """
        self.session.add(r)

    def _get(self, r_id: str) -> model.Table:
        """
        Get a record Table from the SQL Alchemy repository by ID.
        """
        _model = self.model
        return self.session.query(_model).filter_by(id=r_id).first()

    def _edit(self, r: model.Table, _new: dict) -> None:
        """
        Edit a record Table in the SQL Alchemy repository.
        """
        _model = self.model
        if isinstance(r, model.Post):
            r.title = _new["title"]
            r.content = _new["content"]
            r.version += 1
            r.updated_time = datetime.datetime.now()

    def _delete(self, r: model.Table) -> None:
        """
        Delete a record Table from the SQL Alchemy repository.
        """
        _model = self.model
        self.session.delete(r)

    def _query(self, **kwargs) -> list[model.Table]:
        """
        Query from SQL Alchemy repository.
        """
        _model = self.model
        return self.session.query(_model).filter_by(**kwargs).all()

    @property
    def _q(self) -> orm.query.Query:
        """
        Get the query object.
        Use to execute complex queries.
        """
        return self.session.query(self.model)


class MinioRepository(AbstractRepository):
    def __init__(self, client: minio.Minio):
        """
        Initialize the MinIOFileStorage class.
        """
        self.client = client
        super().__init__()

    def _add(self, f: tempfile.SpooledTemporaryFile):
        """
        Add a file to the FileStorage.
        """
        raise NotImplementedError

    def _get(self, path: str):
        """
        Get a presigned URL from the FileStorage by path.
        """
        raise NotImplementedError

    def _edit(self, path: str, f: tempfile.SpooledTemporaryFile):
        """
        Upload a replacement file to the FileStorage by path.
        """
        raise NotImplementedError

    def _delete(self, path: str):
        """
        Delete from the FileStorage by path.
        """
        raise NotImplementedError
