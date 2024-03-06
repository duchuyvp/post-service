import typing as t

from allocation.domain import commands
from allocation.domain import events
from allocation.service_layer import unit_of_work


def create_post(cmd: commands.CommentPostCommand, uow: unit_of_work.AbstractUnitOfWork):
    """"""


def edit_post(cmd: commands.EditPostCommand, uow: unit_of_work.AbstractUnitOfWork):
    """"""


def like_post(cmd: commands.LikePostCommand, uow: unit_of_work.AbstractUnitOfWork):
    """"""


def comment_post(cmd: commands.CommentPostCommand, uow: unit_of_work.AbstractUnitOfWork):
    """"""


def delete_post(cmd: commands.DeletePostCommand, uow: unit_of_work.AbstractUnitOfWork):
    """"""


def publish_post_created(event: events.PostCreated, publish: t.Callable[[events.Event], None]):
    publish(event)


EVENT_HANDLERS = {
    events.PostCreated: [publish_post_created],
}

COMMAND_HANDLERS = {
    commands.CommentPostCommand: comment_post,
    commands.CreatePostCommand: create_post,
    commands.EditPostCommand: edit_post,
    commands.LikePostCommand: like_post,
}
