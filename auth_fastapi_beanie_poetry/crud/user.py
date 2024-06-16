from auth_fastapi_beanie_poetry.models.user import User as UserModel
from auth_fastapi_beanie_poetry.schemas.user import UserInDB

async def get_user(username: str) -> UserInDB | None:
    # user = await User.find_one({"username": username})
    try:
        user: UserModel = await UserModel.find_one(UserModel.username == username)
        if user:
            user_in_db = UserInDB(**user.model_dump())
            return user_in_db
    except AttributeError:
        print("User not found")
        return None

async def get_user_by_email(email: str) -> UserInDB | None:
    try:
        user: UserModel = await UserModel.find_one(UserModel.email == email)
        if user:
            user_in_db = UserInDB(**user.model_dump())
            return user_in_db
    except AttributeError:
        print("User not found")
        return None


