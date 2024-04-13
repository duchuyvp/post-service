import pytest
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from src.app.adapters import orm

pytest.register_assert_rewrite("tests.e2e.api_client")


@pytest.fixture
def sql_session_factory():
    # engine = sa.create_engine("postgresql://postgres:postgres@localhost:5432/db")
    engine = sa.create_engine("sqlite:///:memory:")
    orm.mapper_registry.metadata.create_all(engine)
    yield sessionmaker(bind=engine)
