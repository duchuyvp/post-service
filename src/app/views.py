"""
All view requests are handled here
"""

from src.app.service_layer import unit_of_work


def get_post(post_id: str, uow: unit_of_work.SqlAlchemyUnitOfWork):
    """
    Get a post by its id, I think.
    """
    with uow:
        post = uow.posts.get(post_id)
        return post.model_dump()


def find_post(title: str, uow: unit_of_work.SqlAlchemyUnitOfWork):
    """
    Find a post by its title.
    """
    with uow:
        post = uow.posts.query(title=title)
        return [post.model_dump() for post in post]


def get_comments(post_id: str, uow: unit_of_work.SqlAlchemyUnitOfWork):
    """
    Get comments of a post.
    """
    with uow:
        comments = uow.comments.query(post_id=post_id)
        return [comment.model_dump() for comment in comments]
