import uuid
import pytest
from src.app import views
from src.app.domain import commands
from src.app.service_layer import unit_of_work
from sqlalchemy.orm import clear_mappers
from tests import fake
from tests.confest import sql_session_factory
from src.app import bootstrap


@pytest.fixture
def bus(sql_session_factory):
    bus = bootstrap.bootstrap(
        start_orm=True,
        uow=unit_of_work.SqlAlchemyUnitOfWork(sql_session_factory),
    )
    yield bus
    clear_mappers()


def test_get_post(bus):
    unique_title = str(uuid.uuid4())
    bus.handle(
        commands.CreatePostCommand(
            title=unique_title,
            content="test content",
            author_id="test_author_id",
        )
    )

    posts = views.find_post(unique_title, bus.uow)

    assert len(posts) == 1
    assert posts[0]["title"] == unique_title
    assert posts[0]["content"] == "test content"
    assert posts[0]["author_id"] == "test_author_id"


@pytest.fixture
def post(bus):
    unique_title = str(uuid.uuid4())
    bus.handle(
        commands.CreatePostCommand(
            title=unique_title,
            content="test content",
            author_id="test_author_id",
        )
    )

    post = views.find_post(unique_title, bus.uow)[0]

    return post


@pytest.fixture
def comment(bus, post):
    bus.handle(
        commands.CommentPostCommand(
            post_id=post["id"],
            content="test comment",
            user_id="test_author_id",
        )
    )

    comments = views.get_comments(post["id"], bus.uow)

    return comments[0]


def test_delete_post(bus, post):
    bus.handle(
        commands.DeletePostCommand(
            user_id=post["author_id"],
            post_id=post["id"],
        )
    )

    posts = views.find_post(post["id"], bus.uow)

    assert len(posts) == 0


def test_like_post(bus, post):
    bus.handle(
        commands.LikeUnlikePostCommand(
            post_id=post["id"],
            user_id="test_user_id_like",
        )
    )

    post = views.get_post(post["id"], bus.uow)

    assert len(post["likes"]) == 1  # because it not implemented yet


def test_comment_post(bus, post):
    bus.handle(
        commands.CommentPostCommand(
            post_id=post["id"],
            user_id="test_comment_user_id",
            content="test comment",
        )
    )

    comments = views.get_comments(post["id"], bus.uow)

    assert len(comments) == 1
    assert comments[0]["content"] == "test comment"
    assert comments[0]["author_id"] == "test_comment_user_id"
    assert comments[0]["post_id"] == post["id"]


def test_delete_comment(bus, comment):
    bus.handle(
        commands.DeleteCommentCommand(
            user_id=comment["author_id"],
            comment_id=comment["id"],
        )
    )

    comments = views.get_comments(comment["post_id"], bus.uow)

    assert len(comments) == 0


def test_edit_post(bus, post):
    new_title_unique = str(uuid.uuid4())
    bus.handle(
        commands.EditPostCommand(
            user_id=post["author_id"],
            post_id=post["id"],
            title=new_title_unique,
            content="new content",
        )
    )

    posts = views.find_post(new_title_unique, bus.uow)

    assert len(posts) == 1
    assert posts[0]["title"] == new_title_unique
    assert posts[0]["content"] == "new content"
    assert posts[0]["author_id"] == "test_author_id"
    assert posts[0]["id"] == post["id"]
    assert posts[0]["version"] == 2
