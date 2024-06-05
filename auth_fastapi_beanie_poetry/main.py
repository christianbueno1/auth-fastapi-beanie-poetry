from contextlib import asynccontextmanager
# from os import getenv
# from dotenv import load_dotenv
from fastapi import FastAPI
from auth_fastapi_beanie_poetry.db.mongo import init_db

# load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)


# @app.on_event("startup")
# async def start_db():
#     await init_db()

# from fastapi import FastAPI
# from app.routes import auth, todo

# app = FastAPI()

# app.include_router(auth.router, prefix="/auth", tags=["auth"])
# app.include_router(todo.router, prefix="/todos", tags=["todos"])

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Todo App"}