import pydantic


class Event(pydantic.BaseModel):
    """
    Base class for events.
    """


class PostCreated(Event):
    """
    Event representing the creation of a post.
    """

    title: str
    content: str
    author_id: int
