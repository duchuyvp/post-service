import shutil
import subprocess
import time
from pathlib import Path

import pytest
import redis
import requests
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers
from sqlalchemy.orm import sessionmaker

from src.app import config
from src.app.adapters import orm

pytest.register_assert_rewrite("tests.e2e.api_client")


@pytest.fixture
def sql_session_factory():
    # engine = sa.create_engine("postgresql://postgres:postgres@localhost:5432/db")
    engine = sa.create_engine("sqlite:///:memory:")
    orm.mapper_registry.metadata.create_all(engine)
    yield sessionmaker(bind=engine)
