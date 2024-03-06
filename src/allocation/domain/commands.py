import pydantic


class Command(pydantic.BaseModel):
    """"""


class CreatePostCommand(Command):
    """"""

    title: str
    content: str
    author_id: int


class EditPostCommand(Command):
    """"""

    post_id: int
    title: str
    content: str


class LikePostCommand(Command):
    """"""

    post_id: int
    user_id: int


class CommentPostCommand(Command):
    """"""

    post_id: int
    user_id: int
    content: str


class DeletePostCommand(Command):
    """"""

    post_id: int
    user_id: int
