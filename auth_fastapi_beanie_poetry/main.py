from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth_fastapi_beanie_poetry.db.mongo import init_db
from auth_fastapi_beanie_poetry.api.v1.endpoints.auth import router as auth_router
from auth_fastapi_beanie_poetry.core.config import core_settings
import json

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(f"Starting up with settings:")
    print(f"Token expiration minutes: {core_settings.ACCESS_TOKEN_EXPIRE_MINUTES}")
    await init_db()

    # Create admin if doesn't exist
    # admin_exists = await User.find_one(User.email == core_settings.FIRST_ADMIN_EMAIL)
    # if not admin_exists:
    #     admin = User(
    #         username=core_settings.FIRST_ADMIN_USERNAME,
    #         email=core_settings.FIRST_ADMIN_EMAIL,
    #         hashed_password=get_password_hash(core_settings.FIRST_ADMIN_PASSWORD),
    #         role=Role.ADMIN,
    #         disabled=False
    #     )
    #     await admin.insert()
    #     print("Admin user created from environment variables")

    
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

# Parse allowed origins from environment (handles both string and JSON array formats)
allowed_origins = core_settings.ALLOWED_ORIGINS
if isinstance(allowed_origins, str):
    try:
        # Try to parse as JSON
        origins = json.loads(allowed_origins)
    except json.JSONDecodeError:
        # If not valid JSON, treat as comma-separated string
        origins = [origin.strip() for origin in allowed_origins.split(",")]
else:
    origins = allowed_origins

print(f"Allowed origins: {origins}")
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "Accept", "X-Requested-With"],
    max_age=600,  # Cache preflight results for 10 minutes
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
# app.include_router(todo.router, prefix="/todos", tags=["todos"])