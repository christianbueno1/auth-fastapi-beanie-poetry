from contextlib import asynccontextmanager
from os import getenv
from dotenv import load_dotenv
from fastapi import FastAPI
from beanie import init_beanie
from models.user import User
import motor.motor_asyncio

load_dotenv()

mongo_url = getenv("MONGO_URL")

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
    await init_beanie(database=client.mydatabase, document_models=[User])
    yield

app = FastAPI(lifespan=lifespan)