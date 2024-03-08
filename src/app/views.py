"""
All get requests are handled here
"""

from src.app.service_layer import unit_of_work


def posts(post_id: str, uow: unit_of_work.SqlAlchemyUnitOfWork):
    """
    Get a post by its id, I think.
    """
    with uow:
        post = uow.posts.get(post_id)
        return post.to_dict()
