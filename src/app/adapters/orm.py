import logging

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import clear_mappers
from sqlalchemy.orm import registry

from src.app.domain import model

logger = logging.getLogger(__name__)


mapper_registry = registry()
metadata = mapper_registry.metadata


likes = sa.Table(
    "likes",
    metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("user_id", sa.String),
    sa.Column("post_id", sa.String, nullable=True),
    sa.Column("comment_id", sa.String, nullable=True),
    sa.Column("created_time", sa.TIMESTAMP),
)


comments = sa.Table(
    "comments",
    metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("content", sa.String),
    sa.Column("author_id", sa.String),
    sa.Column("level", sa.Integer),
    sa.Column("post_id", sa.String),
    sa.Column("comment_id", sa.String, nullable=True),
    sa.Column("like_count", sa.Integer),
    sa.Column("version", sa.Integer),
    sa.Column("created_time", sa.TIMESTAMP),
    sa.Column("updated_time", sa.TIMESTAMP),
)


posts = sa.Table(
    "posts",
    metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("title", sa.String),
    sa.Column("author_id", sa.String),
    sa.Column("content", sa.String),
    sa.Column("like_count", sa.Integer),
    sa.Column("version", sa.Integer),
    sa.Column("created_time", sa.TIMESTAMP),
    sa.Column("updated_time", sa.TIMESTAMP),
    sa.Column("images", sa.ARRAY(sa.String)),
)


def start_mappers() -> None:
    """
    This method starts the mappers.
    """

    # clean mapper
    clear_mappers()

    # logger.info("Starting mappers")
    like_mapper = mapper_registry.map_imperatively(
        class_=model.Like,
        local_table=likes,
    )

    comment_mapper = mapper_registry.map_imperatively(
        class_=model.Comment,
        local_table=comments,
    )

    post_mapper = mapper_registry.map_imperatively(
        class_=model.Post,
        local_table=posts,
    )

    comment_mapper.add_properties(
        {
            "replies": orm.relationship(
                argument=comment_mapper,
                primaryjoin=(comments.c.id == orm.foreign(comments.c.comment_id)),
                backref="comment",
                collection_class=list,
                lazy="select",
                remote_side=comments.c.id,
            ),
            "likes": orm.relationship(
                argument=like_mapper,
                primaryjoin=(comments.c.id == orm.foreign(likes.c.comment_id)),
                backref="comment",
                collection_class=list,
                lazy="select",
            ),
        }
    )

    post_mapper.add_properties(
        {
            "comments": orm.relationship(
                argument=comment_mapper,
                primaryjoin=(
                    sa.and_(
                        posts.c.id == orm.foreign(comments.c.post_id),
                        comments.c.comment_id.is_(None),
                    )
                ),
                backref="post",
                collection_class=list,
                lazy="select",
            ),
            "likes": orm.relationship(
                argument=like_mapper,
                primaryjoin=(posts.c.id == orm.foreign(likes.c.post_id)),
                backref="post",
                collection_class=list,
                lazy="select",
            ),
        }
    )

    # metadata.create_all(bind=sa.create_engine("postgresql://postgres:postgres@localhost:5432/db"))
