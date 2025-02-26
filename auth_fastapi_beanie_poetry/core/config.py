from pydantic_settings import BaseSettings

class CoreSettings(BaseSettings):
    DATABASE_URL: str
    DATABASE_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    FRONTEND_URL: str  # Add this field

    class Config:
        env_file = ".env.dev"

core_settings = CoreSettings()
