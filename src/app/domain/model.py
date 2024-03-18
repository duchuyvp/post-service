from __future__ import annotations

import abc
import datetime
import uuid

import pydantic

from src.app.domain import commands
from src.app.domain import events


class Table:
    """
    A abstract table.
    """

    events = []  # type: list[events.Event]

    @abc.abstractmethod
    def model_dump(self) -> dict:
        """Dump the model as a dictionary."""
        raise NotImplementedError


class Post(Table):
    """
    A post.
    Every attr and method is self-explanatory.
    """

    comments = []  # type: list[Comment]

    def __init__(
        self,
        title: str,
        content: str,
        author_id: str,
    ):
        self.id = str(uuid.uuid4())
        self.title = title
        self.content = content
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.version = 1
        self.author_id = author_id
        self.likes = []  # type: list[str]
        self.events = []  # type: list[events.Event]

    def __eq__(self, other: Post) -> bool:
        if not isinstance(other, Post):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"<Post {self.id} {self.title}>"

    def edit(self, new_title: str, new_content: str) -> None:
        self.title = new_title
        self.content = new_content
        self.version += 1
        self.updated_at = datetime.datetime.now()

    @staticmethod
    def create(title: str, content: str, author_id: str) -> Post:
        post = Post(title, content, author_id)
        return post

    def __lt__(self, other: Post) -> bool:
        return self.created_at < other.created_at

    def delete(self) -> None:
        """ """

    def like_unlike(self, user_id: str) -> None:
        if user_id in self.likes:
            self.likes.remove(user_id)
        else:
            self.likes.append(user_id)

    def comment(self, content: str, author_id: str) -> Comment:
        comment = Comment.create(content, author_id, self.id)
        self.comments.append(comment)
        return comment

    def can_edit_or_delete(self, user_id: str) -> bool:
        return user_id == self.author_id

    def model_dump(self) -> dict:
        return {
            "id": str(self.id),
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "author_id": self.author_id,
            "likes": self.likes,
            "version": self.version,
        }


class Comment(Table):
    """
    A comment.
    Every attr and method is self-explanatory.
    """

    def __init__(
        self,
        content: str,
        author_id: str,
        post_id: str,
        created_at: datetime.datetime = datetime.datetime.now(),
    ):
        self.id = str(uuid.uuid4())
        self.content = content
        self.created_at = created_at
        self.post_id = post_id
        self.author_id = author_id
        self.events = []  # type: list[events.Event]

    def __eq__(self, other: Comment) -> bool:
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"<Comment {self.id}>"

    @staticmethod
    def create(content: str, author_id: str, post_id: str) -> Comment:
        comment = Comment(content, author_id, post_id)
        return comment

    def __lt__(self, other: Comment) -> bool:
        return self.created_at < other.created_at

    def delete(self) -> None:
        """ """

    def can_edit_or_delete(self, user_id: str) -> bool:
        return user_id == self.author_id or user_id == self.post_id

    def model_dump(self) -> dict:
        return {
            "id": str(self.id),
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "author_id": self.author_id,
            "post_id": self.post_id,
        }
