from auth_fastapi_beanie_poetry.core.security import verify_password
from auth_fastapi_beanie_poetry.crud.user import get_user
from auth_fastapi_beanie_poetry.models.user import User


async def authenticate_user(username: str, password: str) -> User | False:
    user: User = await get_user(username)
    # if user is None:
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# get_current_user get_current_active_user
