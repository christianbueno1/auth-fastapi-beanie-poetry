from auth_fastapi_beanie_poetry.crud.user import get_user
from auth_fastapi_beanie_poetry.models.user import User


async def authenticate_user(username: str, password: str) -> User | None:
    user = await get_user(username)
    if user is None:
        return None
    if not user.verify_password(password):
        return None
    return user

