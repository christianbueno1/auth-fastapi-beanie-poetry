from datetime import timedelta, datetime, timezone
from typing import Annotated
import secrets
import string

from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder
import jwt
# from jose import JWTError, jwt
from auth_fastapi_beanie_poetry.crud.user import get_user, get_user_by_email
from auth_fastapi_beanie_poetry.models.token import TokenData, Token, TokenMode, TokenPayload
from auth_fastapi_beanie_poetry.models.user import Role, User as UserModel
from auth_fastapi_beanie_poetry.core.security import get_password_hash, verify_password
from auth_fastapi_beanie_poetry.core.config import core_settings
from auth_fastapi_beanie_poetry.core.token import create_refresh_token, create_access_token
from jwt.exceptions import InvalidTokenError

from auth_fastapi_beanie_poetry.schemas.user import UserCreate, UserInDB
from pymongo.errors import DuplicateKeyError
from auth_fastapi_beanie_poetry.models.reset_token import ResetToken

# if core_settings.ENVIRONMENT == "production":
#     oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://authapi.christianbueno.tech/api/v1/auth/token")
# elif core_settings.ENVIRONMENT == "development":
#     oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{core_settings.PREFIX.lstrip('/')}/token")

# Relative path is always the right approach, regardless of environment
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{core_settings.PREFIX.lstrip('/')}/token", auto_error=False
)

# Create a function that combines both token sources
async def get_token_from_request(
    token: Annotated[str | None, Depends(oauth2_scheme)] = None,
    access_token: Annotated[str | None, Cookie()] = None
) -> str | None:
    # For debugging
    # print(f"OAuth2 token: {token}")
    # print(f"Cookie token: {access_token}")
    if token:
        return token
    if access_token:
        # print(f"Access token from cookie: {access_token}")
        # access_token = access_token.strip('"')
        # Remove the "Bearer " prefix if it exists
        if access_token.startswith("Bearer "):
            access_token = access_token[7:]
            # print(f"Access token without Bearer: {access_token}")
        return access_token
    
    # Return header token if available, otherwise cookie
    # return token or access_token
    return None


