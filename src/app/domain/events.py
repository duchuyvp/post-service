import pydantic


class Event(pydantic.BaseModel):
    """
    Base class for events.
    """


class PostCreated(Event):
    """
    Event representing the creation of a post.
    """

    post_id: str
    title: str
    content: str
    author_id: str


class PostEdited(Event):
    """
    Event representing the editing of a post.
    """

    post_id: str
    title: str
    content: str
    version: int


class PostDeleted(Event):
    """
    Event representing the deletion of a post.
    """

    post_id: str


class PostLiked(Event):
    """
    Event representing a like on a post.
    """

    post_id: str
    user_id: str


class PostUnliked(Event):
    """
    Event representing an unlike on a post.
    """

    post_id: str
    user_id: str


class CommentCreated(Event):
    """
    Event representing a comment on a post.
    """

    comment_id: str
    post_id: str
    user_id: str
    content: str


class CommentDeleted(Event):
    """
    Event representing the deletion of a comment.
    """

    comment_id: str


class PostActionDenied(Event):
    """
    Event representing a denial of edit or delete a post.
    """

    post_id: str
    user_id: str


class CommentActionDenied(Event):
    """
    Event representing a denial of a comment delete.
    """

    comment_id: str
    user_id: str
