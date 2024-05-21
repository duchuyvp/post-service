import os
from typing import List
from typing import Optional

from minio import Minio
from sqlalchemy.orm import relationship
from sqlalchemy.orm import RelationshipProperty

from src.app.config import settings

minio_host = f"{settings.MINIO_HOST}:{settings.MINIO_PORT}"
minio = Minio(
    endpoint=minio_host,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False,
)


if not minio.bucket_exists("appt"):
    minio.make_bucket("appt")
