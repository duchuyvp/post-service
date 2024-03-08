import fastapi
from src.app import bootstrap
from src.app.domain import commands
from src.app.entrypoints.depends import authorise_user

from src.app.entrypoints.schema import CreatePostRequest

app = fastapi.FastAPI()
bus = bootstrap.bootstrap()


@app.post("/posts", dependencies=[fastapi.Depends(authorise_user)])
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
