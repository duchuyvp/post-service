import fastapi
from src.app import views
from src.app import bootstrap
from src.app.domain import commands
from src.app.entrypoints import depends

from src.app.entrypoints.schema import CommentRequest, CreatePostRequest, PostResponse

app = fastapi.FastAPI(dependencies=[fastapi.Depends(depends.authorise_user)])
bus = bootstrap.bootstrap()


@app.post("/posts")
def create_post(request: CreatePostRequest, user_id: str = fastapi.Header(...)):
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
def get_post(id: str) -> PostResponse:
    """
    Get a post by its id.
    """
    post = views.get_post(post_id=id, uow=bus.uow)
    return post


@app.put("/posts/{id}")
def edit_post(id: str, request: CreatePostRequest, user_id: str = fastapi.Header(...)):
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


@app.delete("/posts/{id}")
def delete_post(id: str, user_id: str = fastapi.Header(...)):
    """
    Delete a post.
    """
    cmd = commands.DeletePostCommand(
        user_id=user_id,
        post_id=id,
    )
    bus.handle(cmd)

    return fastapi.Response(status_code=204)


@app.post("/posts/{id}/like")
def like_post(id: str, user_id: str = fastapi.Header(...)):
    """
    Like a post.
    """
    cmd = commands.LikeUnlikePostCommand(
        user_id=user_id,
        post_id=id,
    )
    bus.handle(cmd)

    return fastapi.Response(status_code=204)


@app.post("/posts/{id}/comments")
def comment_post(id: str, request: CommentRequest, user_id: str = fastapi.Header(...)):
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


@app.delete("/comments/{id}")
def delete_comment(id: str, user_id: str = fastapi.Header(...)):
    """
    Delete a comment.
    """
    cmd = commands.DeleteCommentCommand(
        user_id=user_id,
        comment_id=id,
    )
    bus.handle(cmd)

    return fastapi.Response(status_code=204)


@app.get("/posts/{post_id}/comments")
def get_comments(post_id: str):
    """
    Get comments of a post.
    """
    comments = views.get_comments(post_id=post_id, uow=bus.uow)
    return comments
