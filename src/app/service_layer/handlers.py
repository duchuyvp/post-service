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
        new_post.events.append(events.PostCreatedEvent(post_id=new_post.id))


def edit_post(cmd: commands.EditPostCommand, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the edit post command.
    """

    with uow:
        post = uow.posts.get(cmd.post_id)
        if post.can_edit_or_delete(user_id=cmd.user_id):
            post.edit(new_title=cmd.title, new_content=cmd.content)
            uow.commit()
            post.events.append(events.PostEditedEvent(post_id=cmd.post_id, version=post.version))
        else:
            post.events.append(events.PostActionDeniedEvent(post_id=cmd.post_id, user_id=cmd.user_id))


def like_unlike_post(cmd: commands.LikeUnlikePostCommand, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the like post command.
    """

    with uow:
        post = uow.posts.get(cmd.post_id)
        post.like_unlike(user_id=cmd.user_id)  # TODO: notworking, don't know why
        uow.commit()
        if cmd.user_id in post.likes:
            post.events.append(events.PostLikedEvent(post_id=cmd.post_id, user_id=cmd.user_id))
        else:
            post.events.append(events.PostUnlikedEvent(post_id=cmd.post_id, user_id=cmd.user_id))


def comment_post(cmd: commands.CommentPostCommand, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the comment post command.
    """

    with uow:
        post = uow.posts.get(cmd.post_id)
        comment = post.comment(content=cmd.content, author_id=cmd.user_id)
        uow.comments.add(comment)
        uow.commit()
        post.events.append(events.CommentCreatedEvent(comment_id=comment.id, post_id=cmd.post_id))


def delete_post(cmd: commands.DeletePostCommand, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the delete post command.
    """

    with uow:
        post = uow.posts.get(cmd.post_id)
        if post.can_edit_or_delete(user_id=cmd.user_id):
            uow.posts.delete(post)
            uow.commit()
            post.events.append(events.PostDeletedEvent(post_id=cmd.post_id))
        else:
            post.events.append(events.PostActionDeniedEvent(post_id=cmd.post_id, user_id=cmd.user_id))


def delete_comment(cmd: commands.DeleteCommentCommand, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the delete comment command.
    """

    with uow:
        comment = uow.comments.get(cmd.comment_id)
        if comment.can_edit_or_delete(user_id=cmd.user_id):
            uow.comments.delete(comment)
            uow.commit()
            comment.events.append(events.CommentDeletedEvent(comment_id=cmd.comment_id))
        else:
            comment.events.append(events.CommentActionDeniedEvent(comment_id=cmd.comment_id, user_id=cmd.user_id))


def do_nothing(events: events.Event, uow: unit_of_work.AbstractUnitOfWork):
    """
    Do nothing.
    """


def handle_post_created(events: events.PostCreatedEvent, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the post created event.
    """

    with uow:
        post = uow.posts.get(events.post_id)
        return post.model_dump()


def handle_comment_created(events: events.CommentCreatedEvent, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the comment created event.
    """

    with uow:
        comment = uow.comments.get(events.comment_id)
        return comment.model_dump()


def handle_permission_denied(events: events.Event, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the permission denied event.
    """

    uow.rollback()
    raise PermissionError(f"Permission denied for {events.__class__.__name__} event.")


EVENT_HANDLERS = {
    events.PostCreatedEvent: [handle_post_created],
    events.PostEditedEvent: [do_nothing],
    events.PostDeletedEvent: [do_nothing],
    events.PostLikedEvent: [do_nothing],
    events.PostUnlikedEvent: [do_nothing],
    events.CommentCreatedEvent: [do_nothing],
    events.CommentDeletedEvent: [do_nothing],
    events.PostActionDeniedEvent: [handle_permission_denied],
    events.CommentActionDeniedEvent: [handle_permission_denied],
}

COMMAND_HANDLERS = {
    commands.CreatePostCommand: create_post,
    commands.EditPostCommand: edit_post,
    commands.LikeUnlikePostCommand: like_unlike_post,
    commands.CommentPostCommand: comment_post,
    commands.DeletePostCommand: delete_post,
    commands.DeleteCommentCommand: delete_comment,
}
