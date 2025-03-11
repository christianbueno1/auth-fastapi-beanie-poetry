from datetime import datetime
from enum import Enum
from typing import TypedDict
from pydantic import BaseModel

class TokenMode(str, Enum):
    access_token = "access_token"
    refresh_token = "refresh_token"

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        json_schema_extra = {
            "example": {
                "token_type": "bearer",
            }
        }

class TokenData(BaseModel):
    username: str | None = None
    email: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@ibm.com",
            }
        }
# use exp as key for jwt.encode
class TokenPayload(TypedDict):
    sub: str | None = None
    exp: datetime | None = None
    mode: TokenMode | None = None