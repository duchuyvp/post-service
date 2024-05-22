import os
import uuid

import pytest
from fastapi import UploadFile
from icecream import ic
from sqlalchemy.orm import clear_mappers

from src.app import bootstrap
from src.app import views
from src.app.domain import commands
from src.app.entrypoints import schema
from src.app.service_layer import unit_of_work
from tests.confest import bus  # noqa: F811, F401
from tests.confest import sql_session_factory  # noqa: F811, F401


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
    assert comments[0]["level"] == 0


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


def test_comment_exceed_3_layers(bus, comment):
    cmd_0 = commands.ReplyCommentCommand(
        comment_id=comment["id"],
        user_id="test_user_reply_id",
        content="test reply comment " + str(uuid.uuid4()),
    )

    bus.handle(cmd_0)
    comments_0 = views.get_reply_comments(comment["id"], bus.uow)
    assert len(comments_0) == 1
    assert comments_0[0]["author_id"] == cmd_0.user_id
    assert comments_0[0]["content"] == cmd_0.content
    assert comments_0[0]["post_id"] == comment["post_id"]
    assert comments_0[0]["comment_id"] == comment["id"]
    assert comments_0[0]["level"] == 1
    assert comments_0[0]["like_count"] == 0

    cmd_1 = commands.ReplyCommentCommand(
        comment_id=comments_0[0]["id"],
        user_id="test_user_reply_id",
        content="test reply comment " + str(uuid.uuid4()),
    )

    bus.handle(cmd_1)
    comments_1 = views.get_reply_comments(comments_0[0]["id"], bus.uow)
    assert len(comments_1) == 1
    assert comments_1[0]["author_id"] == cmd_1.user_id
    assert comments_1[0]["content"] == cmd_1.content
    assert comments_1[0]["post_id"] == comment["post_id"]
    assert comments_1[0]["comment_id"] == comments_0[0]["id"]
    assert comments_1[0]["level"] == 2
    assert comments_1[0]["like_count"] == 0

    cmd_2 = commands.ReplyCommentCommand(
        comment_id=comments_1[0]["id"],
        user_id="test_user_reply_id",
        content="test reply comment " + str(uuid.uuid4()),
    )

    bus.handle(cmd_2)
    comments_2 = views.get_reply_comments(comments_1[0]["id"], bus.uow)
    assert len(comments_2) == 1
    assert comments_2[0]["author_id"] == cmd_2.user_id
    assert comments_2[0]["content"] == cmd_2.content
    assert comments_2[0]["post_id"] == comment["post_id"]
    assert comments_2[0]["comment_id"] == comments_1[0]["id"]
    assert comments_2[0]["level"] == 3
    assert comments_2[0]["like_count"] == 0

    cmd_3 = commands.ReplyCommentCommand(
        comment_id=comments_2[0]["id"],
        user_id="test_user_reply_id",
        content="test reply comment " + str(uuid.uuid4()),
    )

    with pytest.raises(ValueError):
        bus.handle(cmd_3)


def test_get_posts(bus):
    uniq = str(uuid.uuid4())
    params = schema.GetPostsRequest(
        title=uniq + " test_search_title",
        content="test_content",
        author_id="test_search_author_id",
        order=["-created_at"],
        limit=10,
        offset=0,
    )

    posts = views.get_posts(params, bus.uow)

    assert isinstance(posts, list)
    assert len(posts) == 0  # Assuming no posts exist with the given parameters

    # Create some test posts
    cmd1 = commands.CreatePostCommand(
        title=uniq + " test_search_title_1",
        content="test_content_1",
        author_id="test_search_author_id",
    )
    bus.handle(cmd1)

    cmd2 = commands.CreatePostCommand(
        title=uniq + " test_search_title_2",
        content="test_content_2",
        author_id="test_search_author_id",
    )
    bus.handle(cmd2)

    # Test with updated parameters
    params.title = uniq + " test_search_title"
    params.content = "test_content"
    params.author_id = "test_search_author_id"
    params.order = ["-created_time"]
    params.limit = 10
    params.offset = 0

    posts = views.get_posts(params, bus.uow)

    assert isinstance(posts, list)
    assert len(posts) == 2
    assert posts[0]["title"] == uniq + " test_search_title_2"
    assert posts[0]["content"] == "test_content_2"
    assert posts[0]["author_id"] == "test_search_author_id"
    assert posts[1]["title"] == uniq + " test_search_title_1"
    assert posts[1]["content"] == "test_content_1"
    assert posts[1]["author_id"] == "test_search_author_id"


def test_create_post_with_image(bus):
    unique_title = str(uuid.uuid4())
    file_path = "tests/assets/test_image.png"

    image = UploadFile(
        open(file_path, "rb"),
        filename="test_image.png",
        size=os.path.getsize(file_path),
        headers={
            "content-disposition": 'form-data; name="images"; filename="images.png"',
            "content-type": "image/png",
        },
    )

    cmd = commands.CreatePostCommand(
        title=unique_title,
        content="test content " + unique_title,
        author_id="test_author_id",
        image=[image],
    )

    bus.handle(cmd)
    posts = views.find_post(unique_title, bus.uow)

    assert len(posts) == 1

    post = posts[0]
    post = views.get_post(post["id"], bus.uow)

    # assert len(post["images"]) == 1
    # assert post["images"][0]["path"] == f"posts/{post['id']}/test_image.png"
