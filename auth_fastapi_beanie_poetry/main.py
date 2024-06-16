from contextlib import asynccontextmanager
from fastapi import FastAPI
from auth_fastapi_beanie_poetry.db.mongo import init_db
from auth_fastapi_beanie_poetry.api.v1.endpoints.auth import router as auth_router

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

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])