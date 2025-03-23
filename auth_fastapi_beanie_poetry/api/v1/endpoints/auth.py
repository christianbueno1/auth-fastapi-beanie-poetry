from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, Response, Cookie
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from auth_fastapi_beanie_poetry.core.token import create_access_token, create_refresh_token
from auth_fastapi_beanie_poetry.schemas.user import User, UserCreate, UserInDB
from auth_fastapi_beanie_poetry.services import auth_services
from auth_fastapi_beanie_poetry.models.token import Token, TokenData, TokenPayload
from auth_fastapi_beanie_poetry.models.user import Role, User as UserModel
from auth_fastapi_beanie_poetry.core.config import core_settings

router = APIRouter()

# @router.post("/signup")
# async def signup(user: UserCreate):
#     user = await create_user(user)
#     return {"message": "User created"}


@router.post("/token")
async def login(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> JSONResponse:
    form_identifier = form_data.username
    form_password = form_data.password
    try:
        user = await auth_services.authenticate_user_or_email(form_identifier, form_password)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    ####
    # sub, exp, mode
    data = TokenPayload(sub=user.email, exp=None, mode=None)
    # print(f"access_token_expires: {core_settings.ACCESS_TOKEN_EXPIRE_MINUTES}")
    # Create access and refresh tokens
    access_token: str = create_access_token(data=data, expires_delta=timedelta(minutes=core_settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token: str = create_refresh_token(data=data, expires_delta=timedelta(days=core_settings.REFRESH_TOKEN_EXPIRE_DAYS))
    # Store the tokens in the database
    token = Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
    token_data = TokenData(username=user.username, email=user.email)
    # await UserModel.find_one(UserModel.email == user.email).set({UserModel.token: token, UserModel.token_data: token_data, UserModel.role: Role.USER})
    await UserModel.find_one(UserModel.email == user.email).set({UserModel.token: token, UserModel.token_data: token_data})

    # Create a content dictionary for the response
    content = {
        "message": "Login successful",
        "username": user.username,
        "email": user.email,
        "role": user.role,
    }
    
    # Create response object directly
    response = JSONResponse(content=content)

    # Set HttpOnly cookies
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        # value=access_token,
        httponly=True,
        max_age=core_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=core_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=core_settings.ENVIRONMENT == "production",  # Only secure in production
        # quote_cookie_value=False,  # Disable quoting of the cookie value
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=core_settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        expires=core_settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        samesite="lax",
        secure=core_settings.ENVIRONMENT == "production",  # Only secure in production
        path="/api/v1/auth/refresh-token",  # Restrict to refresh endpoint
    )

    # Return user info without exposing tokens in response body
    # return JSONResponse(content={
    #     "message": "Login successful",
    #     "username": user.username,
    #     "email": user.email,
    #     "role": user.role,
    # })
    return response

# Add a new endpoint to test authentication directly
@router.get("/token-debug")
async def token_debug(request: Request):
    """Debug endpoint to see what cookies are being received"""
    cookies = request.cookies
    headers = dict(request.headers)
    
    return {
        "cookies": cookies,
        "auth_header": headers.get("authorization"),
        "cookie_access_token": cookies.get("access_token")
    }

@router.post("/refresh-token")
# async def refresh_token(response: Response, refresh_token: Annotated[str, Depends(auth_services.refresh_token)]):
async def refresh_token(response: Response, refresh_token: Annotated[str | None, Cookie()] = None) -> JSONResponse:
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token not provided")
    
    # Using existing refresh token service but passing the cookie value
    new_access_token = await auth_services.refresh_token(refresh_token)

    # Get token expiration from settings
    expires = core_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60

    # Set the new access token as HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value=f"Bearer {new_access_token}",
        httponly=True,
        max_age=expires,
        expires=expires,
        samesite="lax",
        secure=core_settings.ENVIRONMENT == "production", 
    )
    
    return JSONResponse(content={"message": "Token refreshed successfully"})

# /users (protected) - For admins to manage users
# Only admin users can access this endpoint and create users with specific roles: admin, user, guest
# The first admin user would typically be created directly in the database or through a separate initialization process
@router.post("/users", response_model=User)
async def create_user(user: UserCreate, current_user: Annotated[User, Depends(auth_services.check_admin_role)]):
    try:
        user: UserInDB = await auth_services.create_user(user)
        user_in_db = User(**user.model_dump())
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail="Error in create_user")
    return user_in_db

@router.get("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(auth_services.check_user_role)]):
    # print(f"Current user: {current_user}")
    if current_user is None:
        raise HTTPException(status_code=400, detail="User not found")
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="User is disabled")
    return current_user

@router.get("/users/me/items")
async def read_own_items(current_user: Annotated[User, Depends(auth_services.check_user_role)]):
    return [{"item_id": "Foo", "ownert": current_user.username}]

@router.get("/admin/dashboards", response_model=dict)
async def admin_dashboard(current_user: Annotated[User, Depends(auth_services.check_admin_role)]):
    """Get admin-specific dashboard information."""
    # Get system statistics and information only relevant to admins
    user_count = await UserModel.find().count()
    recent_users = await UserModel.find().sort(-UserModel.created_at).limit(5).to_list()
    recent_user_data = [
        {"username": user.username, "email": user.email, "role": user.role, "created_at": user.created_at}
        for user in recent_users
    ]
    
    return {
        "admin": {
            "username": current_user.username,
            "email": current_user.email,
            "role": current_user.role
        },
        "stats": {
            "total_users": user_count,
            "recent_users": recent_user_data
        }
    }

# /signup (public) - For new users to self-register
# Be publicly accessible (no token required)
# Automatically assign the basic user role
@router.post("/signup")
async def signup(user: UserCreate):
    try:
        # Force user role to USER
        user_dict = user.model_dump()
        user_dict["role"] = Role.USER
        user_create = UserCreate(**user_dict)
        user_in_db: UserInDB = await auth_services.create_user(user_create)
        user = User(**user_in_db.model_dump())
    except HTTPException as e:
        print(f"Error: {e.detail}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail="Error creating user or User already exists")

    return {"message": "User created successfully", "user": user}

@router.post("/clear-tokens")
async def clear_tokens():
    result = await auth_services.clear_all_tokens()
    # print(f"Result: {result}")
    return {"message": "Tokens cleared", "modified_count": result.modified_count}

@router.post("/logout")
async def logout(response: Response):
    """Clear authentication cookies"""
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token", path="/api/v1/auth/refresh-token")
    return {"message": "Logged out successfully"}