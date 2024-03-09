"""
This module contains the AbstractRepository class and its subclasses.
"""

import abc
import datetime
from src.app.adapters import orm
from src.app.domain import model


class AbstractRepository(abc.ABC):
    def __init__(self):
        """
        Initialize the AbstractRepository class.
        """
        self.seen = set()  # type: set[model.Table]

    def add(self, rc: model.Table) -> None:
        """
        Add a record to the repository.
        """
        self._add(rc)
        self.seen.add(rc)

    def get(self, id: str) -> model.Table:
        """
        Get a record from the repository by ID.
        """
        rc = self._get(id)
        if rc:
            self.seen.add(rc)
        return rc

    def edit(self, rc: model.Table, _new: dict) -> None:
        """
        Edit a record in the repository.
        """
        self._edit(rc, _new)
        self.seen.add(rc)

    def delete(self, rc: model.Table) -> None:
        """
        Delete a record from the repository.
        """
        self._delete(rc)
        self.seen.remove(rc)

    def query(self, **kwargs) -> list[model.Table]:
        """
        Query the repository.
        """
        rcs = self._query(**kwargs)
        self.seen.update(rcs)
        return rcs

    @abc.abstractmethod
    def _add(self, rc: model.Table):
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
    def _edit(self, rc: model.Table, _new: dict):
        """
        Abstract method to edit a record in the repository.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _delete(self, rc: model.Table):
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


class SqlAlchemyPostRepository(AbstractRepository):
    def __init__(self, session):
        """
        Initialize the SqlAlchemyRepository class.
        """
        super().__init__()
        self.session = session

    def _add(self, post):
        """
        Add a post to the SQL Alchemy repository.
        """
        self.session.add(post)

    def _get(self, post_id) -> model.Post:
        """
        Get a post from the SQL Alchemy repository by ID.
        """
        return self.session.query(model.Post).filter_by(id=post_id).first()

    def _edit(self, post: model.Post, _new: dict) -> None:
        """
        Edit a post in the SQL Alchemy repository.
        """

        post.title = _new["title"]
        post.content = _new["content"]
        post.version += 1
        post.updated_at = datetime.datetime.now()

    def _delete(self, post: model.Post) -> None:
        """
        Delete a post from the SQL Alchemy repository.
        """
        self.session.delete(post)

    def _query(self, **kwargs):
        """
        Query the SQL Alchemy repository.
        """
        return self.session.query(model.Post).filter_by(**kwargs).all()


class SqlAlchemyCommentRepository(AbstractRepository):

    def __init__(self, session):
        """
        Initialize the SqlAlchemyCommentRepository class.
        """
        super().__init__()
        self.session = session

    def _add(self, comment: model.Comment):
        """
        Add a comment to the SQL Alchemy repository.
        """
        self.session.add(comment)

    def _get(self, comment_id):
        """
        Get a comment from the SQL Alchemy repository by ID.
        """
        return self.session.query(model.Comment).filter_by(id=comment_id).first()

    def _delete(self, comment: model.Comment):
        """
        Delete a comment from the SQL Alchemy repository.
        """
        self.session.delete(comment)

    def _edit(self, comment: model.Comment, _new: dict):
        """
        Edit a comment in the SQL Alchemy repository.
        """
        raise NotImplementedError

    def _query(self, **kwargs):
        """
        Query the SQL Alchemy repository.
        """
        return self.session.query(model.Comment).filter_by(**kwargs).all()
