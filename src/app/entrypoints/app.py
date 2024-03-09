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

    return {"message": "post created"}


@app.get("/posts/{post_id}")
def get_post(post_id: str) -> PostResponse:
    """
    Get a post by its id.
    """
    post = views.get_post(post_id=post_id, uow=bus.uow)
    return post


@app.put("/posts/{post_id}")
def edit_post(post_id: str, request: CreatePostRequest, user_id: str = fastapi.Header(...)):
    """
    Edit a post.
    """
    cmd = commands.EditPostCommand(
        user_id=user_id,
        post_id=post_id,
        title=request.title,
        content=request.content,
    )
    bus.handle(cmd)

    return {"message": "post edited"}


@app.delete("/posts/{post_id}")
def delete_post(post_id: str, user_id: str = fastapi.Header(...)):
    """
    Delete a post.
    """
    cmd = commands.DeletePostCommand(
        user_id=user_id,
        post_id=post_id,
    )
    bus.handle(cmd)

    return {"message": "post deleted"}


@app.post("/posts/{post_id}/like")
def like_post(post_id: str, user_id: str = fastapi.Header(...)):
    """
    Like a post.
    """
    cmd = commands.LikeUnlikePostCommand(
        user_id=user_id,
        post_id=post_id,
    )
    bus.handle(cmd)

    return {"message": "post liked"}


@app.post("/posts/{post_id}/comment")
def comment_post(post_id: str, request: CommentRequest, user_id: str = fastapi.Header(...)):
    """
    Comment a post.
    """
    cmd = commands.CommentPostCommand(
        user_id=user_id,
        post_id=post_id,
        content=request.content,
    )
    bus.handle(cmd)

    return {"message": "comment created"}


@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: str, user_id: str = fastapi.Header(...)):
    """
    Delete a comment.
    """
    cmd = commands.DeleteCommentCommand(
        user_id=user_id,
        comment_id=comment_id,
    )
    bus.handle(cmd)

    return {"message": "comment deleted"}
