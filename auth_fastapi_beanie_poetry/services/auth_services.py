from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from auth_fastapi_beanie_poetry.core.security import verify_password
from auth_fastapi_beanie_poetry.crud.user import get_user
from auth_fastapi_beanie_poetry.models.token import TokenData
from auth_fastapi_beanie_poetry.models.user import User
from auth_fastapi_beanie_poetry.core.config import core_settings
from jwt.exceptions import InvalidTokenError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def authenticate_user(username: str, password: str) -> User | False:
    user: User = await get_user(username)
    # if user is None:
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# get_current_user get_current_active_user

# get_current_user
# username is the sub claim of the JWT token
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, core_settings.SECRET_KEY, algorithms=[core_settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user: User = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# get_current_active_user
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user