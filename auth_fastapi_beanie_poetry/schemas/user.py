from pydantic import BaseModel, EmailStr, Field, GetCoreSchemaHandler, GetJsonSchemaHandler, ValidationInfo, field_validator, StringConstraints
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema
from auth_fastapi_beanie_poetry.models.token import Token, TokenData
from auth_fastapi_beanie_poetry.models.user import Role
from typing import Annotated, Any, ClassVar

# Username: min 3 chars, max 30 chars, indexed and unique
UsernameType = Annotated[str, StringConstraints(min_length=3, max_length=30, pattern="^[a-zA-Z0-9_]+$")]

# Validate password
    # at least 1 uppercase letter
    # at least 1 lowercase letter
    # at least 1 number
    # at least 1 special character
    # min 8 chars, max 128 chars

def validate_password(value: str) -> str:
    if len(value) < 8 or len(value) > 128:
        raise ValueError("Password must be between 8 and 128 characters long")
    if not any(char.isupper() for char in value):
        raise ValueError("Password must contain at least one uppercase letter")
    if not any(char.islower() for char in value):
        raise ValueError("Password must contain at least one lowercase letter")
    if not any(char.isdigit() for char in value):
        raise ValueError("Password must contain at least one number")
    if not any(char in "!@#$%^&*" for char in value):
        raise ValueError("Password must contain at least one special character")
    return value

class UserBase(BaseModel):
    username: UsernameType
    email: EmailStr

class UserCreate(UserBase):
    password: str
    disabled: bool | None = None
    role: Role | None = None

    @field_validator("password")
    @classmethod
    def validate_password_field(cls, value: str, info: ValidationInfo) -> str:
        return validate_password(value)



class UserInDB(UserBase):
    hashed_password: str
    disabled: bool | None = None
    token: Token | None = None
    token_data: TokenData | None = None
    role: Role | None = None

class User(UserBase):
    pass

class LoginCredentials(BaseModel):
    identifier: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password_field(cls, value: str, info: ValidationInfo) -> str:
        return validate_password(value)
    
# Define request/response schemas
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_password_field(cls, value: str, info: ValidationInfo) -> str:
        return validate_password(value)