from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder
import jwt
from auth_fastapi_beanie_poetry.crud.user import get_user
from auth_fastapi_beanie_poetry.models.token import TokenData, Token
from auth_fastapi_beanie_poetry.models.user import User as UserModel
from auth_fastapi_beanie_poetry.core.security import get_password_hash, verify_password
from auth_fastapi_beanie_poetry.core.config import core_settings
from auth_fastapi_beanie_poetry.core.token import create_refresh_token, create_access_token
from jwt.exceptions import InvalidTokenError

from auth_fastapi_beanie_poetry.schemas.user import UserCreate, UserInDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def authenticate_user(username: str, password: str) -> UserInDB | bool:
    user: UserInDB = await get_user(username)
    # user_in_db = UserInDB(**user.model_dump())
    # if user is None:
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# get_current_user get_current_active_user
#
# get_current_user
# username is the sub claim of the JWT token
# token= sub, exp, mode
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, core_settings.SECRET_KEY, algorithms=[core_settings.ALGORITHM])
        username: str = payload.get("sub")
        print(f"username: {username}")
        mode: str = payload.get("mode")
        print(f"mode: {mode}")
        if username is None:
            raise credentials_exception
        if mode != "access_token":
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user: UserInDB = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# get_current_active_user
async def get_current_active_user(current_user: Annotated[UserInDB, Depends(get_current_user)]) -> UserInDB:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# refresh token
async def refresh_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, core_settings.SECRET_KEY, algorithms=[core_settings.ALGORITHM])
        username: str = payload.get("sub")
        # "mode": "refresh_token"
        token_mode: str = payload.get("mode")
        if username is None and token_mode is None:
            raise credentials_exception
        if token_mode != "refresh_token":
            raise credentials_exception
        user_in_db: UserInDB = await get_user(username)
        if user_in_db is None:
            raise credentials_exception
        else:
            if token != user_in_db.token.refresh_token:
                raise credentials_exception
        data = { "sub": user_in_db.username}
        refresh_token = create_refresh_token(data=data, expires_delta=timedelta(days=core_settings.REFRESH_TOKEN_EXPIRE_DAYS))
        await UserModel.find_one(UserModel.username == user_in_db.username).set({UserModel.token.refresh_token: refresh_token})
        access_token = create_access_token(data=data, expires_delta=timedelta(minutes=core_settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        new_token: Token = Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
    except InvalidTokenError:
        raise credentials_exception
    return {
        **jsonable_encoder(new_token)
    }

# create_user
async def create_user(user: UserCreate) -> UserInDB:
    hashedd_password = get_password_hash(user.password)

    return await UserInDB(**user.create())