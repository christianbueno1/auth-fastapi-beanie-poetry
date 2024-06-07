from auth_fastapi_beanie_poetry.models.user import User

async def get_user(username: str) -> User | None:
    # user = await User.find_one({"username": username})
    user = await User.find_one(User.username == username)
    user_in_db = User(**user.model_dump())
    return user_in_db

async def get_user_by_email(email: str) -> User | None:
    user = await User.find_one(User.email == email)
    user_in_db = User(**user.model_dump())
    return user_in_db



