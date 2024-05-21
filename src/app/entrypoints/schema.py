from typing import Annotated

import fastapi
import pydantic


class CreatePostRequest(pydantic.BaseModel):
    title: Annotated[str, fastapi.Form(...)]
    content: Annotated[str, fastapi.Form(...)]
    images: Annotated[list[fastapi.UploadFile], fastapi.Form()] = []


class GetPostRequest(pydantic.BaseModel):
    id: Annotated[str, fastapi.Path(...)]


class EditPostRequest(pydantic.BaseModel):
    id: Annotated[str, fastapi.Path(...)]
    title: Annotated[str, fastapi.Form(...)]
    content: Annotated[str, fastapi.Form(...)]


class DeletePostRequest(pydantic.BaseModel):
    id: Annotated[str, fastapi.Path(...)]


class LikePostRequest(pydantic.BaseModel):
    id: Annotated[str, fastapi.Path(...)]


class CommentRequest(pydantic.BaseModel):
    id: Annotated[str, fastapi.Path(...)]
    content: Annotated[str, fastapi.Form(...)]


class ReplyRequest(pydantic.BaseModel):
    id: Annotated[str, fastapi.Path(...)]
    content: Annotated[str, fastapi.Form(...)]


class DeleteCommentRequest(pydantic.BaseModel):
    id: Annotated[str, fastapi.Path(...)]


class LikeCommentRequest(pydantic.BaseModel):
    id: Annotated[str, fastapi.Path(...)]


class GetPostCommentRequest(pydantic.BaseModel):
    id: Annotated[str, fastapi.Path(...)]


class GetCommentReplyRequest(pydantic.BaseModel):
    id: Annotated[str, fastapi.Path(...)]


class GetPostsRequest(pydantic.BaseModel):
    title: Annotated[str | None, fastapi.Query(None)]
    content: Annotated[str | None, fastapi.Query(None)]
    author_id: Annotated[str | None, fastapi.Query(None)]

    order: Annotated[list[str], fastapi.Query()]
    limit: Annotated[int, fastapi.Query(10)]
    offset: Annotated[int, fastapi.Query(0)]


class PostResponse(pydantic.BaseModel):
    id: str
    title: str
    content: str
    created_time: str
    author_id: str
    like_count: int
    version: int


class CommentResponse(pydantic.BaseModel):
    content: str
    author_id: str
    created_time: str
