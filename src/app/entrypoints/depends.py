import fastapi


async def authorise_user(user_id: str = fastapi.Header(...)) -> str:
    """
    Authorise a user.
    """
    return user_id
