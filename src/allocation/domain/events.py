import pydantic


class Event(pydantic.BaseModel):
    """"""


class PostCreated(Event):
    """"""

    title: str
    content: str
    author_id: int
