from datetime import datetime
from enum import Enum
from beanie import Document
from pydantic import Field
from auth_fastapi_beanie_poetry.models.token import Token, TokenData

class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class User(Document):
    username: str
    email: str
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = None
    disabled: bool | None = None
    token: Token | None = None
    token_data: TokenData | None = None
    role: Role = Role.USER

    class Settings:
        collection = "users"

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@ibm.com",
                "hashed_password": "password",
                "created_at": "2021-01-01T00:00:00",
                "updated_at": "2021-01-01T00:00:00",
                "disables": False,
                "token": None,
                "token_data": None,
                "role": "Role.USER"
            }
        }

