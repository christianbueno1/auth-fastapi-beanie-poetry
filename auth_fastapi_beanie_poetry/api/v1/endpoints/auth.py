from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from auth_fastapi_beanie_poetry.core.token import create_access_token
from auth_fastapi_beanie_poetry.schemas.user import User
from auth_fastapi_beanie_poetry.services.auth_services import authenticate_user
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
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(core_settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    # return {"access_token": access_token, "token_type": "bearer"}
    return Token(access_token=access_token, token_type="bearer")

@router.get("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(auth_service.get_current_active_user)]):
    return current_user


