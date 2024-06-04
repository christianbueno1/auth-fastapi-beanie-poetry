from beanie import PydanticObjectId
from auth_fastapi_beanie_poetry.models.user import User

async def get_user(username: str) -> User | None:
    # user = await User.find_one({"username": username})
    user = await User.find_one(User.username == username)
    return user