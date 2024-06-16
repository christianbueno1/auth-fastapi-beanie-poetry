from beanie import init_beanie
from passlib.context import CryptContext
import jwt #pyjwt
from auth_fastapi_beanie_poetry.core.config import core_settings
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from auth_fastapi_beanie_poetry.models.user import User
from auth_fastapi_beanie_poetry.schemas.user import UserCreate

# Define the payload
def test1():
    to_encode = {"some": "payload"}

    # Define the secret key and algorithm
    SECRET_KEY = "my_secret_key"
    ALGORITHM = "HS256"

    # Encode the payload
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # The result is a byte string
    print(encoded_jwt, f"Type: {type(encoded_jwt)}")
    print(f"{encoded_jwt.upper()}")
    print(f"{encoded_jwt.capitalize()}")
    print(f"{encoded_jwt.split(".")}")
    print(f"encoded: {encoded_jwt.encode()}, Type: {type(encoded_jwt.encode())}")

    # Decode the byte string into a regular string
    # decoded_jwt = encoded_jwt.decode('UTF-8')
    decoded_jwt = jwt.decode(encoded_jwt, SECRET_KEY, algorithms=[ALGORITHM])

    print(decoded_jwt)


async def init_db():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")
    client = AsyncIOMotorClient(core_settings.DATABASE_URL, uuidRepresentation="standard")
    database= client[core_settings.DATABASE_NAME]
    await init_beanie(database=database, document_models=[User])
    
    # create a User object
    # user: UserCreate = UserCreate(username="tom", email="tom@ibm.com", password="password")
    # print(f"User: {user}")
    # hashed_password = pwd_context.hash(user.password)
    # user_in_db = User(username=user.username, email=user.email, hashed_password=hashed_password)
    # await user_in_db.insert()
    
    # find the user
    # user = await User.find_one(User.username == "tom")
    user = await User.get("66665ed8eec9d71c757d57d8")
    print(f"User: {user} Type: {type(user)}")
    print("Searching for user")

    # delete
    await user.delete()
    print("User deleted")


if __name__ == "__main__":
    # test1()
    asyncio.run(init_db())
    print("Database initialized")
    