#!/bin/bash
# filepath: /home/chris/projects/auth-fastapi-beanie-poetry/pod_setup.sh

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

# Wait for MongoDB to be ready
echo "Waiting for MongoDB to start up..."
sleep 10

# Step 3: Create MongoDB user for the application
echo "Creating MongoDB user for the application..."
podman exec $MONGO_CONTAINER_NAME mongosh --eval "
db = db.getSiblingDB('admin');
db.auth({user: '$MONGO_USER', pwd: '$MONGO_PASSWORD'});
db = db.getSiblingDB('$MONGO_DB');

// Check if user already exists
const userExists = db.getUser('$MONGO_USER');
if (!userExists) {
  db.createUser({
    user: '$MONGO_USER',
    pwd: '$MONGO_PASSWORD',
    roles: [{ role: 'readWrite', db: '$MONGO_DB' }]
  });
  print('MongoDB user created successfully.');
} else {
  print('MongoDB user already exists.');
}

// Create collections if they don't exist
if (!db.getCollectionNames().includes('users')) {
  db.createCollection('users');
  print('Users collection created.');
}
if (!db.getCollectionNames().includes('tokens')) {
  db.createCollection('tokens');
  print('Tokens collection created.');
}
"

# Step 4: Build the FastAPI container
echo "Building FastAPI container..."
podman build -t $FASTAPI_IMAGE -f Containerfile .

# Step 5: Start the FastAPI container
echo "Starting FastAPI container..."
podman run -d --pod $POD_NAME --name $FASTAPI_CONTAINER_NAME \
  --env-file .env \
  $FASTAPI_IMAGE

# Step 6: Display pod and container status
echo "Pod and containers are running."
podman pod ps
podman ps -p

echo "Setup complete. Your API is now available at http://localhost:8000"