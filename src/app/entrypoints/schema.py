import pydantic


class CreatePostRequest(pydantic.BaseModel):
    title: str
    content: str


class PostResponse(pydantic.BaseModel):
    id: str
    title: str
    content: str
    created_at: str
    author_id: str
    likes: list[str]
    version: int


class CommentRequest(pydantic.BaseModel):
    content: str


class CommentResponse(pydantic.BaseModel):
    content: str
    author_id: str
    created_at: str
