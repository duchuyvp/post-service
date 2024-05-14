# """
# Module-level docstring describing the purpose of the module.
# """

# import logging

# import redis

# from src.app import config
# from src.app.domain import events

# logger = logging.getLogger(__name__)

# r = redis.Redis(host=config.settings.REDIS_HOST, port=config.settings.REDIS_PORT, db=2)


# def publish(channel, event: events.Event):
#     """
#     Method-level docstring describing the purpose of the method.

#     Args:
#         channel: The channel to publish the event to.
#         event: The event to be published.
#     """
#     logging.info("publishing: channel=%s, event=%s", channel, event)
#     r.publish(channel, event.model_dump_json())
