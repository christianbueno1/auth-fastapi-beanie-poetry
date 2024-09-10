from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder
import jwt
from auth_fastapi_beanie_poetry.crud.user import get_user, get_user_by_email
from auth_fastapi_beanie_poetry.models.token import TokenData, Token, TokenMode, TokenPayload
from auth_fastapi_beanie_poetry.models.user import Role, User as UserModel
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

async def authenticate_user_by_email(email: str, password: str) -> UserInDB | bool:
    user: UserInDB = await get_user_by_email(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# get_current_user get_current_active_user
#
# get_current_user
# email is the sub claim of the JWT token
# token= sub, exp, mode
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: TokenPayload = jwt.decode(token, core_settings.SECRET_KEY, algorithms=[core_settings.ALGORITHM])
        email: str = payload.get("sub")
        # print(f"email: {email}")
        mode: TokenMode = payload.get("mode")
        # print(f"mode: {mode}")
        if email is None:
            raise credentials_exception
        if mode != TokenMode.access_token:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user: UserInDB = await get_user_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

# get_current_active_user
async def get_current_active_user(current_user: Annotated[UserInDB, Depends(get_current_user)]) -> UserInDB:
    if current_user.disabled:
        raise HTTPException(status_code=403, detail="Inactive user")
    return current_user

async def check_user_role(user: Annotated[UserInDB, Depends(get_current_active_user)] ) -> UserInDB:
    permissions_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    if user.role == Role.USER:
        return user
    else:
        raise permissions_exception

async def check_admin_role(user: Annotated[UserInDB, Depends(get_current_active_user)] ) -> UserInDB:
    permissions_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    if user.role == Role.ADMIN:
        return user
    else:
        raise permissions_exception

async def check_guest_role(user: Annotated[UserInDB, Depends(get_current_active_user)] ) -> UserInDB:
    permissions_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    if user.role == Role.GUEST:
        return user
    else:
        raise permissions_exception

# refresh token
async def refresh_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload: TokenPayload = jwt.decode(token, core_settings.SECRET_KEY, algorithms=[core_settings.ALGORITHM])
        email: str = payload.get("sub")
        # "mode": "refresh_token"
        token_mode: TokenMode = payload.get("mode")
        if email is None and token_mode is None:
            raise credentials_exception
        if token_mode != TokenMode.refresh_token:
            raise credentials_exception
        user_in_db: UserInDB = await get_user_by_email(email=email)
        if user_in_db is None:
            raise credentials_exception
        else:
            if token != user_in_db.token.refresh_token:
                raise credentials_exception
        data = TokenPayload(sub=user_in_db.email, exp=None, mode=None)
        # data: TokenPayload = { "sub": user_in_db.email, 'exp': None, 'mode': None }

        refresh_token = create_refresh_token(data=data, expires_delta=timedelta(days=core_settings.REFRESH_TOKEN_EXPIRE_DAYS))
        
        await UserModel.find_one(UserModel.email == user_in_db.email).set({UserModel.token.refresh_token: refresh_token})
        
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