import pydantic


class Command(pydantic.BaseModel):
    """
    Base class for all commands.
    """


class CreatePostCommand(Command):
    """
    Command for creating a new post.
    """

    title: str
    content: str
    author_id: int


class EditPostCommand(Command):
    """
    Command for editing an existing post.
    """

    post_id: int
    title: str
    content: str


class LikePostCommand(Command):
    """
    Command for liking a post.
    """

    post_id: int
    user_id: int


class CommentPostCommand(Command):
    """
    Command for commenting on a post.
    """

    post_id: int
    user_id: int
    content: str


class DeletePostCommand(Command):
    """
    Command for deleting a post.
    """

    post_id: int
    user_id: int
