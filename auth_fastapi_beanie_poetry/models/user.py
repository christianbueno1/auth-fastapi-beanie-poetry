from datetime import datetime
from enum import Enum
from beanie import Document, Indexed
from pydantic import Field, EmailStr
from auth_fastapi_beanie_poetry.models.token import Token, TokenData
from typing import Annotated

class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class User(Document):
    username: Annotated[str, Indexed(unique=True)]
    email: Annotated[EmailStr, Indexed(unique=True)]
    # Password hash
    hashed_password: str
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = None
    
    # Status and tokens
    disabled: bool = Field(default=False)
    token: Token | None = None
    token_data: TokenData | None = None
    role: Role = Field(default=Role.USER)

    class Settings:
        collection = "users"
        name = "users"
        use_state_management = True

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "hashed_password": "hashed_password_string",
                "created_at": "2021-01-01T00:00:00",
                "updated_at": "2021-01-01T00:00:00",
                "disabled": False,
                "token": None,
                "token_data": None,
                "role": "user"
            }
        }

