from pydantic_settings import BaseSettings

class CoreSettings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool
    ENVIRONMENT: str
    FASTAPI_PORT: int
    API_BASE_URL: str
    API_PREFIX: str
    API_FULL_URL: str
    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_DB: str
    MONGO_HOST: str
    MONGO_PORT: int
    MONGODB_URL: str
    PODMAN_POD_NAME: str
    PODMAN_MONGO_IMAGE_NAME: str
    PODMAN_MONGO_IMAGE_TAG: str
    PODMAN_MONGO_IMAGE: str
    PODMAN_MONGO_PORT: int
    PODMAN_MONGO_CONTAINER: str
    PODMAN_FASTAPI_PORT: int
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    ALLOWED_ORIGINS: list[str]
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_SSL_TLS: bool
    USE_CREDENTIALS: bool

    class Config:
        env_file = ".env"

core_settings = CoreSettings()
