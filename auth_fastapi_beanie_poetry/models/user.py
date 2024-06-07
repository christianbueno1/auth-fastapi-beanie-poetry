from datetime import datetime
from beanie import Document
from pydantic import Field


class User(Document):
    username: str
    email: str
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = None
    # role: str | None = None # user, admin, superadmin
    # disabled: bool | None = None

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
            }
        }

