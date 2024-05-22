"""
This module contains the handlers for post-related commands.
"""

from __future__ import annotations

import uuid

from src.app.domain import commands
from src.app.domain import events
from src.app.domain import model
from src.app.service_layer import unit_of_work


def create_post(cmd: commands.CreatePostCommand, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the create post command.
    """

    with uow.unit_of_work() as uow_ctx:
        new_post = model.Post(
            title=cmd.title,
            content=cmd.content,
            author_id=cmd.author_id,
        )
        uow_ctx.posts.add(new_post)
        uow_ctx.commit()
        new_post.events.append(events.PostCreatedEvent(post_id=new_post.id, images=cmd.images))


def edit_post(cmd: commands.EditPostCommand, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the edit post command.
    """

    with uow.unit_of_work() as uow_ctx:
        post = uow_ctx.posts.get(cmd.post_id)
        if post.can_edit_or_delete(user_id=cmd.user_id):
            post.edit(new_title=cmd.title, new_content=cmd.content)
            uow_ctx.commit()
            post.events.append(events.PostEditedEvent(post_id=cmd.post_id, version=post.version))
        else:
            post.events.append(events.PostActionDeniedEvent(post_id=cmd.post_id, user_id=cmd.user_id))


def like_unlike_post(cmd: commands.LikePostCommand, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the like post command.
    """

    with uow.unit_of_work() as uow_ctx:
        post = uow_ctx.posts.get(cmd.post_id)
        post.like_unlike(user_id=cmd.user_id)
        uow_ctx.commit()
        if cmd.user_id in post.likes:
            post.events.append(events.PostLikedEvent(post_id=cmd.post_id, user_id=cmd.user_id))
        else:
            post.events.append(events.PostUnlikedEvent(post_id=cmd.post_id, user_id=cmd.user_id))


def like_unlike_comment(cmd: commands.LikeCommentCommand, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the like comment command.
    """

    with uow.unit_of_work() as uow_ctx:
        comment = uow_ctx.comments.get(cmd.comment_id)
        comment.like_unlike(user_id=cmd.user_id)
        uow_ctx.commit()
        if cmd.user_id in comment.likes:
            comment.events.append(events.CommentLikedEvent(comment_id=cmd.comment_id, user_id=cmd.user_id))
        else:
            comment.events.append(events.CommentUnlikedEvent(comment_id=cmd.comment_id, user_id=cmd.user_id))


def comment_post(cmd: commands.CommentPostCommand, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the comment post command.
    """

    with uow.unit_of_work() as uow_ctx:
        post = uow_ctx.posts.get(cmd.post_id)
        comment = post.comment(content=cmd.content, author_id=cmd.user_id)
        uow_ctx.comments.add(comment)
        uow_ctx.commit()
        post.events.append(events.CommentCreatedEvent(comment_id=comment.id, post_id=cmd.post_id))


def delete_post(cmd: commands.DeletePostCommand, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the delete post command.
    """

    with uow.unit_of_work() as uow_ctx:
        post = uow_ctx.posts.get(cmd.post_id)
        if post.can_edit_or_delete(user_id=cmd.user_id):
            uow_ctx.posts.delete(post)
            uow_ctx.commit()
            post.events.append(events.PostDeletedEvent(post_id=cmd.post_id))
        else:
            post.events.append(events.PostActionDeniedEvent(post_id=cmd.post_id, user_id=cmd.user_id))


def delete_comment(cmd: commands.DeleteCommentCommand, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the delete comment command.
    """

    with uow.unit_of_work() as uow_ctx:
        comment = uow_ctx.comments.get(cmd.comment_id)
        if comment.can_edit_or_delete(user_id=cmd.user_id):
            uow_ctx.comments.delete(comment)
            uow_ctx.commit()
            comment.events.append(events.CommentDeletedEvent(comment_id=cmd.comment_id))
        else:
            comment.events.append(events.CommentActionDeniedEvent(comment_id=cmd.comment_id, user_id=cmd.user_id))


def reply_comment(cmd: commands.ReplyCommentCommand, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the reply comment command.
    """

    with uow.unit_of_work() as uow_ctx:
        comment = uow_ctx.comments.get(cmd.comment_id)
        reply = comment.reply(content=cmd.content, author_id=cmd.user_id)
        uow_ctx.comments.add(reply)
        uow_ctx.commit()
        comment.events.append(events.CommentRepliedEvent(comment_id=reply.id, post_id=comment.post_id))


def do_nothing(events: events.Event, uow: unit_of_work.AbstractUnitOfWork):
    """
    Do nothing.
    """


def handle_post_created(events: events.PostCreatedEvent, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the post created event. Upload images to the storage.
    """

    with uow.unit_of_work() as uow_ctx:
        images = uow_ctx.images
        post = uow_ctx.posts.get(events.post_id)
        for file in events.images:
            path = f"posts/{post.id}/{file.filename}"
            image = post.add_image(path)
            images.add(image)
            err_code = uow_ctx.minio.add(path, file)
            if err_code == 0:
                uow_ctx.commit()
            else:
                # Notification.send(f"Failed to upload image {file.filename}.")
                uow_ctx.rollback()


def handle_comment_created(events: events.CommentCreatedEvent, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the comment created event.
    """


def handle_permission_denied(events: events.Event, uow: unit_of_work.AbstractUnitOfWork):
    """
    Handle the permission denied event.
    """

    # raise PermissionError(f"Permission denied for {events.__class__.__name__} event.")
    # Notification.send(f"Permission denied for {events.__class__.__name__} event.")


EVENT_HANDLERS = {
    events.PostCreatedEvent: [handle_post_created],
    events.PostEditedEvent: [do_nothing],
    events.PostDeletedEvent: [do_nothing],
    events.PostLikedEvent: [do_nothing],
    events.PostUnlikedEvent: [do_nothing],
    events.CommentCreatedEvent: [do_nothing],
    events.CommentLikedEvent: [do_nothing],
    events.CommentUnlikedEvent: [do_nothing],
    events.CommentRepliedEvent: [do_nothing],
    events.CommentDeletedEvent: [do_nothing],
    events.PostActionDeniedEvent: [handle_permission_denied],
    events.CommentActionDeniedEvent: [handle_permission_denied],
}

COMMAND_HANDLERS = {
    commands.CreatePostCommand: create_post,
    commands.EditPostCommand: edit_post,
    commands.LikePostCommand: like_unlike_post,
    commands.LikeCommentCommand: like_unlike_comment,
    commands.CommentPostCommand: comment_post,
    commands.DeletePostCommand: delete_post,
    commands.DeleteCommentCommand: delete_comment,
    commands.ReplyCommentCommand: reply_comment,
}
