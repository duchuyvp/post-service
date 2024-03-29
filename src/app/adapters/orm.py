import json
import logging

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import registry
from src.app.adapters import orm_helper

from src.app.domain import model

logger = logging.getLogger(__name__)


mapper_registry = registry()


comments = sa.Table(
    "comments",
    mapper_registry.metadata,
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
    mapper_registry.metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("title", sa.String),
    sa.Column("content", sa.String),
    sa.Column("likes", orm_helper.JSONArray, default=[]),
    sa.Column("created_at", sa.TIMESTAMP),
    sa.Column("updated_at", sa.TIMESTAMP),
    sa.Column("version", sa.Integer),
    sa.Column("author_id", sa.String),
)


def start_mappers():
    """
    This method starts the mappers.
    """
    # logger.info("Starting mappers")
    mapper_registry.map_imperatively(model.Post, posts)
    mapper_registry.map_imperatively(model.Comment, comments)
