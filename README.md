## Links

## Prompt
- Give me an example of structure of files in a python backend web application or REST API, following the best conventions in architecture in microservices, low coupling, high cohesion, SOLID

## Notes
```
# new 3.10
username: str | None = None
# old
username: Optional[str] = None
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

# dev dep
poetry add --dev pytest

```