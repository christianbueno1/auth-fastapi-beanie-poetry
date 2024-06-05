import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = "My FastAPI Application"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() in ["true", "1"]
    # DATABASE_URL: str = os.getenv("DATABASE_URL")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL")

settings = Settings()
