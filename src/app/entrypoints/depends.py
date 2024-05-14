import fastapi

from src.app.entrypoints import schema


async def authorise_user(user_id: str = fastapi.Header(...)) -> str:
    """
    Authorise a user.
    """
    return user_id


def get_query_params(params: schema.GetPostParamRequest = fastapi.Depends()):
    return params
