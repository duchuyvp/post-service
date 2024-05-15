import json
import uuid

import pytest
from fastapi.testclient import TestClient
from icecream import ic
from sqlalchemy.orm import clear_mappers

from src.app import bootstrap
from src.app import views
from src.app.domain import commands
from src.app.entrypoints.app import app
from src.app.service_layer import unit_of_work
from tests.confest import bus  # noqa: F811, F401
from tests.confest import sql_session_factory  # noqa: F811, F401

client = TestClient(app)


@pytest.fixture
def user_id():
    return "test_e2e_user_id"


def test_create_post(user_id, bus):
    response = client.post(
        "/posts",
        headers={"user-id": user_id},
        json={"title": "test 2e2 title", "content": "test e2e content"},
    )

    assert response.status_code == 201


@pytest.fixture(scope="function")
def post_id(bus):
    unique_title = str(uuid.uuid4())
    cmd = commands.CreatePostCommand(
        title=unique_title,
        content="test content " + unique_title,
        author_id="test_author_id",
    )

    bus.handle(cmd)
    post = views.find_post(unique_title, bus.uow)[0]

    return post["id"]


def test_get_post(bus, post_id):
    response = client.get(f"/posts/{post_id}", headers={"user-id": "test_user_id"})

    assert response.status_code == 200
    assert response.json()["id"] == post_id


def test_edit_post(bus, post_id, user_id):
    response = client.put(
        f"/posts/{post_id}",
        headers={"user-id": user_id},
        json={"title": "new e2e title", "content": "new content"},
    )

    assert response.status_code == 204


def test_delete_post(bus, post_id, user_id):
    response = client.delete(f"/posts/{post_id}", headers={"user-id": user_id})

    assert response.status_code == 204


def test_like_post(bus, post_id):
    response = client.post(f"/posts/{post_id}/like", headers={"user-id": "test_user_id"})

    assert response.status_code == 204


def test_comment_post(bus, post_id):
    response = client.post(
        f"/posts/{post_id}/comments",
        headers={"user-id": "test_user_id"},
        json={"content": "test comment"},
    )

    assert response.status_code == 201


@pytest.fixture(scope="function")
def comment_id(bus, post_id):
    cmd = commands.CommentPostCommand(
        post_id=post_id,
        user_id="test_user_comment_id",
        content="test comment " + str(uuid.uuid4()),
    )

    bus.handle(cmd)
    comments = views.get_comments(post_id, bus.uow)

    return comments[0]["id"]


def test_reply_comment(bus, comment_id):
    response = client.post(
        f"/comments/{comment_id}/reply",
        headers={"user-id": "test_user_id"},
        json={"content": "test reply comment"},
    )

    assert response.status_code == 201


def test_delete_comment(bus, comment_id):
    response = client.delete(f"/comments/{comment_id}", headers={"user-id": "test_user_id"})

    assert response.status_code == 204


def test_like_comment(bus, comment_id):
    response = client.post(f"/comments/{comment_id}/like", headers={"user-id": "test_user_id"})

    assert response.status_code == 204


def test_get_comments(bus, post_id):
    response = client.get(f"/posts/{post_id}/comments", headers={"user-id": "test_user_id"})

    assert response.status_code == 200


def test_get_reply_comments(bus, comment_id):
    response = client.get(f"/comments/{comment_id}/reply", headers={"user-id": "test_user_id"})

    assert response.status_code == 200


def test_get_posts(bus):
    response = client.get("/posts", headers={"user-id": "test_user_id"})

    assert response.status_code == 200
