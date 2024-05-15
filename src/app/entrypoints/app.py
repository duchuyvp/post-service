import typing as t

import fastapi

from src.app import bootstrap
from src.app import views
from src.app.domain import commands
from src.app.entrypoints import depends
from src.app.entrypoints import schema

app = fastapi.FastAPI(dependencies=[fastapi.Depends(depends.authorise_user)])
bus = bootstrap.bootstrap()


@app.post("/posts", status_code=fastapi.status.HTTP_201_CREATED)
def create_post(request: schema.CreatePostRequest, user_id: str = fastapi.Header(...)):
    """
    Create a post.
    """
    cmd = commands.CreatePostCommand(
        title=request.title,
        content=request.content,
        author_id=user_id,
    )
    bus.handle(cmd)

    return fastapi.Response(status_code=201)


@app.get("/posts/{id}")
def get_post(id: str) -> schema.PostResponse:
    """
    Get a post by its id.
    """
    post = views.get_post(post_id=id, uow=bus.uow)
    return post


@app.put("/posts/{id}", status_code=fastapi.status.HTTP_204_NO_CONTENT)
def edit_post(id: str, request: schema.EditPostRequest, user_id: str = fastapi.Header(...)):
    """
    Edit a post.
    """
    cmd = commands.EditPostCommand(
        user_id=user_id,
        post_id=id,
        title=request.title,
        content=request.content,
    )
    bus.handle(cmd)

    return fastapi.Response(status_code=204)


@app.delete("/posts/{id}", status_code=fastapi.status.HTTP_204_NO_CONTENT)
def delete_post(id: str, user_id: t.Annotated[str, fastapi.Header(...)]):
    """
    Delete a post.
    """
    cmd = commands.DeletePostCommand(
        user_id=user_id,
        post_id=id,
    )
    bus.handle(cmd)

    return fastapi.Response(status_code=204)


@app.post("/posts/{id}/like", status_code=fastapi.status.HTTP_204_NO_CONTENT)
def like_post(id: str, user_id: t.Annotated[str, fastapi.Header(...)]):
    """
    Like a post.
    """
    cmd = commands.LikePostCommand(
        user_id=user_id,
        post_id=id,
    )
    bus.handle(cmd)

    return fastapi.Response(status_code=204)


@app.post("/posts/{id}/comments", status_code=fastapi.status.HTTP_201_CREATED)
def comment_post(id: str, request: schema.CommentRequest, user_id: t.Annotated[str, fastapi.Header(...)]):
    """
    Comment a post.
    """
    cmd = commands.CommentPostCommand(
        user_id=user_id,
        post_id=id,
        content=request.content,
    )
    bus.handle(cmd)

    return fastapi.Response(status_code=201)


@app.post("/comments/{id}/reply", status_code=fastapi.status.HTTP_201_CREATED)
def reply_comment(id: str, request: schema.CommentRequest, user_id: t.Annotated[str, fastapi.Header(...)]):
    """
    Reply to a comment.
    """
    cmd = commands.ReplyCommentCommand(
        user_id=user_id,
        comment_id=id,
        content=request.content,
    )
    bus.handle(cmd)

    return fastapi.Response(status_code=201)


@app.delete("/comments/{id}", status_code=fastapi.status.HTTP_204_NO_CONTENT)
def delete_comment(id: str, user_id: t.Annotated[str, fastapi.Header(...)]):
    """
    Delete a comment.
    """
    cmd = commands.DeleteCommentCommand(
        user_id=user_id,
        comment_id=id,
    )
    bus.handle(cmd)

    return fastapi.Response(status_code=204)


@app.post("/comments/{id}/like", status_code=fastapi.status.HTTP_204_NO_CONTENT)
def like_comment(id: str, user_id: t.Annotated[str, fastapi.Header(...)]):
    """
    Like a comment.
    """
    cmd = commands.LikeCommentCommand(
        user_id=user_id,
        comment_id=id,
    )
    bus.handle(cmd)

    return fastapi.Response(status_code=204)


@app.get("/posts/{post_id}/comments")
def get_comments(post_id: str) -> list[schema.CommentResponse]:
    """
    Get comments of a post.
    """
    comments = views.get_comments(post_id=post_id, uow=bus.uow)
    return comments


@app.get("/comments/{id}/reply")
def get_replies(id: str) -> list[schema.CommentResponse]:
    """
    Get replies of a comment.
    """
    replies = views.get_reply_comments(comment_id=id, uow=bus.uow)
    return replies


@app.get("/posts")
def get_posts(params: t.Annotated[schema.GetPostParamRequest, fastapi.Depends(depends.get_query_params)]) -> list[schema.PostResponse]:
    """
    Get all posts.
    """
    posts = views.get_posts(params, uow=bus.uow)
    return posts
