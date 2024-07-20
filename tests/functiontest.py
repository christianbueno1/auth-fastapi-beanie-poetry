from datetime import datetime, timedelta, timezone
from enum import Enum
from beanie import Document, init_beanie
from passlib.context import CryptContext
import jwt
from pydantic import BaseModel #pyjwt
from auth_fastapi_beanie_poetry.core.config import core_settings
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from auth_fastapi_beanie_poetry.models.token import TokenMode, TokenPayload
from auth_fastapi_beanie_poetry.models.user import User
from auth_fastapi_beanie_poetry.schemas.user import UserCreate
from beanie.exceptions import DocumentNotFound

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
    if user:
        print(f"User: {user} Type: {type(user)}")
        print("Searching for user")

        # delete
        await user.delete()
        print("User deleted")
    else:
        print(f"User doesn't exists")
    
    # update
    user = await User.find_one(User.email == "pam@foo.xyz")
    if user:
        user.email = 'bob@bar.xyz'
        await user.save()
        print('user updated successfully')
    else:
        hashed_password = pwd_context.hash('123pam')
        new_user = User(username='Pam', email='pam@foo.xyz', hashed_password=hashed_password)
        await new_user.save()
        print('New user created successfully')
    
    user = await User.find_one(User.email == "bob@foo.xyz")
    if user:
        user.email = 'bob@bar.xyz'
        try:
            await user.replace()
        except ValueError:
            print("The document does not have an id yet.")
        except DocumentNotFound:
            print("The document with the given id does not exist in the collection")

    
    await User.find_one(User.email == "jerry@foo.xyz").set({User.email: "iamjerry@foo.xyz"})

def spread_operator():
    numbers = [1,2,3]
    fruits = ['apple','banana','grape']
    more_fruits = ['kiwi','coconut','cherry','peach']
    combined_fruits = [*fruits, *more_fruits]
    data1 = {
        'name': "christian",
        'email': "chris@ibm.com"
    }
    data2 = {
        "token": "123",
        "token_type": "bearer"
    }
    # print(f"{numbers}\n{*numbers}")
    print(f"numbers: {numbers}")
    print(*numbers)
    print(f"combined_fruits: {combined_fruits}")
    print({**data1, **data2})
    fruit1, *rest_fruit = more_fruits
    print(f"fruit1: {fruit1} and rest_fruit: {rest_fruit}")
    starred1 = fruits, *more_fruits
    print(f"starred1: {starred1}, type {type(starred1)}")
    *st2, st3 = fruits, *more_fruits
    print(f"st2: {st2} type: {type(st2)}\nst3: {st3}")
    # print(f"st2: {st2}")

def test2_enum():
    class Role(str, Enum):
        ADMIN = "admin"
        USER = "user"
        GUEST = "guest"

    print(f"ADMIN: {Role.ADMIN}, value: {Role.ADMIN.value}")
    print(f"USER: {Role.USER}")
    print(f"GUEST: {Role.GUEST}")
    # user_role = Role.USER
    # user_role = Role.GUEST
    user_role = Role.ADMIN
    if user_role == Role.USER:
        print(f"user_role: {user_role}")
    elif user_role == Role.ADMIN:
        print(f"user_role: {user_role}")
    elif user_role == Role.GUEST:
        print(f"user_role: {user_role}")
        
def test3_dict():
    data = {
        'name': "christian",
        'email': "chris@ibm.com"
    }
    print(f"data: {data}")
    print(f"data['name']: {data['name']}, datatype: {type(data['name'])}")
    print(f"data['email']: {data['email']}, datatype: {type(data['email'])}")
    today = datetime.now(timezone.utc)
    print(f"today: {today}")
    # add one minute
    tomorrow = today + timedelta(minutes=1)
    # use exp
    data.update({"token": "123", "token_type": "bearer", "exp": tomorrow})
    data.update({"custom_date": tomorrow.strftime("%Y-%m-%dT%H:%M:%SZ")})
    print(f"data: {data}")
    print(f"data['exp']: {data['exp']}, datatype: {type(data['exp'])}")
    print(f"data['token']: {data['token']}, datatype: {type(data['token'])}")
    print(f"data['token_type']: {data['token_type']}, datatype: {type(data['token_type'])}")
    encoded_jwt: str = jwt.encode(data, core_settings.SECRET_KEY, algorithm=core_settings.ALGORITHM)
    print(f"encoded_jwt: {encoded_jwt}, datatype: {type(encoded_jwt)}")

    dog = TokenPayload(sub="123", exp=tomorrow, mode=TokenMode.access_token)

if __name__ == "__main__":
    # test1()
    # asyncio.run(init_db())
    # print("Database initialized")
    # spread_operator()
    # test2_enum()
    test3_dict()
    