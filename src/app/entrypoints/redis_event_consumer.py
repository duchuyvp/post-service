import json
import logging

import redis

from src.app import bootstrap, config
from src.app.domain import commands

logger = logging.getLogger(__name__)

r = redis.Redis(host=config.settings.REDIS_HOST, port=config.settings.REDIS_PORT, db=0)


def main():
    logger.info("Redis pubsub starting")
    bus = bootstrap.bootstrap()
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe("some_topic")

    for m in pubsub.listen():
        handle_some_event(m, bus)


def handle_some_event(m, bus):
    logger.info("handling %s", m)
    data = json.loads(m["data"])
    cmd = commands.SomeCommand()
    bus.handle(cmd)


if __name__ == "__main__":
    main()
