from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from auth_fastapi_beanie_poetry.models.user import User
from auth_fastapi_beanie_poetry.models.reset_token import ResetToken
from auth_fastapi_beanie_poetry.core.config import core_settings


async def init_db():
    try:
        client = AsyncIOMotorClient(core_settings.MONGODB_URL, uuidRepresentation="standard")
        # print(f"MongoDB URL: {core_settings.MONGODB_URL}")
        # print(f"MongoDB Name: {core_settings.MONGODB_NAME}")
        database= client[core_settings.MONGODB_NAME]
        
        # Initialize Beanie with all document models
        await init_beanie(database=database, document_models=[User, ResetToken])
        print("Database initialized successfully")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise e

# async def close_db():
#     client = AsyncIOMotorClient(DB_URL, uuidRepresentation="standard")
#     client.close()

# async def get_db():
#     client = AsyncIOMotorClient(DB_URL, uuidRepresentation="standard")
#     return client.registerdb
