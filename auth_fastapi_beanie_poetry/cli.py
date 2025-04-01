import typer
import asyncio

import uvicorn
from auth_fastapi_beanie_poetry.models.user import Role
from auth_fastapi_beanie_poetry.schemas.user import UserCreate, UserInDB
from auth_fastapi_beanie_poetry.db.mongo import init_db
from auth_fastapi_beanie_poetry.services.auth_services import create_user
from fastapi import HTTPException
from auth_fastapi_beanie_poetry.core.config import core_settings

cli = typer.Typer()

@cli.command()
def create_admin(
    username: str = typer.Option(..., prompt=True),
    email: str = typer.Option(..., prompt=True),
    password: str = typer.Option(..., prompt=True, hide_input=True),
):
    """Create initial admin user"""
    password_requirements = """
    Password must comply with the following rules:
    - At least 8 characters long
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character (!@#$%^&*)
    """
    print(password_requirements)

    async def _create_admin():
        await init_db()
        try:
            user_create = UserCreate(
                username=username,
                email=email,
                password=password,
                role=Role.ADMIN,
                disabled=False
            )
            user_indb: UserInDB = await create_user(user_create)
            if not user_indb:
                print(f"Error creating admin user {email}")
                return
            print(f"Admin user {email} created successfully")
        except HTTPException as e:
            print(f"HTTPException: {e.detail}")
        except Exception as e:
            print(f"Error: {e}")

    try:
        asyncio.run(_create_admin())
    except Exception as e:
        print(f"Failed to create admin user: {e}")

def dev():
    uvicorn.run("auth_fastapi_beanie_poetry.main:app", reload=True, env_file=".env", port=core_settings.FASTAPI_PORT, host="127.0.0.1")

if __name__ == "__main__":
    cli()