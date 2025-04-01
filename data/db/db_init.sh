#!/bin/bash
# filepath: /home/chris/projects/auth-fastapi-beanie-poetry/data/db/db_init.sh
# This script creates a MongoDB container using Podman and initializes it with a user and database.
# System fedora 41 Linux

set -e  # Exit on any error

# Define the path to the .env file
ENV_FILE="/home/chris/projects/auth-fastapi-beanie-poetry/.env"
# Check if the .env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "ERROR: .env file not found at $ENV_FILE"
    exit 1
fi
# Load environment variables from the .env file
# export $(grep -v '^#' "$ENV_FILE" | xargs)

# load and support variable substitution
# Source environment variables (ensuring variable expansion)
set -a
. "$ENV_FILE"
set +a

# Variables
# MONGO_USER=chris
# MONGO_PASSWORD='maGazine1!devE'
# MONGO_DB=auth_db
# MONGO_HOST=localhost
# MONGO_PORT=27017
# PODMAN_POD_NAME="authapi-pod"
# PODMAN_MONGO_IMAGE=docker.io/mongodb/mongodb-community-server:7.0.16-ubi9
# PODMAN_MONGO_CONTAINER="authapi-mongo"


# Function to handle errors
handle_error() {
    echo "ERROR: $1"
    exit 1
}

echo "=== MongoDB Setup Script ==="

# Create a Podman container for MongoDB
# Check if Podman is installed, if not install it
if ! command -v podman &> /dev/null; then
    echo "Podman could not be found, installing..."
    sudo dnf install -y podman || handle_error "Failed to install Podman"
    echo "✓ Podman installed successfully"
else
    echo "✓ Podman already installed"
fi

# Check if Podman is running, if not start it
if ! podman info &> /dev/null; then
    echo "Podman is not running, starting it..."
    podman machine start || handle_error "Failed to start Podman"
    echo "✓ Podman started"
else
    echo "✓ Podman is running"
fi

# Check if MongoDB image is available, if not pull it
if ! podman images | grep -q "$PODMAN_MONGO_IMAGE_NAME"; then
    echo "MongoDB image not found, pulling it..."
    podman pull "$PODMAN_MONGO_IMAGE" || handle_error "Failed to pull MongoDB image"
    echo "✓ MongoDB image pulled successfully"
else
    echo "✓ MongoDB image already available"
fi

# Step 1: Check if pod exists, create if not
if ! podman pod exists "$PODMAN_POD_NAME"; then
    echo "Creating Podman pod: $PODMAN_POD_NAME"
    podman pod create --name "$PODMAN_POD_NAME" -p "$PODMAN_FASTAPI_PORT":80 -p "$PODMAN_MONGO_PORT":27017 || handle_error "Failed to create pod"
    echo "✓ Pod created successfully"
else
    echo "✓ Pod $PODMAN_POD_NAME already exists"
fi

# Step 2: Check if MongoDB container exists inside pod, create if not
if ! podman ps -a --pod --filter "pod=$PODMAN_POD_NAME" | grep -q "$PODMAN_MONGO_CONTAINER"; then
    echo "MongoDB container not found in pod, creating it..."
    podman run -d --pod "$PODMAN_POD_NAME" --name "$PODMAN_MONGO_CONTAINER" \
        -e MONGO_INITDB_ROOT_USERNAME="$MONGO_USER" \
        -e MONGO_INITDB_ROOT_PASSWORD="$MONGO_PASSWORD" \
        "$PODMAN_MONGO_IMAGE" || handle_error "Failed to create MongoDB container"
    echo "✓ MongoDB container created"
    
    # Wait for MongoDB to start
    echo "Waiting for MongoDB to start..."
    sleep 10
else
    echo "✓ MongoDB container exists in pod"
    
    # Check if container is running, if not start it
    if ! podman ps --pod --filter "pod=$PODMAN_POD_NAME" | grep -q "$PODMAN_MONGO_CONTAINER"; then
        echo "MongoDB container is not running, starting it..."
        podman start "$PODMAN_MONGO_CONTAINER" || handle_error "Failed to start MongoDB container"
        echo "✓ MongoDB container started"
        
        # Wait for MongoDB to start
        echo "Waiting for MongoDB to start..."
        sleep 5
    else
        echo "✓ MongoDB container is running"
    fi
fi

# Step 3: Create MongoDB user for the application
echo "Creating MongoDB user for the application..."
if podman exec "$PODMAN_MONGO_CONTAINER" mongosh --eval "
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
"; then
    echo "✓ MongoDB database and user setup completed"
else
    handle_error "Failed to set up MongoDB database and user"
fi

echo ""
echo "=== Setup Complete ==="
echo "MongoDB is available in pod: $PODMAN_POD_NAME"
echo "Connection string: mongodb://${MONGO_USER}:${MONGO_PASSWORD}@${MONGO_HOST}:${PODMAN_MONGO_PORT}/${MONGO_DB}?authSource=admin"
echo ""