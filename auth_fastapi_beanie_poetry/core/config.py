import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class CoreSettings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    

    class Config:
        env_file = ".env"

core_settings = CoreSettings()
