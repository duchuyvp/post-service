import shutil
import subprocess
import time
from pathlib import Path

import pytest
import redis
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

import sqlalchemy as sa

from src.app.adapters import orm
from src.app import config

pytest.register_assert_rewrite("tests.e2e.api_client")


@pytest.fixture
def in_memory_sqlite_db():
    engine = sa.create_engine("sqlite:///:memory:")
    orm.mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def sqlite_session_factory(in_memory_sqlite_db):
    yield sessionmaker(bind=in_memory_sqlite_db)


@pytest.fixture
def mappers():
    orm.start_mappers()
    yield
    clear_mappers()
