from typing import Annotated

import fastapi
import pydantic


@pydantic.dataclasses.dataclass
class CreatePostRequest:
    title: Annotated[str, fastapi.Form(...)]
    content: Annotated[str, fastapi.Form(...)]
    images: Annotated[list[fastapi.UploadFile], fastapi.Form(default_factory=list)]


@pydantic.dataclasses.dataclass
class GetPostRequest:
    id: Annotated[str, fastapi.Path(...)]


@pydantic.dataclasses.dataclass
class EditPostRequest:
    id: Annotated[str, fastapi.Path(...)]
    title: Annotated[str, fastapi.Form(...)]
    content: Annotated[str, fastapi.Form(...)]


@pydantic.dataclasses.dataclass
class DeletePostRequest:
    id: Annotated[str, fastapi.Path(...)]


@pydantic.dataclasses.dataclass
class LikePostRequest:
    id: Annotated[str, fastapi.Path(...)]


@pydantic.dataclasses.dataclass
class CommentRequest:
    id: Annotated[str, fastapi.Path(...)]
    content: Annotated[str, fastapi.Form(...)]


@pydantic.dataclasses.dataclass
class ReplyRequest:
    id: Annotated[str, fastapi.Path(...)]
    content: Annotated[str, fastapi.Form(...)]


@pydantic.dataclasses.dataclass
class DeleteCommentRequest:
    id: Annotated[str, fastapi.Path(...)]


@pydantic.dataclasses.dataclass
class LikeCommentRequest:
    id: Annotated[str, fastapi.Path(...)]


@pydantic.dataclasses.dataclass
class GetPostCommentRequest:
    id: Annotated[str, fastapi.Path(...)]


@pydantic.dataclasses.dataclass
class GetCommentReplyRequest:
    id: Annotated[str, fastapi.Path(...)]


@pydantic.dataclasses.dataclass
class GetPostsRequest:
    title: Annotated[str | None, fastapi.Query(None)]
    content: Annotated[str | None, fastapi.Query(None)]
    author_id: Annotated[str | None, fastapi.Query(None)]

    order: Annotated[list[str], fastapi.Query(["-created_time"])]
    limit: Annotated[int, fastapi.Query(10)]
    offset: Annotated[int, fastapi.Query(0)]


class CommentResponse(pydantic.BaseModel):
    content: str
    author_id: str
    created_time: str


class ImageResponse(pydantic.BaseModel):
    id: str
    path: str
    link: str


class PostResponse(pydantic.BaseModel):
    id: str
    title: str
    content: str
    created_time: str
    author_id: str
    like_count: int
    version: int
    images: list[ImageResponse]
