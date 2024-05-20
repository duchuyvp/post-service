import fastapi
import pydantic


class Event(pydantic.BaseModel):
    """
    Base class for events.
    """


class PostCreatedEvent(Event):
    """
    Event representing the creation of a post.
    """

    post_id: str
    images: list[fastapi.UploadFile]


class PostEditedEvent(Event):
    """
    Event representing the editing of a post.
    """

    post_id: str
    version: int


class PostDeletedEvent(Event):
    """
    Event representing the deletion of a post.
    """

    post_id: str


class PostLikedEvent(Event):
    """
    Event representing a like on a post.
    """

    post_id: str
    user_id: str


class PostUnlikedEvent(Event):
    """
    Event representing an unlike on a post.
    """

    post_id: str
    user_id: str


class CommentLikedEvent(Event):
    """
    Event representing a like on a comment.
    """

    comment_id: str
    user_id: str


class CommentUnlikedEvent(Event):
    """
    Event representing an unlike on a comment.
    """

    comment_id: str
    user_id: str


class CommentCreatedEvent(Event):
    """
    Event representing a comment on a post.
    """

    comment_id: str
    post_id: str


class CommentRepliedEvent(Event):
    """
    Event representing a reply to a comment.
    """

    comment_id: str
    post_id: str


class CommentDeletedEvent(Event):
    """
    Event representing the deletion of a comment.
    """

    comment_id: str


class PostActionDeniedEvent(Event):
    """
    Event representing a denial of edit or delete a post.
    """

    post_id: str
    user_id: str


class CommentActionDeniedEvent(Event):
    """
    Event representing a denial of a comment delete.
    """

    comment_id: str
    user_id: str
