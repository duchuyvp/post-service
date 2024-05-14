"""
All view requests are handled here
"""

from src.app.entrypoints import schema
from src.app.service_layer import unit_of_work


def get_post(post_id: str, uow: unit_of_work.AbstractUnitOfWork):
    """
    Get a post by its id, I think.
    """
    with uow.unit_of_work() as uow_ctx:
        post = uow_ctx.posts.get(post_id)
        return post.model_dump()


def find_post(title: str, uow: unit_of_work.AbstractUnitOfWork):
    """
    Find a post by its title.
    """
    with uow.unit_of_work() as uow_ctx:
        post = uow_ctx.posts.query(title=title)
        return [post.model_dump() for post in post]


def get_comments(post_id: str, uow: unit_of_work.AbstractUnitOfWork):
    """
    Get comments of a post.
    """
    with uow.unit_of_work() as uow_ctx:
        comments = uow_ctx.comments.query(post_id=post_id)
        return [comment.model_dump() for comment in comments]


def get_comment(comment_id: str, uow: unit_of_work.AbstractUnitOfWork):
    """
    Get a comment by its id.
    """
    with uow.unit_of_work() as uow_ctx:
        comment = uow_ctx.comments.get(comment_id)
        return comment.model_dump()


def get_reply_comments(comment_id: str, uow: unit_of_work.AbstractUnitOfWork):
    """
    Get reply comments of a comment.
    """
    with uow.unit_of_work() as uow_ctx:
        comments = uow_ctx.comments.query(comment_id=comment_id)
        return [comment.model_dump() for comment in comments]


def get_posts(params: schema.GetPostParamRequest, uow: unit_of_work.AbstractUnitOfWork):
    """
    Get all posts.
    """
    with uow.unit_of_work() as uow_ctx:
        post = uow_ctx.posts.model
        q = uow_ctx.posts._q

        if params.title is not None:
            q = q.filter(post.title.like(f"%{params.title}%"))

        if params.content is not None:
            q = q.filter(post.content.like(f"%{params.content}%"))

        if params.author_id is not None:
            q = q.filter(post.author_id == params.author_id)

        if len(params.order) > 0:
            q = q.order_by(
                *[
                    getattr(post, field[1:]).desc() if field.startswith("-") else getattr(post, field[1:]).asc()
                    for field in params.order
                    if field[1:] in post.__table__.columns.keys() and field[0] in ["-", "+"]
                ]
            )
        q = q.limit(params.limit).offset(params.offset)

        posts = q.all()
        return [post.model_dump() for post in posts]
