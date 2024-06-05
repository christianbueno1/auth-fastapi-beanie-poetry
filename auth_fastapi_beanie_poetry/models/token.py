from beanie import Document


class Token(Document):
    access_token: str
    token_type: str

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJ123",
                "token_type": "bearer",
            }
        }

class TokenData(Document):
    username: str | None = None
    email: str | None = None

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@ibm.com",
            }
        }