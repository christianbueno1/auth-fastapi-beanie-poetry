from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from auth_fastapi_beanie_poetry.core.token import create_access_token, create_refresh_token
from auth_fastapi_beanie_poetry.schemas.user import User, UserCreate, UserInDB
# from auth_fastapi_beanie_poetry.services.auth_services import authenticate_user
from auth_fastapi_beanie_poetry.services import auth_services
from auth_fastapi_beanie_poetry.models.token import Token
from auth_fastapi_beanie_poetry.core.config import core_settings
# from app.schemas.user import UserCreate
# from app.services.auth_service import create_user, authenticate_user

router = APIRouter()

# @router.post("/signup")
# async def signup(user: UserCreate):
#     user = await create_user(user)
#     return {"message": "User created"}


@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await auth_services.authenticate_user(form_data.username, form_data.password)
    print(f"User: {user}")
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token: str = create_access_token(data={"sub": user.username}, expires_delta=timedelta(core_settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    print(f"Access token: {access_token}")
    # create refresh token
    refresh_token: str = create_refresh_token(data={"sub": user.username}, expires_delta=timedelta(core_settings.REFRESH_TOKEN_EXPIRE_DAYS))
    # return {"access_token": access_token, "token_type": "bearer"}
    return Token(
        access_token=access_token, 
        refresh_token=refresh_token,
        token_type="bearer")

@router.get("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(auth_services.get_current_active_user)]):
    return current_user

@router.get("/users/me/items")
async def read_own_items(current_user: Annotated[User, Depends(auth_services.get_current_active_user)]):
    return [{"item_id": "Foo", "ownert": current_user.username}]

# register endpoints
@router.post("/signup")
async def signup(user: UserCreate):
    try :
        user: UserInDB = await auth_services.create_user(user)
        user_in_db = User(**user.model_dump())
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail="User already exists")

    return {"message": "User created"}