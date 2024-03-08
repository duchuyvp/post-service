from __future__ import annotations
import abc
import datetime
import uuid

import pydantic
from src.app.domain import events, commands


class Table: ...


class MyClass(Table):
    def __init__(
        self,
        title: str,
        content: str,
        author_id: str,
        post_id: str = uuid.uuid4(),
    ):
        self._id = post_id
        self._title = title
        self._content = content
        self._created_at = datetime.datetime.now()
        self._updated_at = datetime.datetime.now()
        self._version = 0
        self._author_id = author_id
        self._likes = []  # type: list[str]
        self._comments = []  # type: list[Comment]
        self.events = []  # type: list[events.Event]

    def __eq__(self, other: Post) -> bool:
        if not isinstance(other, Post):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __repr__(self) -> str:
        return f"<Post {self._id} {self._title}>"


class Post(Table):
    """
    A post.
    Every attr and method is self-explanatory.
    """

    def __init__(
        self,
        title: str,
        content: str,
        author_id: str,
        post_id: str = uuid.uuid4(),
    ):
        self._id = post_id
        self._title = title
        self._content = content
        self._created_at = datetime.datetime.now()
        self._updated_at = datetime.datetime.now()
        self._version = 0
        self._author_id = author_id
        self._likes = []  # type: list[str]
        self._comments = []  # type: list[Comment]
        self.events = []  # type: list[events.Event]

    def __eq__(self, other: Post) -> bool:
        if not isinstance(other, Post):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __repr__(self) -> str:
        return f"<Post {self._id} {self._title}>"

    def edit(self, new_title: str, new_content: str) -> None:
        self._title = new_title
        self._content = new_content
        self._version += 1
        self._updated_at = datetime.datetime.now()
        self.events.append(events.PostEdited(post_id=self._id, title=new_title, content=new_content, version=self._version))

    @property
    def title(self) -> str:
        return self._title

    @property
    def content(self) -> str:
        return self._content

    @property
    def created_at(self) -> datetime.datetime:
        return self._created_at

    @property
    def version(self) -> int:
        return self._version

    @property
    def author_id(self) -> str:
        return self._author_id

    @staticmethod
    def create(title: str, content: str, author_id: str) -> Post:
        post = Post(title, content, author_id)
        post.events.append(events.PostCreated(post_id=post._id, title=title, content=content, author_id=author_id))
        return post

    def __lt__(self, other: Post) -> bool:
        return self._created_at < other._created_at

    def delete(self) -> None:
        self.events.append(events.PostDeleted(post_id=self._id))

    def like_unlike(self, user_id: str) -> None:
        if user_id in self._likes:
            self._likes.remove(user_id)
            self.events.append(events.PostUnliked(post_id=self._id, user_id=user_id))
        else:
            self._likes.append(user_id)
            self.events.append(events.PostLiked(post_id=self._id, user_id=user_id))

    def comment(self, content: str, author_id: str) -> Comment:
        comment = Comment.create(content, author_id, self._id)
        self._comments.append(comment)
        return comment

    def can_edit_or_delete(self, user_id: str) -> bool:
        return user_id == self._author_id


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
        comment_id: str = uuid.uuid4(),
        created_at: datetime.datetime = datetime.datetime.now(),
    ):
        self._id = comment_id
        self._content = content
        self._created_at = created_at
        self._post_id = post_id
        self._author_id = author_id
        self.events = []  # type: list[events.Event]

    def __eq__(self, other: Comment) -> bool:
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __repr__(self) -> str:
        return f"<Comment {self._id}>"

    @property
    def content(self) -> str:
        return self._content

    @property
    def created_at(self) -> datetime.datetime:
        return self._created_at

    @property
    def post_id(self) -> str:
        return self._post_id

    @property
    def author_id(self) -> str:
        return self._author_id

    @staticmethod
    def create(content: str, author_id: str, post_id: str) -> Comment:
        comment = Comment(content, author_id, post_id)
        comment.events.append(events.CommentCreated(comment_id=comment._id, content=content, author_id=author_id, post_id=post_id))
        return comment

    def __lt__(self, other: Comment) -> bool:
        return self._created_at < other._created_at

    def delete(self) -> None:
        self.events.append(events.CommentDeleted(comment_id=self._id))

    def can_edit_or_delete(self, user_id: str) -> bool:
        return user_id == self._author_id or user_id == self._post_id
