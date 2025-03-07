## User Authentication Service API
You have a user authentication services API using Python, JWT, FastAPI, Beanie ODM, MongoDB, to allow user to Register/sign-up, Login/sign-in, Logout, and access a protected user profile API.

- Authentication services, MongoDB avoid duplicate entries.

## Steps
```
# on f40 Linux install poetry
sudo dnf install poetry
#
# clone the repo
gh repo clone christuianbueno/auth-fastapi-beanie-poetry


# create the db or run the container db
# install dependencies of pydantic-core: rust cargo, to compile from source
sudo dnf install cargo rust
# alternative, install the binary from the repo
poetry add pydantic-core
#
# set up the project
poetry install
#
# create .env file
#
# run
poetry run <command>
poetry run python YOUR_SCRIPT_NAME.py
# 
# run a python file
poetry run python tests/functiontest.py

poetry add uvicorn -G dev

# add in toml
#[tool.poetry.scripts]
#start = "auth_fastapi_beanie_poetry.main:start"
#poetry run start


# run the app and use the .env.dev file
# use underscore
poetry run uvicorn auth_fastapi_beanie_poetry.main:app --reload --env-file .env.dev

# create admin user
# install the script
poetry install
#
poetry run create-admin
#  chris123 chris@ibm.com chris123


# or
poetry shell
uvicorn auth_fastapi_beanie_poetry.main:app --reload


# uvicorn command
uvicorn auth_fastapi_beanie_poetry.main:app --reload

# generate secret key
openssl rand -hex 32


```

## Prompt
- Give me an example of structure of files in a python backend web application or REST API, following the best conventions in architecture in microservices, low coupling, high cohesion, SOLID

## Notes
```
# new 3.10
# multiple, or
username: str | None = None

# typing
username: Optional[str] = None

# e.g.2
def foo(client_id: str) -> list | bool:
from typing import Union
def foo(client_id: str) -> Union[list, bool]:
#
Optional[...] is a shorthand notation for Union[..., None]

# dictionary
user = {
    "id": 12,
    "name": 'john',
    "dob": '1998-01-14'
}
```
- Use the email with OAuth2PasswordRequestForm` instead of username.
- json.dumps in jwt.encode, TokenPayload
- the key value in data dict must be 'exp' for use in jwt.encode [https://github.com/jpadilla/pyjwt/issues/853](https://github.com/jpadilla/pyjwt/issues/853)

## packages
```
pip install python-dotenv
# from dotenv import load_dotenv
# import os

load_dotenv
DB_URL = os.getenv(DB_URL)

```

## Environment variable file example

```
# Environment variables for the project
# in production remove this file and set the variables in the server
touch .env
vim .env
# Application settings
APP_NAME="Your App Name"
APP_VERSION="0.0.1"
DEBUG=true
ENVIRONMENT=development

# MongoDB settings
MONGODB_URL="mongodb://username:password@localhost:27017/auth_db?authSource=auth_db"
MONGODB_NAME=auth_db

# JWT settings
JWT_SECRET="your_jwt_secret_key"
JWT_ALGORITHM="HS256"
# access token expire in 60 minutes
ACCESS_TOKEN_EXPIRE_MINUTES=2
# refresh token expire in 30 days 
REFRESH_TOKEN_EXPIRE_DAYS=1

# Security
ALLOWED_ORIGINS=["https://yourfrontend.com","http://localhost:5173"]



# use separate .env files for different environments
# .env.dev, .env.prod, .env.test
# run on dev
poetry run uvicorn auth_fastapi_beanie_poetry.main:app --reload --env-file .env.dev
# run on prod
poetry run uvicorn auth_fastapi_beanie_poetry.main:app --env-file .env.prod

```

## Poetry
```
# create a default dir
poetry new sample-project

# virtual env
poetry shell

 
# add flask
poetry add flask
poetry add beanie

# dev dep, deprecated, use -G dev
poetry add --dev pytest

# remove
poetry remove pytest -G dev

# general config
poetry config --list

# list all virt env
poetry env list
poetry env list --full-path

poetry env info
poetry env use system
poetry env use python3.7
poetry env use 3.7
poetry env info --path

poetry env remove /full/path/to/python
poetry env remove python3.7
poetry env remove 3.7
poetry env remove test-O3eWbxRl-py3.7


# decativate
deactivate

# In a Python Poetry project, you can open a Python shell with all installed dependencies by running:
# If you just need a one-time test → Use poetry run python
poetry run python
# If you want a persistent shell with Poetry's virtual environment → Use poetry shell first
poetry shell
python

# test
import bcrypt
dir(bcrypt)
bcrypt.__version__


