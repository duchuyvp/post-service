import logging

import sqlalchemy as sa

metadata = sa.MetaData()

logger = logging.getLogger(__name__)


def start_mappers():
    logger.info("Starting mappers")
    print("Starting mappers")
