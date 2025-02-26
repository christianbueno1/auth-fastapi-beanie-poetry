from contextlib import asynccontextmanager
from fastapi import FastAPI
from auth_fastapi_beanie_poetry.db.mongo import init_db
from auth_fastapi_beanie_poetry.api.v1.endpoints.auth import router as auth_router
from auth_fastapi_beanie_poetry.core.config import core_settings

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

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
# app.include_router(todo.router, prefix="/todos", tags=["todos"])
