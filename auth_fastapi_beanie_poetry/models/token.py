from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        schema_extra = {
            "example": {
                "token_type": "bearer",
            }
        }

class TokenData(BaseModel):
    username: str | None = None
    email: str | None = None

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@ibm.com",
            }
        }