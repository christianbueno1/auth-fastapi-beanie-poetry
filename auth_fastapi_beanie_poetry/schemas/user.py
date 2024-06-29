from pydantic import BaseModel, EmailStr

from auth_fastapi_beanie_poetry.models.token import Token, TokenData


class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str
    disabled: bool | None = None
    token: Token | None = None
    token_data: TokenData | None = None

class User(UserBase):
    pass