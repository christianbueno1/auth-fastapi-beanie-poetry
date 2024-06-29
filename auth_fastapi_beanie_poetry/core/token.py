from datetime import datetime, timedelta, timezone
import jwt
from auth_fastapi_beanie_poetry.core.config import core_settings


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str: 
    to_encode = data.copy()
    if expires_delta:
        print(f"expires_delta: {expires_delta}")
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire, "mode": "access_token"})
    encoded_jwt: str = jwt.encode(to_encode, core_settings.SECRET_KEY, algorithm=core_settings.ALGORITHM)
    
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire, "mode": "refresh_token"})
    encoded_jwt: str = jwt.encode(to_encode, core_settings.SECRET_KEY, algorithm=core_settings.ALGORITHM)
    
    return encoded_jwt