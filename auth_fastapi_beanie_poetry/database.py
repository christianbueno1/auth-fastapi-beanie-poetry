import os
from dotenv import load_dotenv
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()
DB_URL = os.getenv("DB_URL")

async def init_db():
    client = AsyncIOMotorClient(DB_URL, uuidRepresentation="standard")
    await init_beanie(database=client.



