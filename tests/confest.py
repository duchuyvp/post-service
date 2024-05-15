import pytest
import sqlalchemy as sa
from sqlalchemy.orm import clear_mappers
from sqlalchemy.orm import sessionmaker

from src.app import bootstrap
from src.app import views
from src.app.adapters import orm
from src.app.adapters.orm import start_mappers
from src.app.domain import commands
from src.app.service_layer import unit_of_work

pytest.register_assert_rewrite("tests.e2e.api_client")


@pytest.fixture(scope="session")
def sql_session_factory():
    engine = sa.create_engine("postgresql://postgres:postgres@localhost:5432/test_db")
    # engine = sa.create_engine("sqlite:///:memory:")
    orm.mapper_registry.metadata.create_all(engine)
    yield sessionmaker(bind=engine)
    orm.mapper_registry.metadata.drop_all(engine)


@pytest.fixture(scope="session")
def bus(sql_session_factory):
    bus = bootstrap.bootstrap(
        start_orm=True,
        uow=unit_of_work.SqlAlchemyUnitOfWork(sql_session_factory),
    )
    yield bus
    clear_mappers()
