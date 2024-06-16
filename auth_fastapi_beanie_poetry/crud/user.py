from auth_fastapi_beanie_poetry.models.user import User as UserModel

async def get_user(username: str) -> UserModel | None:
    # user = await User.find_one({"username": username})
    try:
        user: UserModel = await UserModel.find_one(UserModel.username == username)
        # user_in_db = UserModel(**user.model_dump())
        # return user_in_db
        return user
    except AttributeError:
        print("User not found")
        return None

async def get_user_by_email(email: str) -> UserModel | None:
    user: UserModel = await UserModel.find_one(UserModel.email == email)
    # user_in_db = UserModel(**user.model_dump())
    # return user_in_db
    return user



