import fastapi
import pydantic


class CreatePostRequest(pydantic.BaseModel):
    title: str
    content: str


class EditPostRequest(pydantic.BaseModel):
    title: str
    content: str


class PostResponse(pydantic.BaseModel):
    id: str
    title: str
    content: str
    created_time: str
    author_id: str
    like_count: int
    version: int


class CommentRequest(pydantic.BaseModel):
    content: str


class CommentResponse(pydantic.BaseModel):
    content: str
    author_id: str
    created_time: str


class GetPostParamRequest(pydantic.BaseModel):
    title: str | None = None
    content: str | None = None
    author_id: str | None = None

    order: list[str] = fastapi.Query(["-created_time"])
    limit: int = 100
    offset: int = 0
