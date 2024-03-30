import json
import logging

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import registry
from src.app.adapters import orm_helper

from src.app.domain import model

logger = logging.getLogger(__name__)


mapper_registry = registry()
metadata = mapper_registry.metadata

comments = sa.Table(
    "comments",
    metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("post_id", sa.String, sa.ForeignKey("posts.id")),
    sa.Column("content", sa.String),
    sa.Column("created_at", sa.TIMESTAMP),
    sa.Column("updated_at", sa.TIMESTAMP),
    sa.Column("version", sa.Integer),
    sa.Column("author_id", sa.String),
)


posts = sa.Table(
    "posts",
    metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("title", sa.String),
    sa.Column("content", sa.String),
    sa.Column("created_at", sa.TIMESTAMP),
    sa.Column("updated_at", sa.TIMESTAMP),
    sa.Column("version", sa.Integer),
    sa.Column("author_id", sa.String),
)

likes = sa.Table(
    "likes",
    metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("post_id", sa.String, sa.ForeignKey("posts.id")),
    sa.Column("user_id", sa.String),
)


def start_mappers() -> None:
    """
    This method starts the mappers.
    """
    # logger.info("Starting mappers")
    comment_mapper = mapper_registry.map_imperatively(
        class_=model.Comment,
        local_table=comments,
    )

    like_mapper = mapper_registry.map_imperatively(
        class_=model.Like,
        local_table=likes,
    )

    mapper_registry.map_imperatively(
        class_=model.Post,
        local_table=posts,
        properties={
            "comments": orm.relationship(
                argument=comment_mapper,
                backref="post",
                collection_class=list,
                lazy="subquery",
            ),
            "likes": orm.relationship(
                argument=like_mapper,
                backref="post",
                collection_class=list,
                lazy="subquery",
            ),
        },
    )

    # metadata.create_all(component_factory.create_engine())
