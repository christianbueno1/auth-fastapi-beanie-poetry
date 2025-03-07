from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from auth_fastapi_beanie_poetry.models.user import User
from auth_fastapi_beanie_poetry.core.config import core_settings


async def init_db():
    client = AsyncIOMotorClient(core_settings.MONGODB_URL, uuidRepresentation="standard")
    print(f"MongoDB URL: {core_settings.MONGODB_URL}")
    print(f"MongoDB Name: {core_settings.MONGODB_NAME}")
    database= client[core_settings.MONGODB_NAME]
    await init_beanie(database=database, document_models=[User])


# async def close_db():
#     client = AsyncIOMotorClient(DB_URL, uuidRepresentation="standard")
#     client.close()

# async def get_db():
#     client = AsyncIOMotorClient(DB_URL, uuidRepresentation="standard")
#     return client.registerdb
