import fastapi
import pydantic


class Event(pydantic.BaseModel):
    """
    Base class for events.
    """


class CreatedPostEvent(Event):
    """
    Event representing the creation of a post.
    """

    post_id: str


class EditedPostEvent(Event):
    """
    Event representing the editing of a post.
    """

    post_id: str
    version: int


class DeletedPostEvent(Event):
    """
    Event representing the deletion of a post.
    """

    post_id: str


class LikedPostEvent(Event):
    """
    Event representing a like on a post.
    """

    post_id: str
    user_id: str


class UnlikedPostEvent(Event):
    """
    Event representing an unlike on a post.
    """

    post_id: str
    user_id: str


class LikedCommentEvent(Event):
    """
    Event representing a like on a comment.
    """

    comment_id: str
    user_id: str


class UnlikedCommentEvent(Event):
    """
    Event representing an unlike on a comment.
    """

    comment_id: str
    user_id: str


class CreatedCommentEvent(Event):
    """
    Event representing a comment on a post.
    """

    comment_id: str
    post_id: str


class RepliedCommentEvent(Event):
    """
    Event representing a reply to a comment.
    """

    comment_id: str
    post_id: str


class DeletedCommentEvent(Event):
    """
    Event representing the deletion of a comment.
    """

    comment_id: str


class DeniedPostActionEvent(Event):
    """
    Event representing a denial of edit or delete a post.
    """

    post_id: str
    user_id: str


class DeniedCommentActionEvent(Event):
    """
    Event representing a denial of a comment delete.
    """

    comment_id: str
    user_id: str
