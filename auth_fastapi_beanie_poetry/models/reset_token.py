from datetime import datetime
from beanie import Document
from pydantic import Field

class ResetToken(Document):
    user_email: str
    token: str
    expires_at: datetime
    used: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "tokens"
