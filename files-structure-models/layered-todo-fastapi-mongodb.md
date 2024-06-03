### Layered or Horizontal Structure of Files in a Python FastAPI MongoDB Web Application

A layered or horizontal file structure in a FastAPI application helps organize code into logical layers, each responsible for a specific aspect of the application's functionality. This approach promotes separation of concerns, making the codebase more maintainable and scalable.

#### Common Layers in a FastAPI Application

1. **Presentation Layer**: Handles incoming HTTP requests and outgoing HTTP responses.
2. **Application Layer**: Contains the application logic, orchestrating the use of domain entities.
3. **Domain Layer**: Encapsulates the core business logic and rules.
4. **Infrastructure Layer**: Manages external systems such as databases, email services, etc.

#### Example File Structure

Here is an example of a file structure for a FastAPI application using MongoDB:

```
/my_fastapi_app
│
├── /app
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── /api
│   │   ├── __init__.py
│   │   └── v1
│   │       ├── __init__.py
│   │       └── endpoints
│   │           ├── __init__.py
│   │           ├── auth.py
│   │           └── todos.py
│   ├── /core
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   └── utils.py
│   ├── /models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── todo.py
│   ├── /schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── todo.py
│   ├── /services
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── todo_service.py
│   ├── /db
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── session.py
│   │   └── mongo.py
│   └── /tests
│       ├── __init__.py
│       ├── test_auth.py
│       └── test_todos.py
│
├── .env
├── pyproject.toml
├── README.md
└── requirements.txt
```

#### Explanation of Directories and Files

- **/app**: The main application directory.
  - **__init__.py**: Marks the directory as a Python package.
  - **main.py**: Entry point for the application.
  - **config.py**: Configuration settings.
  
- **/api**: Contains the API routes and endpoints.
  - **v1**: Version 1 of the API.
  - **endpoints**: Specific routes such as `auth.py` for authentication and `todos.py` for managing todos.

- **/core**: Contains core functionalities and utilities.
  - **config.py**: Configuration settings for the application.
  - **security.py**: Security utilities (e.g., JWT token handling).
  - **utils.py**: Helper functions.

- **/models**: Database models representing entities.
  - **user.py**: User model.
  - **todo.py**: Todo model.

- **/schemas**: Pydantic models for data validation and serialization.
  - **user.py**: User schema.
  - **todo.py**: Todo schema.

- **/services**: Business logic and services.
  - **auth_service.py**: Authentication services.
  - **todo_service.py**: Todo services.

- **/db**: Database-related code.
  - **base.py**: Base classes for database models.
  - **session.py**: Database session management.
  - **mongo.py**: MongoDB connection setup.

- **/tests**: Unit and integration tests.
  - **test_auth.py**: Tests for authentication.
  - **test_todos.py**: Tests for todo functionalities.

#### Advantages of This Structure

1. **Separation of Concerns**: Each layer has a distinct responsibility, making the codebase easier to understand and maintain.
2. **Scalability**: Adding new features or modifying existing ones becomes more manageable.
3. **Reusability**: Components can be reused across different parts of the application.
4. **Testability**: The clear separation makes it easier to write unit and integration tests.

### Tips for Implementing JWT Authentication with FastAPI and MongoDB

1. **Install Dependencies**:
   ```bash
   pip install fastapi[all] beanie pymongo pydantic[dotenv] python-jose
   ```

2. **Set Up MongoDB Connection**:
   ```python
   # app/db/mongo.py
   from beanie import init_beanie
   from motor.motor_asyncio import AsyncIOMotorClient
   from app.models.user import User
   from app.models.todo import Todo

   async def init_db():
       client = AsyncIOMotorClient("mongodb://localhost:27017")
       await init_beanie(database=client.db_name, document_models=[User, Todo])
   ```

3. **Define Models and Schemas**:
   ```python
   # app/models/user.py
   from beanie import Document
   from pydantic import BaseModel
   from datetime import datetime

   class User(Document):
       username: str
       email: str
       hashed_password: str
       created_at: datetime

       class Settings:
           collection = "users"

   # app/schemas/user.py
   from pydantic import BaseModel

   class UserCreate(BaseModel):
       username: str
       email: str
       password: str
   ```

4. **Implement Authentication Logic**:
   ```python
   # app/core/security.py
   from datetime import datetime, timedelta
   from jose import JWTError, jwt

   SECRET_KEY = "your_secret_key"
   ALGORITHM = "HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES = 30

   def create_access_token(data: dict):
       to_encode = data.copy()
       expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
       to_encode.update({"exp": expire})
       encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
       return encoded_jwt
   ```

5. **Create Authentication Endpoints**:
   ```python
   # app/api/v1/endpoints/auth.py
   from fastapi import APIRouter, Depends, HTTPException
   from app.schemas.user import UserCreate
   from app.services.auth_service import create_user, authenticate_user

   router = APIRouter()

   @router.post("/signup")
   async def signup(user: UserCreate):
       user = await create_user(user)
       return {"message": "User created"}

   @router.post("/login")
   async def login(form_data: OAuth2PasswordRequestForm = Depends()):
       user = await authenticate_user(form_data.username, form_data.password)
       if not user:
           raise HTTPException(status_code=400, detail="Invalid credentials")
       access_token = create_access_token(data={"sub": user.username})
       return {"access_token": access_token, "token_type": "bearer"}
   ```

By following this structure and these tips, you can build a robust, maintainable, and scalable FastAPI application with MongoDB as the backend.