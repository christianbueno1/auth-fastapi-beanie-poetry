from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from auth_fastapi_beanie_poetry.core.token import create_access_token, create_refresh_token
from auth_fastapi_beanie_poetry.schemas.user import ForgotPasswordRequest, LoginCredentials, ResetPasswordRequest, User, UserCreate, UserInDB
# from auth_fastapi_beanie_poetry.services.auth_services import authenticate_user
from auth_fastapi_beanie_poetry.services import auth_services, email_services
from auth_fastapi_beanie_poetry.models.token import Token, TokenData, TokenPayload
from auth_fastapi_beanie_poetry.models.user import Role, User as UserModel
from auth_fastapi_beanie_poetry.core.config import core_settings
import json
# from app.schemas.user import UserCreate
# from app.services.auth_service import create_user, authenticate_user

router = APIRouter()
# @router.post("/signup")
# async def signup(user: UserCreate):
#     user = await create_user(user)
#     return {"message": "User created"}


@router.post("/token")
async def login(response: Response, credentials: LoginCredentials) -> JSONResponse:
    identifier = credentials.identifier
    password = credentials.password
    try:
        user = await auth_services.authenticate_user_or_email(identifier, password)
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
    # content parameter = response body
    # Content-type header is set to application/json
    response = JSONResponse(content=content)

    # print(f"Setting access_token: {access_token}")

    # response.set_cookie(
    #     key="Authorization",  # Cookie name
    #     value=f"Bearer {token}",  # Value, typically a JWT token
    #     httponly=True,  # Prevents access via JavaScript
    #     secure=True,  # Ensures cookies are sent only over HTTPS
    #     samesite="none",  # Allows cross-domain cookies
    #     domain=".christianbueno.tech",  # Matches your backend domain
    #     max_age=1800,  # Cookie lifetime in seconds (30 minutes)
    #     expires=1800  # Sets expiration time explicitly
    # )

    # Set HttpOnly cookies
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        # domain="localhost",  # Set domain to localhost for local testing
        domain=".christianbueno.tech",  # Matches your backend domain
        path="/api/v1/auth",  # Restrict to auth endpoint
        # value=access_token,
        httponly=True,
        max_age=core_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=core_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="none" if core_settings.ENVIRONMENT == "production" else "lax",
        secure=core_settings.ENVIRONMENT == "production",  # Only secure in production
        # quote_cookie_value=False,  # Disable quoting of the cookie value
        # path="/api/v1/auth/token",  # Restrict to token endpoint
        # access_token avaible to all endpoints
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        # domain="localhost",  # Set domain to localhost for local testing
        domain=".christianbueno.tech",  # Matches your backend domain
        path="/api/v1/auth/refresh-token",  # Restrict to refresh endpoint
        httponly=True,
        max_age=core_settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        expires=core_settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        samesite="none" if core_settings.ENVIRONMENT == "production" else "lax",
        secure=core_settings.ENVIRONMENT == "production",  # Only secure in production
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


# @router.post("/refresh-token")
# async def refresh_token(token: Annotated[str, Depends(auth_services.refresh_token)]):
#     return token

@router.post("/refresh-token")
async def refresh_token(response: Response, user: Annotated[UserInDB, Depends(auth_services.get_current_active_user)]) -> Response:
    refresh_token_value = user.token.refresh_token
    if not refresh_token_value:
        raise HTTPException(status_code=401, detail="Refresh token not provided")
    
    # Create new tokens using your refresh logic
    token: Token = await auth_services.refresh_token(refresh_token_value)
    print(f"Token: {token}")
    new_access_token = token.access_token
    new_refresh_token = token.refresh_token

    # Get expiration values from settings
    expires = core_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    expires_refresh_token = core_settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60

    # Write response content to the same Response instance so cookies are included
    content = {
        "message": "Token refreshed successfully",
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "expires_in": expires,
        "token_type": "bearer"
    }
    response = JSONResponse(content=content)

    # Order is important: set cookies after setting the response content, if you set the cookies before the content, the cookies will not be included in the response
    
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
    
    # Set the new refresh token as HttpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        max_age=expires_refresh_token,
        expires=expires_refresh_token,
        samesite="lax",
        secure=core_settings.ENVIRONMENT == "production",
        path="/api/v1/auth/refresh-token",  # Restrict to refresh endpoint
    )
    
    return response


# /users (protected) - For admins to manage users
# Only admin users can access this endpoint and create users with specific roles: admin, user, guest
# The first admin user would typically be created directly in the database or through a separate initialization process
@router.post("/admin/users", response_model=User)
async def create_user(user: UserCreate, current_user: Annotated[User, Depends(auth_services.check_admin_role)]):
    try :
        user: UserInDB = await auth_services.create_user(user)
        # print(f"User: {user}")
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
    return [{"item_id": "Foo", "owner": current_user.username}]

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
    print(f"Result: {result}")
    return {"message": "Tokens cleared", "modified_count": result.modified_count}

@router.post("/logout")
async def logout(response: Response, current_user: Annotated[UserInDB, Depends(auth_services.get_current_active_user)]):
    """Clear authentication cookies and revoke tokens"""
    # Revoke tokens by setting token and token_data to None in the database
    await UserModel.find_one(UserModel.email == current_user.email).set({
        UserModel.token: None,
        UserModel.token_data: None
    })

    # Clear authentication cookies
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token", path="/api/v1/auth/refresh-token")
    return {"message": "Logged out successfully"}

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest):
    """Request a password reset token via email"""
    # Generate reset token
    token = await auth_services.generate_password_reset_token(request.email)
    
    # In development mode, we return the token for testing
    if core_settings.DEBUG:
        reset_link = f"{core_settings.API_FULL_URL}/reset-password?token={token}"
        await email_services.send_password_reset(request.email, token)
        return {
            "message": "If this email is registered, a password reset link has been sent.",
            "debug": {
                "reset_token": token,
                "reset_link": reset_link
            }
        }
    
    
    # In production, we would send an email with the token
    # TODO: Implement email sending functionality
    # example: await email_service.send_password_reset(request.email, token)
    # await email_services.send_password_reset(request.email, token)
    
    # Always return the same response regardless of whether the email exists
    # This prevents email enumeration attacks
    return {"message": "If this email is registered, a password reset link has been sent to your inbox."}

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest):
    """Reset password using token"""
    try:
        # Validate new password
        # from auth_fastapi_beanie_poetry.schemas.user import validate_password
        # validate_password(request.new_password)
        
        # Reset password
        success = await auth_services.reset_password_with_token(
            token=request.token,
            new_password=request.new_password
        )
        
        if success:
            return {"message": "Password has been reset successfully. You can now log in with your new password."}
            
    except ValueError as e:
        # Password validation error
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        # Log unexpected errors but don't expose details
        print(f"Error in reset_password: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while resetting password")
        
    raise HTTPException(status_code=400, detail="Unable to reset password")

@router.get("/")
async def root():
    return {"message": "Auth API is running"}

