#!/bin/bash

# Variables
POD_NAME="authapi-pod"
FASTAPI_IMAGE="docker.io/christianbueno1/authapi-fastapi:1.0"
MONGO_IMAGE="docker.io/mongodb/mongodb-community-server:7.0.16-ubi9"
MONGO_CONTAINER_NAME="authapi-mongo"
FASTAPI_CONTAINER_NAME="authapi-fastapi"
MONGO_USER="chris"
MONGO_PASSWORD="maGazine1!devE"
MONGO_DB="auth_db"

# Step 1: Create a Podman pod
echo "Creating Podman pod: $POD_NAME"
podman pod create --name $POD_NAME -p 8000:80 -p 27017:27017

# Step 2: Start MongoDB container
echo "Starting MongoDB container..."
podman run -d --pod $POD_NAME --name $MONGO_CONTAINER_NAME \
  -e MONGO_INITDB_ROOT_USERNAME="$MONGO_USER" \
  -e MONGO_INITDB_ROOT_PASSWORD="$MONGO_PASSWORD" \
  $MONGO_IMAGE

# Step 3: Build the FastAPI container
echo "Building FastAPI container..."
podman build -t $FASTAPI_IMAGE -f Containerfile .

# Step 4: Start the FastAPI container
echo "Starting FastAPI container..."
podman run -d --pod $POD_NAME --name $FASTAPI_CONTAINER_NAME \
  --env-file .env \
  $FASTAPI_IMAGE

# Step 5: Display pod and container status
echo "Pod and containers are running."
podman pod ps
podman ps -p

# Step 6: Create MongoDB user for the application
echo "Creating MongoDB user for the application..."
podman exec $MONGO_CONTAINER_NAME mongosh --eval '
db = db.getSiblingDB("admin");
db.auth({user: $MONGO_USER, pwd: $MONGO_PASSWORD});
db = db.getSiblingDB("$MONGO_DB");
db.createUser({
  user: "$MONGO_USER",
  pwd: "$MONGO_PASSWORD",
  roles: [{ role: "readWrite", db: "$MONGO_DB" }]
});
db.createCollection("users");
db.createCollection("tokens");
'
echo "MongoDB user created successfully."