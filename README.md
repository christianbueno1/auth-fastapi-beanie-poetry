## Steps
```
# on f40 Linux install poetry
sudo dnf install poetry

# clone the repo
# create the db or run the container db
poetry install
# run
poetry run <command>
poetry run python YOUR_SCRIPT_NAME.py

poetry add uvicorn -G dev

# add in toml
#[tool.poetry.scripts]
#start = "auth_fastapi_beanie_poetry.main:start"
#poetry run start

# use underscore
poetry run uvicorn auth_fastapi_beanie_poetry.main:app --reload

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

## packages
```
pip install python-dotenv
# from dotenv import load_dotenv
# import os

load_dotenv
DB_URL = os.getenv(DB_URL)

```

## Envairoment variable file example

```
# Envaironment variables for the project
# in production remove this file and set the variables in the server

DB_URL=mongodb://chris:maGazine1!@127.0.0.1:27017
DB_NAME=registerdb

SECRET_KEY = "83daa0256a2289b0fb23693bf1f6034d44396675749244721a2b20e896e11662"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS=1
FRONTEND_URL = "http://localhost:5173"
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


```

## Database
```
# create the container db
podman pull mongo:
```

## Token
- The default lifetime for the refresh tokens is 24 hours for single page apps and 90 days for all other scenarios.
- The access token in JWT usually expires in 10-60 minutes, this is configured in the backend side. 
- Refresh tokens should be valid for at least 7 days (ideally 90-365 days). 
- Authentication is implemented through JWT access tokens along with refresh tokens. The API returns a short-lived token (JWT), which expires in 15 minutes, and in HTTP cookies, the refresh token expires in 7 days.
- With this setup, the JWT's expiration duration is set to something short (5-10 minutes) and the refresh token is set to something long (2 weeks or 2 months), link2.
- [link1, refresh-tokens-jwt-interaction](https://www.loginradius.com/blog/identity/refresh-tokens-jwt-interaction/)
- [link2, revoking-jwts](https://fusionauth.io/articles/tokens/revoking-jwts)