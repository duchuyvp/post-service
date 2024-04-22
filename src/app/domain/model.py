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
        post_id: str | None,
        comment_id: str | None,
    ):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.post_id = post_id
        self.comment_id = comment_id
        self.events = []  # type: list[events.Event]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Like):
            return False
        return self.user_id == other.user_id and self.post_id == other.post_id and self.comment_id == other.comment_id

    def __repr__(self) -> str:
        return f"<Like {self.id}>"

    @staticmethod
    def create(user_id: str, post_id: str | None = None, comment_id: str | None = None) -> Like:
        if post_id is None and comment_id is None:
            raise ValueError("Cannot create a like without a post_id or comment_id")

        like = Like(user_id, post_id, comment_id)
        return like

    def delete(self) -> None:
        """ """

    def model_dump(self) -> dict:
        return {
            "id": str(self.id),
            "user_id": self.user_id,
            "post_id": self.post_id,
            "comment_id": self.comment_id,
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
        level: t.Literal[0, 1, 2, 3],
        post_id: str | None,
        comment_id: str | None,
    ):
        self.id = str(uuid.uuid4())
        self.content = content
        self.author_id = author_id
        self.level = level
        self.post_id = post_id
        self.comment_id = comment_id
        self.like_count = 0
        self.version = 1
        self.created_time = datetime.datetime.now()
        self.replies = []  # type: list[Comment]
        self.likes = []  # type: list[Like]
        self.events = []  # type: list[events.Event]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Comment):
            return False
        return self.id == other.id

    def __repr__(self) -> str:
        return f"<Comment {self.id}>"

    @staticmethod
    def create(
        content: str,
        author_id: str,
        level: t.Literal[0, 1, 2, 3],
        post_id: str | None = None,
        comment_id: str | None = None,
    ) -> Comment:
        if post_id is None and comment_id is None:
            raise ValueError("Cannot create a comment without a post_id or comment_id")

        if level not in [0, 1, 2, 3]:
            raise ValueError("level of a comment or reply must not exceed 3")

        if level != 0 and comment_id is None:
            raise ValueError("A reply must have a comment_id")

        comment = Comment(content, author_id, level, post_id, comment_id)
        return comment

    def __lt__(self, other: Comment) -> bool:
        return self.created_time < other.created_time

    def delete(self) -> None:
        """ """

    def like_unlike(self, user_id: str) -> None:
        like = Like.create(user_id, self.post_id, self.id)
        if like in self.likes:
            self.likes.remove(like)
            self.like_count -= 1
        else:
            self.likes.append(like)
            self.like_count += 1

    def reply(self, content: str, author_id: str) -> Comment:
        reply = Comment.create(content, author_id, t.cast(t.Literal[0, 1, 2, 3], self.level + 1), self.post_id, self.id)
        # self.replies.append(reply)
        return reply

    def can_edit_or_delete(self, user_id: str) -> bool:
        return user_id == self.author_id

    def model_dump(self) -> dict:
        return {
            "id": str(self.id),
            "content": self.content,
            "author_id": self.author_id,
            "level": self.level,
            "post_id": self.post_id,
            "comment_id": self.comment_id,
            "created_time": self.created_time.isoformat(),
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
        self.author_id = author_id
        self.like_count = 0
        self.version = 1
        self.created_time = datetime.datetime.now()
        self.updated_time = datetime.datetime.now()
        self.likes = []  # type: list[Like]
        self.comments = []  # type: list[Comment]
        self.events = []  # type: list[events.Event]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Post):
            return False
        return self.id == other.id

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
        like = Like.create(user_id, self.id, None)
        if like in self.likes:
            self.likes.remove(like)
            self.like_count -= 1
        else:
            self.likes.append(like)
            self.like_count += 1

    def comment(self, content: str, author_id: str) -> Comment:
        comment = Comment.create(content, author_id, 0, self.id, None)
        self.comments.append(comment)
        return comment

    def can_edit_or_delete(self, user_id: str) -> bool:
        return user_id == self.author_id

    def model_dump(self) -> dict:
        return {
            "id": str(self.id),
            "title": self.title,
            "author_id": self.author_id,
            "content": self.content,
            "like_count": self.like_count,
            "version": self.version,
            "created_time": self.created_time.isoformat(),
        }
