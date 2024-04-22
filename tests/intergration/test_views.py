import uuid

import pytest
from sqlalchemy.orm import clear_mappers

from src.app import bootstrap, views
from src.app.domain import commands
from src.app.service_layer import unit_of_work
from tests.confest import sql_session_factory  # noqa: F811, F401


@pytest.fixture
def bus(sql_session_factory):
    bus = bootstrap.bootstrap(
        start_orm=True,
        uow=unit_of_work.SqlAlchemyUnitOfWork(sql_session_factory),
    )
    yield bus
    clear_mappers()


def test_create_post(bus):
    unique_title = str(uuid.uuid4())
    cmd = commands.CreatePostCommand(title=unique_title, content="test content " + unique_title, author_id="test_author_id")

    bus.handle(cmd)
    posts = views.find_post(unique_title, bus.uow)

    assert len(posts) == 1
    assert posts[0]["title"] == cmd.title
    assert posts[0]["content"] == cmd.content
    assert posts[0]["author_id"] == cmd.author_id
    assert posts[0]["version"] == 1


@pytest.fixture(scope="function")
def post(bus):
    unique_title = str(uuid.uuid4())
    cmd = commands.CreatePostCommand(
        title=unique_title,
        content="test content " + unique_title,
        author_id="test_author_id",
    )

    bus.handle(cmd)
    post = views.find_post(unique_title, bus.uow)[0]

    return post


def test_edit_post(bus, post):
    new_title_unique = str(uuid.uuid4())
    cmd = commands.EditPostCommand(
        user_id=post["author_id"],
        post_id=post["id"],
        title=new_title_unique,
        content="new content " + new_title_unique,
    )

    bus.handle(cmd)
    posts = views.find_post(new_title_unique, bus.uow)

    assert len(posts) == 1
    assert posts[0]["title"] == new_title_unique
    assert posts[0]["content"] == cmd.content
    assert posts[0]["author_id"] == post["author_id"]
    assert posts[0]["id"] == post["id"]
    assert posts[0]["version"] == 2


def test_delete_post(bus, post):
    cmd = commands.DeletePostCommand(user_id=post["author_id"], post_id=post["id"])

    bus.handle(cmd)
    posts = views.find_post(post["id"], bus.uow)
    assert len(posts) == 0


def test_like_unlike_post(bus, post):
    cmd_like_1 = commands.LikePostCommand(post_id=post["id"], user_id="test_user_id_like")
    cmd_like_2 = commands.LikePostCommand(post_id=post["id"], user_id="test_user_id_like_2")
    cmd_unlike_2 = commands.LikePostCommand(post_id=post["id"], user_id="test_user_id_like_2")

    bus.handle(cmd_like_1)
    post = views.get_post(post["id"], bus.uow)
    assert post["like_count"] == 1

    bus.handle(cmd_like_2)
    post = views.get_post(post["id"], bus.uow)
    assert post["like_count"] == 2

    bus.handle(cmd_unlike_2)
    post = views.get_post(post["id"], bus.uow)
    assert post["like_count"] == 1


def test_comment_post(bus, post):
    cmd = commands.CommentPostCommand(
        post_id=post["id"],
        user_id="test_comment_user_id",
        content="test comment " + str(uuid.uuid4()),
    )

    bus.handle(cmd)
    comments = views.get_comments(post["id"], bus.uow)

    assert len(comments) == 1
    assert comments[0]["author_id"] == cmd.user_id
    assert comments[0]["content"] == cmd.content
    assert comments[0]["post_id"] == post["id"]


@pytest.fixture(scope="function")
def comment(bus, post):
    cmd = commands.CommentPostCommand(
        post_id=post["id"],
        user_id="test_user_comment_id",
        content="test comment " + str(uuid.uuid4()),
    )

    bus.handle(cmd)
    comments = views.get_comments(post["id"], bus.uow)

    return comments[0]


def test_delete_comment(bus, comment):
    cmd = commands.DeleteCommentCommand(
        user_id=comment["author_id"],
        comment_id=comment["id"],
    )

    bus.handle(cmd)
    comments = views.get_comments(comment["post_id"], bus.uow)

    assert len(comments) == 0


def test_like_unlike_comment(bus, comment):
    cmd_like_1 = commands.LikeCommentCommand(comment_id=comment["id"], user_id="test_user_id_like")
    cmd_like_2 = commands.LikeCommentCommand(comment_id=comment["id"], user_id="test_user_id_like_2")
    cmd_unlike_2 = commands.LikeCommentCommand(comment_id=comment["id"], user_id="test_user_id_like_2")

    bus.handle(cmd_like_1)
    comment = views.get_comment(comment["id"], bus.uow)
    assert comment["like_count"] == 1

    bus.handle(cmd_like_2)
    comment = views.get_comment(comment["id"], bus.uow)
    assert comment["like_count"] == 2

    bus.handle(cmd_unlike_2)
    comment = views.get_comment(comment["id"], bus.uow)
    assert comment["like_count"] == 1


def test_reply_comment(bus, comment):
    cmd = commands.ReplyCommentCommand(
        comment_id=comment["id"],
        user_id="test_user_reply_id",
        content="test reply comment " + str(uuid.uuid4()),
    )

    bus.handle(cmd)
    comments = views.get_comments(comment["post_id"], bus.uow)

    assert len(comments) == 2
    assert comments[1]["author_id"] == cmd.user_id
    assert comments[1]["content"] == cmd.content
    assert comments[1]["post_id"] == comment["post_id"]
    assert comments[1]["comment_id"] == comment["id"]
    assert comments[1]["level"] == 1
    assert comments[1]["like_count"] == 0
