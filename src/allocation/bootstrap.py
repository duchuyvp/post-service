import inspect
import typing as t

from allocation.adapters import orm
from allocation.adapters import redis_eventpublisher
from allocation.service_layer import handlers
from allocation.service_layer import messagebus
from allocation.service_layer import unit_of_work

"""
This module contains the bootstrap function for the allocation application.
"""


def bootstrap(
    start_orm: bool = True,
    uow: unit_of_work.AbstractUnitOfWork = unit_of_work.SqlAlchemyUnitOfWork(),
    publish: t.Callable = redis_eventpublisher.publish,
) -> messagebus.MessageBus:
    """
    Bootstrap the allocation application.

    Args:
        start_orm: A boolean indicating whether to start the ORM.
        uow: An instance of the unit of work.
        publish: A callable for publishing events.

    Returns:
        An instance of the MessageBus.
    """
    if start_orm:
        orm.start_mappers()

    dependencies = {"uow": uow, "publish": publish}
    injected_event_handlers = {
        event_type: [inject_dependencies(handler, dependencies) for handler in event_handlers]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }
    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies) for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    return messagebus.MessageBus(
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )


def inject_dependencies(handler: t.Callable, dependencies: dict):
    """
    Inject dependencies into a handler.

    Args:
        handler: The handler to inject dependencies into.
        dependencies: A dictionary of dependencies to inject.

    Returns:
        A new handler with the dependencies injected.
    """

    params = inspect.signature(handler).parameters
    deps = {name: dependency for name, dependency in dependencies.items() if name in params}
    return lambda message: handler(message, **deps)
