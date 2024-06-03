from datetime import datetime
from beanie import Document


class User(Document):
    username: str
    email: str
    hashed_password: str
    created_at: datetime = datetime.now()

    class Settings:
        collection = "users"

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@ibm.com",
                "hashed_password": "password",
                "created_at": "2021-01-01T00:00:00",
            }
        }