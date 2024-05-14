import json

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import clear_mappers

from src.app import bootstrap
from src.app import views
from src.app.entrypoints.app import app
from src.app.service_layer import unit_of_work
from tests.confest import bus  # noqa: F811, F401
from tests.confest import setup_database  # noqa: F811, F401
from tests.confest import sql_session_factory  # noqa: F811, F401

client = TestClient(app)


# @pytest.fixture
# def user_id():
#     return "test_e2e_user_id"


# def test_create_post(user_id, bus):
#     response = client.post(
#         "/posts",
#         headers={"user_id": user_id},
#         json={"title": "test e2e title", "content": "test e2e content"},
#     )

#     assert response.status_code == 201

#     posts = views.find_post("test e2e title", bus.uow)

#     assert len(posts) == 1
#     assert posts[0]["title"] == "test e2e title"
#     assert posts[0]["content"] == "test e2e content"
#     assert posts[0]["author_id"] == user_id
#     assert posts[0]["version"] == 1
