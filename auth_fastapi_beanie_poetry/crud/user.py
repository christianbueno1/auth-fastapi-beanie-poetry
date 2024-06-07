from typing import Annotated
from beanie import PydanticObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from auth_fastapi_beanie_poetry.models.token import TokenData
from auth_fastapi_beanie_poetry.models.user import User
from auth_fastapi_beanie_poetry.core.config import core_settings
from jwt.exceptions import InvalidTokenError
from auth_fastapi_beanie_poetry.schemas.user import UserInDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_user(username: str) -> User | None:
    # user = await User.find_one({"username": username})
    user = await User.find_one(User.username == username)
    user_in_db = User(**user.model_dump())
    return user_in_db

async def get_user_by_email(email: str) -> User | None:
    user = await User.find_one(User.email == email)
    user_in_db = User(**user.model_dump())
    return user_in_db

# create_user

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