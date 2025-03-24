from datetime import datetime, timedelta, timezone
import jwt, json
from auth_fastapi_beanie_poetry.core.config import core_settings
from auth_fastapi_beanie_poetry.models.token import TokenMode, TokenPayload


def create_access_token(data: TokenPayload, expires_delta: timedelta | None = None) -> str: 
    if expires_delta:
        # print(f"expires_delta: {expires_delta}")
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    data["exp"] = expire
    data["mode"] = TokenMode.access_token
    encoded_jwt: str = jwt.encode(data, core_settings.JWT_SECRET, algorithm=core_settings.JWT_ALGORITHM)
    
    return encoded_jwt

def create_refresh_token(data: TokenPayload, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=30)
    data["exp"] = expire
    data["mode"] = TokenMode.refresh_token
    encoded_jwt: str = jwt.encode(data, core_settings.JWT_SECRET, algorithm=core_settings.JWT_ALGORITHM)
    
    return encoded_jwt