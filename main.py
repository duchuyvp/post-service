import sqlalchemy as sa

from src.app.adapters.orm import metadata
from src.app.service_layer.unit_of_work import POSTGRES_URI

metadata.create_all(bind=sa.create_engine(POSTGRES_URI))