async def authenticate_user(username: str, password: str) -> UserInDB:
    user: UserInDB = await get_user(username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Valid username but Invalid password")
    return user

async def authenticate_user_by_email(email: str, password: str) -> UserInDB:
    user: UserInDB = await get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Valid email but Invalid password")
    return user

async def authenticate_user_or_email(identifier: str, password: str) -> UserInDB:
    try:
        user: UserInDB = await authenticate_user_by_email(identifier, password)
        return user
    except HTTPException as e:
        if e.detail == "Invalid email":
            try:
                user: UserInDB = await authenticate_user(identifier, password)
                return user
            except HTTPException as e:
                if e.detail == "Invalid username":
                    raise HTTPException(status_code=400, detail="Invalid email or username")
                elif e.detail == "Valid username but Invalid password":
                    raise e
                else:
                    raise e
        else:
            raise e

    
    
    
########################################
# get_current_user get_current_active_user
#
# get_current_user
# email is the sub claim of the JWT token
# token= sub, exp, mode
# async def get_current_user(token: Annotated[str | None, Depends(oauth2_scheme)] = None, access_token: Annotated[str | None, Cookie()] = None) -> UserInDB:
async def get_current_user(token: Annotated[str | None, Depends(get_token_from_request)]) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # print(f"Final token received: {token}")
    
    if not token:
        print("No token provided")
        raise credentials_exception

    try:
        # Debug decoded token value
        # decoded_token_parts = token.split('.')
        # if len(decoded_token_parts) != 3:
        #     print("WARNING: Token does not appear to be a valid JWT (should have 3 parts)")
            
        # print(f"token: {token}")
        # print(f"access_token_expires: {core_settings.ACCESS_TOKEN_EXPIRE_MINUTES}")
        payload: TokenPayload = jwt.decode(token, core_settings.JWT_SECRET, algorithms=[core_settings.JWT_ALGORITHM])
        # print(f"payload: {payload}")
        email: str = payload.get("sub")
        # print(f"email: {email}")
        mode: TokenMode = payload.get("mode")
        # print(f"mode: {mode}")
        if email is None or mode != "access_token":
            raise credentials_exception
        if mode != TokenMode.access_token:
            raise credentials_exception
        user: UserInDB = await get_user_by_email(email=email)
        if token != user.token.access_token:
            raise credentials_exception
        # token_data = TokenData(username=user.username, email=email)
        
        # print(f"token_data: {token_data}")
    except InvalidTokenError as e:
        print(f"JWT decode error: {str(e)}")
        raise credentials_exception
    except AttributeError as e:
        print(f"Attribute error: {str(e)}")
        raise credentials_exception
    # print(f"user-: {user}")
    if user is None:
        raise credentials_exception
    return user

# get_current_active_user
async def get_current_active_user(current_user: Annotated[UserInDB, Depends(get_current_user)]) -> UserInDB:
    if current_user.disabled:
        raise HTTPException(status_code=403, detail="Inactive user")
    return current_user

async def check_user_role(user: Annotated[UserInDB, Depends(get_current_active_user)] ) -> UserInDB:
    permissions_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    if user.role == Role.USER:
        return user
    else:
        raise permissions_exception

async def check_admin_role(user: Annotated[UserInDB, Depends(get_current_active_user)] ) -> UserInDB:
    permissions_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    if user.role == Role.ADMIN:
        return user
    else:
        raise permissions_exception

async def check_guest_role(user: Annotated[UserInDB, Depends(get_current_active_user)] ) -> UserInDB:
    permissions_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    if user.role == Role.GUEST:
        return user
    else:
        raise permissions_exception

# refresh token
async def refresh_token(token: Annotated[str, Depends(oauth2_scheme)]) -> Token:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload: TokenPayload = jwt.decode(token, core_settings.JWT_SECRET, algorithms=[core_settings.JWT_ALGORITHM])
        # print(f"payload: {payload}")
        email: str = payload.get("sub")
        # "mode": "refresh_token"
        token_mode: TokenMode = payload.get("mode")
        if email is None and token_mode is None:
            raise credentials_exception
        if token_mode != TokenMode.refresh_token:
            raise credentials_exception
        user_in_db: UserInDB = await get_user_by_email(email=email)
        # print(f"user_in_db.token.refresh_token: {user_in_db.token.refresh_token}")
        if user_in_db is None:
            raise credentials_exception
        else:
            # compare the refresh token from the payload with the one in the database
            if token != user_in_db.token.refresh_token:
                raise credentials_exception
        data = TokenPayload(sub=user_in_db.email, exp=None, mode=None)

        access_token = create_access_token(data=data, expires_delta=timedelta(minutes=core_settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        
        refresh_token = create_refresh_token(data=data, expires_delta=timedelta(days=core_settings.REFRESH_TOKEN_EXPIRE_DAYS))
        # print(f"refresh_token::: {refresh_token}")
        
        new_token: Token = Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
        
        await UserModel.find_one(UserModel.email == user_in_db.email).set({UserModel.token: new_token})
        
    except InvalidTokenError:
        raise credentials_exception
    return new_token

# create_user
async def create_user(user: UserCreate) -> UserInDB:
    try:
        hashed_password = get_password_hash(user.password)
        new_user = UserModel(**user.model_dump(), hashed_password=hashed_password)
        # print(f"new_user: {new_user}")
        await new_user.insert()
        return new_user
    except DuplicateKeyError as e:
        if "username" in str(e):
            raise HTTPException(
                status_code=400, 
                detail="User with this username already exists"
            )
        elif "email" in str(e):
            raise HTTPException(
                status_code=400, 
                detail="User with this email already exists"
            )
        else:
            raise HTTPException(
                status_code=400, 
                detail="User with this username or email already exists"
            )
    
    

async def clear_all_tokens():
    # Clear tokens for all users by updating the token and token_data fields to None.
    update_result = await UserModel.find_all().update({
        "$set": {
            "token": None,
            "token_data": None
        }
    })
    return update_result

# Password reset functions
async def generate_password_reset_token(email: str) -> str:
    """Generate a password reset token and store it in the token collection"""
    user = await get_user_by_email(email)
    
    # Avoid leaking user existence, but still generate a token for security
    if not user:
        # Return a fake token for non-existent users (for security)
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(64))
    
    # Create secure token
    token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(64))
    
    # Set token expiration (1 hour)
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
    
    # Create token document
    reset_token = ResetToken(
        user_email=email,
        token=token,
        expires_at=expires_at
    )
    
    # Save token to database
    await reset_token.insert()
    
    return token

async def verify_password_reset_token(token: str) -> str:
    """Verify a password reset token and return the associated email"""
    # Find token in database
    reset_token = await ResetToken.find_one(
        ResetToken.token == token,
        ResetToken.used == False,
        ResetToken.expires_at > datetime.now(timezone.utc)
    )
    
    if not reset_token:
        raise HTTPException(
            status_code=400, 
            detail="Invalid or expired password reset token"
        )
    
    return reset_token.user_email

async def reset_password_with_token(token: str, new_password: str) -> bool:
    """Reset a user's password using a reset token"""
    # Verify token and get email
    user_email = await verify_password_reset_token(token)
    
    # Get user
    user: UserInDB = await get_user_by_email(user_email)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    # Update password
    hashed_password = get_password_hash(new_password)
    await UserModel.find_one(UserModel.email == user_email).update({
        "$set": {
            "hashed_password": hashed_password,
            "last_password_reset": datetime.now(timezone.utc)
        }
    })
    
    # Mark token as used
    await ResetToken.find_one(ResetToken.token == token).update({
        "$set": {"used": True}
    })
    
    # Clear sessions for security
    await UserModel.find_one(UserModel.email == user_email).set({
        "token": None,
        "token_data": None
    })
    
    return True