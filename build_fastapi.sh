#!/bin/bash

# Variables
PODMAN_POD_NAME="authapi-pod"
PODMAN_FASTAPI_IMAGE="docker.io/christianbueno1/authapi-fastapi:1.0"
PODMAN_MONGO_IMAGE="docker.io/mongodb/mongodb-community-server:7.0.16-ubi9"
PODMAN_MONGO_CONTAINER="authapi-mongo"
PODMAN_FASTAPI_CONTAINER="authapi-fastapi"
MONGO_USER="chris"
MONGO_PASSWORD="maGazine1!devE"
MONGO_DB="auth_db"

# check there exists PODMAN_MONGO_CONTAINER inside PODMAN_POD_NAME
echo "Checking if MongoDB container exists inside pod..."
if podman ps -a | grep -q "$PODMAN_MONGO_CONTAINER"; then
    echo "✓ MongoDB container already exists"
else
  echo "The PODMAN_MONGO_CONTAINER doesn't exist"
  exit 1
fi

# build the FastAPI image
echo "🚀 Building FastAPI image: $PODMAN_FASTAPI_IMAGE"
podman build -t $PODMAN_FASTAPI_IMAGE . || { echo "Failed to build FastAPI image"; exit 1; }
echo "✓ FastAPI image built successfully"

# stop and rm the FastAPI container if it exists
if podman ps -a | grep -q "$PODMAN_FASTAPI_CONTAINER"; then
    echo "Stopping and removing existing FastAPI container..."
    podman stop $PODMAN_FASTAPI_CONTAINER || { echo "Failed to stop FastAPI container"; exit 1; }
    podman rm $PODMAN_FASTAPI_CONTAINER || { echo "Failed to remove FastAPI container"; exit 1; }
    echo "✓ FastAPI container stopped and removed"
else
    echo "✓ No existing FastAPI container found"
fi

# start the PODMAN_FASTAPI_CONTAINER inside the PODMAN_POD_NAME
echo "🐳 Starting FastAPI container..."
podman run -d --pod $PODMAN_POD_NAME --name $PODMAN_FASTAPI_CONTAINER \
  --env-file .env \
  $PODMAN_FASTAPI_IMAGE || { echo "Failed to start FastAPI container"; exit 1; }
echo "✓ FastAPI container started successfully"
echo "FastAPI container is running at https://authapi.christianbueno.tech:8000"