# lock file
# 3️⃣ Remove and regenerate poetry.lock
rm poetry.lock
poetry lock
# 1️⃣ Ignore poetry.lock when installing dependencies
poetry install --no-root --no-lock
# 🚀 Alternative: Ignore poetry.lock Temporarily
poetry install --no-lock



```

## Database
- database name: registerdb
- Use plural for collections, e.g. users, todos, posts
```
# create the container db
# pull the image
podman pull docker.io/mongodb/mongodb-community-server:latest
podman pull docker.io/mongodb/mongodb-community-server:7.0.16-ubuntu2204
podman pull docker.io/mongodb/mongodb-community-server:7.0.16-ubi9

# update the image
podman pull docker.io/mongodb/mongodb-community-server:latest

#
podman run -d --name auth -e MONGO_INITDB_ROOT_USERNAME=chris -e MONGO_INITDB_ROOT_PASSWORD='maGazine1!devE' -p 27017:27017 mongodb-community-server:7.0.16-ubi9

# install GUI from flathub
flatpak install flathub com.mongodb.Compass
# run
flatpak run com.mongodb.Compass

# use cli client
podman exec -it auth bash
mongosh -u chris -p maGazine1!
show dbs
use registerdb
#
db.createUser
db.createCollection("users")
db.users.insertOne({username: "chris", email: "chris@ibm.com", password: "password"})
db.users.find()
#
# show collections, tables
show collections
# show all documents on User collection
db.users.find()
# db.collection.find( <query>, <projection>, <options> )
#
# delete collection Users
# take care of case sensitivity
db.users.drop()
db.User.drop()
# delete database
db.dropDatabase()
#
# projection
# db.collection.find({}, {field1: 1, field2: 1})
# db.collection.find({}, {field1: 0, field2: 0})
db.users.find({}, {email: 1, username: 1})
#
# query
# Equality Condition
# {email: "chris@ibm.com"}
db.users.find({email: "chris@ibm.com"})
#
db.users.find({created_at: {$gte: ISODate('2025-02-20')}}, {email: 1, created_at: 1})
#
db.users.find({created_at: {$gte: ISODate('2025-02-20'), $lt: ISODate('2025-03-01')}}, {email: 1, created_at: 1})

# mongodb version
db.version()

```

## Test, Http file
- ctrl + , to open settings
- search: rest client: show
- show response in different tab
### Interactive docs
http://127.0.0.1:8000/docs

## Token
- The default lifetime for the refresh tokens is 24 hours for single page apps and 90 days for all other scenarios.
- The access token in JWT usually expires in 10-60 minutes, this is configured in the backend side. 
- Refresh tokens should be valid for at least 7 days (ideally 90-365 days). 
- Authentication is implemented through JWT access tokens along with refresh tokens. The API returns a short-lived token (JWT), which expires in 15 minutes, and in HTTP cookies, the refresh token expires in 7 days.
- With this setup, the JWT's expiration duration is set to something short (5-10 minutes) and the refresh token is set to something long (2 weeks or 2 months), link2.
- [link1, refresh-tokens-jwt-interaction](https://www.loginradius.com/blog/identity/refresh-tokens-jwt-interaction/)
- [link2, revoking-jwts](https://fusionauth.io/articles/tokens/revoking-jwts)

## Regex pattern
```bash
echo "123123123" | grep -E '^[a-zA-Z0-9_]{8,20}$'

```

### **Standard Password Validation Rules**
A strong and commonly accepted password validation standard includes the following rules:  

1️⃣ **Minimum Length**: At least **8 characters** long (some systems require 12+).  
2️⃣ **Uppercase Letter**: At least **one uppercase letter** (`A-Z`).  
3️⃣ **Lowercase Letter**: At least **one lowercase letter** (`a-z`).  
4️⃣ **Digit**: At least **one numeric digit** (`0-9`).  
5️⃣ **Special Character**: At least **one special character** (e.g., `!@#$%^&*`).  
6️⃣ **No Spaces**: Password **must not contain spaces**.  

Would you like to add any additional requirements, such as **prohibiting consecutive characters** or **restricting certain words**?

```bash
# regex
# Lookahead (?=.*[A-Z])
# positive lookahead (?=.*[a-z])
# negative lookahead (?!.*[!@#$%^&*])
# Lookbehind (?<=\d)
# positive lookbehind (?<=\d)
# negative lookbehind (?<!\d)
# you can use word before or after: word (..) word
# word boundary \b
echo 'hello1!A' | grep -P '^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$!%^*?&])[A-Za-z\d@$!%*?&]{8,}$'
echo 'hello1!A' | grep -P '^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W])[A-Za-z\d\W]{8,}$'
```