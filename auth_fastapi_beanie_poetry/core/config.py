from pydantic_settings import BaseSettings

class CoreSettings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool
    ENVIRONMENT: str
    MONGODB_URL: str
    MONGODB_NAME: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    ALLOWED_ORIGINS: list[str]

    class Config:
        env_file = ".env"

core_settings = CoreSettings()
