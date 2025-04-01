from datetime import datetime
from enum import Enum
from beanie import Document, Indexed
from pydantic import Field, EmailStr, StringConstraints
from typing import Annotated
from auth_fastapi_beanie_poetry.models.token import Token, TokenData
# from auth_fastapi_beanie_poetry.schemas.user import UsernameType

class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

# Username: min 3 chars, max 30 chars, indexed and unique
UsernameType = Annotated[str, StringConstraints(min_length=3, max_length=30, pattern="^[a-zA-Z0-9_.-]+$"), Indexed(unique=True)]

class User(Document):
    username: UsernameType
    
    # Email: validated format, indexed and unique
    email: Annotated[EmailStr, Indexed(unique=True)]
    
    # Password hash
    hashed_password: Annotated[str, StringConstraints(min_length=60, max_length=60)]
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = None
    
    # Status and tokens
    disabled: bool = Field(default=False)
    token: Token | None = None
    token_data: TokenData | None = None
    role: Role = Field(default=Role.USER)
    
    # Last password reset
    last_password_reset: datetime | None = None

    class Settings:
        # collection = "users"
        name = "users"
        use_state_management = True

    class Config:
        json_schema_extra = {
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

