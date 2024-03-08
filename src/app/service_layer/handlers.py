"""
This module contains the handlers for post-related commands.
"""

from __future__ import annotations
import typing as t

from src.app.domain import commands
from src.app.domain import events
from src.app.domain import model
from src.app.service_layer import unit_of_work


def create_post(cmd: commands.CreatePostCommand, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the create post command.
    """

    with uow:
        new_post = model.Post(
            title=cmd.title,
            content=cmd.content,
            author_id=cmd.author_id,
        )
        uow.posts.add(new_post)
        uow.commit()


def edit_post(cmd: commands.EditPostCommand, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the edit post command.
    """

    with uow:
        post = uow.posts.get(cmd.post_id)
        if post.can_edit_or_delete(user_id=cmd.user_id):
            post.edit(new_title=cmd.title, new_content=cmd.content)
            uow.commit()
        else:
            post.events.append(events.PostActionDenied(post_id=cmd.post_id, user_id=cmd.user_id))


def like_unlike_post(cmd: commands.LikeUnlikePostCommand, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the like post command.
    """

    with uow:
        post = uow.posts.get(cmd.post_id)
        post.like_unlike(user_id=cmd.user_id)
        uow.commit()


def comment_post(cmd: commands.CommentPostCommand, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the comment post command.
    """

    with uow:
        post = uow.posts.get(cmd.post_id)
        post.comment(content=cmd.content, author_id=cmd.user_id)
        uow.commit()


def delete_post(cmd: commands.DeletePostCommand, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the delete post command.
    """

    with uow:
        post = uow.posts.get(cmd.post_id)
        if post.can_edit_or_delete(user_id=cmd.user_id):
            post.delete()
            uow.commit()
        else:
            post.events.append(events.PostActionDenied(post_id=cmd.post_id, user_id=cmd.user_id))


def delete_comment(cmd: commands.DeleteCommentCommand, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the delete comment command.
    """

    with uow:
        comment = uow.comments.get(cmd.comment_id)
        if comment.can_edit_or_delete(user_id=cmd.user_id):
            comment.delete()
            uow.commit()
        else:
            comment.events.append(events.CommentActionDenied(comment_id=cmd.comment_id, user_id=cmd.user_id))


def do_nothing(events: events.Event, uow: unit_of_work.AbstractUnitOfWork):
    """
    Do nothing.
    """


def handle_permission_denied(events: events.Event, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the permission denied event.
    """

    uow.rollback()
    raise PermissionError(f"Permission denied for {events.__class__.__name__} event.")


EVENT_HANDLERS = {
    events.PostCreated: [do_nothing],
    events.PostEdited: [do_nothing],
    events.PostDeleted: [do_nothing],
    events.PostLiked: [do_nothing],
    events.PostUnliked: [do_nothing],
    events.CommentCreated: [do_nothing],
    events.CommentDeleted: [do_nothing],
    events.PostActionDenied: [handle_permission_denied],
    events.CommentActionDenied: [handle_permission_denied],
}

COMMAND_HANDLERS = {
    commands.CreatePostCommand: create_post,
    commands.EditPostCommand: edit_post,
    commands.LikeUnlikePostCommand: like_unlike_post,
    commands.CommentPostCommand: comment_post,
    commands.DeletePostCommand: delete_post,
    commands.DeleteCommentCommand: delete_comment,
}
