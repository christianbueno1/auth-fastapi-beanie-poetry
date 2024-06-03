import os
from dotenv import load_dotenv
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from auth_fastapi_beanie_poetry.models.user import User

load_dotenv()
DB_URL = os.getenv("DB_URL")

async def init_db():
    client = AsyncIOMotorClient(DB_URL, uuidRepresentation="standard")
    await init_beanie(database=client.registerdb, document_models=[User])



