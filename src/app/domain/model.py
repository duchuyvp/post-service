from __future__ import annotations

import abc
import datetime
import typing as t
import uuid

from src.app.domain import events


class Table:
    """
    A abstract table.
    """

    events: list[events.Event] = []

    @abc.abstractmethod
    def model_dump(self) -> dict:
        """Dump the model as a dictionary."""
        raise NotImplementedError


class Like(Table):
    """
    A like.
    Every attr and method is self-explanatory.
    """

    def __init__(
        self,
        user_id: str,
        source_id: str,
        source_type: t.Literal["post", "comment"],
    ):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.source_id = source_id
        self.source_type = source_type
        self.events = []  # type: list[events.Event]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Like):
            return False
        return (
            self.source_id == other.source_id
            and self.source_type == other.source_type
            and self.user_id == other.user_id
        )

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"<Like {self.id}>"

    @staticmethod
    def create(user_id: str, source_id: str, source_type: t.Literal["post", "comment"]) -> Like:
        like = Like(user_id, source_id, source_type)
        return like

    def delete(self) -> None:
        """ """

    def model_dump(self) -> dict:
        return {
            "id": str(self.id),
            "user_id": self.user_id,
            "source_id": self.source_id,
            "source_type": self.source_type,
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
        source_id: str,
        source_type: t.Literal["post", "comment"],
    ):
        self.id = str(uuid.uuid4())
        self.content = content
        self.created_time = datetime.datetime.now()
        self.source_id = source_id
        self.source_type = source_type
        self.author_id = author_id
        self.replies = []  # type: list[Comment]
        self.likes = []  # type: list[Like]
        self.like_count = 0
        self.events = []  # type: list[events.Event]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Comment):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"<Comment {self.id}>"

    @staticmethod
    def create(
        content: str, author_id: str, source_id: str, source_type: t.Literal["post", "comment"]
    ) -> Comment:
        comment = Comment(content, author_id, source_id, source_type)
        return comment

    def __lt__(self, other: Comment) -> bool:
        return self.created_time < other.created_time

    def delete(self) -> None:
        """ """

    def like_unlike(self, user_id: str) -> None:
        like = Like.create(user_id, self.id, "comment")
        if like in self.likes:
            self.likes.remove(like)
        else:
            self.likes.append(like)

    def can_edit_or_delete(self, user_id: str) -> bool:
        return user_id == self.author_id

    def model_dump(self) -> dict:
        return {
            "id": str(self.id),
            "content": self.content,
            "created_time": self.created_time.isoformat(),
            "author_id": self.author_id,
            "source_id": self.source_id,
            "source_type": self.source_type,
            "like_count": self.like_count,
        }


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
        self.created_time = datetime.datetime.now()
        self.updated_time = datetime.datetime.now()
        self.version = 1
        self.author_id = author_id
        self.like_count = 0
        self.likes = []  # type: list[Like]
        self.comments = []  # type: list[Comment]
        self.events = []  # type: list[events.Event]

    def __eq__(self, other: object) -> bool:
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
        self.updated_time = datetime.datetime.now()

    @staticmethod
    def create(title: str, content: str, author_id: str) -> Post:
        post = Post(title, content, author_id)
        return post

    def __lt__(self, other: Post) -> bool:
        return self.created_time < other.created_time

    def delete(self) -> None:
        """ """

    def like_unlike(self, user_id: str) -> None:
        like = Like.create(user_id, self.id, "post")
        if like in self.likes:
            self.likes.remove(like)
        else:
            self.likes.append(like)

    def comment(self, content: str, author_id: str) -> Comment:
        comment = Comment.create(content, author_id, self.id, "post")
        self.comments.append(comment)
        return comment

    def can_edit_or_delete(self, user_id: str) -> bool:
        return user_id == self.author_id

    def model_dump(self) -> dict:
        return {
            "id": str(self.id),
            "title": self.title,
            "content": self.content,
            "created_time": self.created_time.isoformat(),
            "author_id": self.author_id,
            # "likes": self.likes,
            "like_count": self.like_count,
            "version": self.version,
        }
