from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from auth_fastapi_beanie_poetry.core.token import create_access_token
from auth_fastapi_beanie_poetry.services.auth_services import authenticate_user
from auth_fastapi_beanie_poetry.models.token import Token
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
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}