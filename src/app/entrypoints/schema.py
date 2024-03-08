import pydantic
import fastapi


class CreatePostRequest(pydantic.BaseModel):
    title: str
    content: str
