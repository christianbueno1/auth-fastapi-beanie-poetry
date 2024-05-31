Creating a REST API for authentication using JWT and refresh tokens in FastAPI with MongoDB as the database and Beanie as the ODM involves several steps. Here's an outline of the process along with some advice and best practices.

### Prerequisites
1. **Python**: Ensure you have Python installed.
2. **Poetry**: Install Poetry for dependency management.
3. **MongoDB**: Have a running instance of MongoDB.
4. **FastAPI**: You should be familiar with FastAPI.
5. **Beanie**: Knowledge of using Beanie with MongoDB.

### Project Setup
1. **Initialize a new Poetry project**:
    ```bash
    poetry new my_auth_api
    cd my_auth_api
    poetry add fastapi uvicorn beanie motor pymongo pydantic[dotenv] python-jose passlib
    ```

2. **Project Structure**:
    ```
    my_auth_api/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── config.py
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── user.py
    │   ├── routes/
    │   │   ├── __init__.py
    │   │   ├── auth.py
    │   ├── services/
    │   │   ├── __init__.py
    │   │   ├── auth.py
    │   ├── utils/
    │       ├── __init__.py
    │       ├── security.py
    │       ├── token.py
    ├── tests/
    ├── pyproject.toml
    └── README.md
    ```

### Configuration
**app/config.py**:
```python
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'mongodb://localhost:27017')
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'your-secret-key')
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 1440

settings = Settings()
```

### Models
**app/models/user.py**:
```python
from beanie import Document
from pydantic import BaseModel

class User(Document):
    username: str
    email: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False

    class Settings:
        collection = "users"

class UserIn(BaseModel):
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    username: str
    email: str
    is_active: bool

class UserInDB(UserOut):
    hashed_password: str
```

### Utility Functions
**app/utils/security.py**:
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
```

**app/utils/token.py**:
```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.config import settings

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
```

### Services
**app/services/auth.py**:
```python
from app.models.user import User, UserIn, UserInDB
from app.utils.security.py import verify_password, get_password_hash
from app.utils.token import create_access_token, create_refresh_token
from fastapi import HTTPException, status

class AuthService:
    @staticmethod
    async def authenticate_user(username: str, password: str):
        user = await User.find_one(User.username == username)
        if not user or not verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    async def create_user(user_in: UserIn):
        user = await User.find_one(User.email == user_in.email)
        if user:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = get_password_hash(user_in.password)
        user = User(username=user_in.username, email=user_in.email, hashed_password=hashed_password)
        await user.insert()
        return user

    @staticmethod
    def create_tokens(user: User):
        access_token = create_access_token(data={"sub": user.username})
        refresh_token = create_refresh_token(data={"sub": user.username})
        return access_token, refresh_token
```

### Routes
**app/routes/auth.py**:
```python
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import UserIn, UserOut
from app.services.auth import AuthService
from app.utils.token import verify_token

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(user_in: UserIn):
    user = await AuthService.create_user(user_in)
    return user

@router.post("/login")
async def login(username: str, password: str):
    user = await AuthService.authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token, refresh_token = AuthService.create_tokens(user)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh")
async def refresh_token(token: str):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    username = payload.get("sub")
    user = await AuthService.authenticate_user(username, "")
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token, refresh_token = AuthService.create_tokens(user)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
```

### Main Application
**app/main.py**:
```python
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.user import User
from app.routes import auth
from app.config import settings

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    await init_beanie(database=client.get_default_database(), document_models=[User])

app.include_router(auth.router, prefix="/auth", tags=["auth"])
```

### Running the Application
1. **Set Environment Variables**:
   Create a `.env` file with your environment variables.
   ```dotenv
   DATABASE_URL=mongodb://localhost:27017
   SECRET_KEY=your-secret-key
   ```

2. **Run the Application**:
   ```bash
   uvicorn app.main:app --reload
   ```

### Testing
You can use tools like **Postman** or **httpie** to test your API endpoints.

### Summary
- **Low Coupling**: Each component (models, services, routes, utils) is modular and independent.
- **High Cohesion**: Related functionality is grouped together, making the code easier to maintain.
- **SOLID Principles**: The structure adheres to SOLID principles, ensuring a clean, maintainable, and scalable design.
- **JWT for Authentication**: Secure your API with JWT and refresh tokens for session management.

By following these steps, you'll create a robust authentication system for your FastAPI project using MongoDB and Beanie ODM, all managed with Poetry.