#!/bin/bash
# Direct request to the FastAPI container inside the pod

### install
# Step 1: Install curl in the container
podman exec -it authapi-fastapi apt-get update
podman exec -it authapi-fastapi apt-get install -y curl

# Method 1: Use podman exec to make request from inside the container
echo "Method 1: Using podman exec to make request from inside container"
podman exec -it authapi-fastapi curl -v -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=christianbueno.1@gmail.com&password=maGazine1\!"

podman exec -it authapi-fastapi curl -v -X POST http://localhost:8000/api/v1/auth/signup \
    -H "Content-Type: application/json" \
    -d '{
    "username": "bruce1234",
    "email": "bruce123@ibm.com",
    "password": "hello1!A",
    "disabled": false,
    "role": "user"
}'

podman exec -it authapi-fastapi curl -v -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=bruce123@ibm.com&password=hello1\!A"

# register a new user, only admin can do this
podman exec -it authapi-fastapi curl http://localhost:8000/api/v1/auth/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "username": "tim123",
    "email": "tim@foo.xyz",
    "password": "magazine1!",
    "disabled": false,
    "role": "user"
}'


podman exec -it authapi-fastapi curl -X POST http://localhost:8000/api/v1/auth/refresh-token \
  -H "Authorization: Bearer $ACCESS"

podman exec -it authapi-fastapi curl -X GET http://localhost:8000/api/v1/auth/users/me \
  -H "Authorization: Bearer $ACCESS"

podman exec -it authapi-fastapi curl -X GET http://localhost:8000/api/v1/auth/admin/dashboard \
  -H "Authorization: Bearer $ACCESS"