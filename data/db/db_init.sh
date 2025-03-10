#!/bin/bash
# This script creates a MongoDB container using Podman and initializes it with a user and database.
# System fedora 41 Linux

set -e  # Exit on any error

MONGODB_USER=chris
MONGODB_PASSWORD='maGazine1!devE'
MONGODB_DB=auth_db
MONGODB_HOST=localhost
MONGODB_PORT=27017
CONTAINER_IMAGE=docker.io/mongodb/mongodb-community-server:7.0.16-ubi9

echo "=== MongoDB Setup Script ==="

# Function to handle errors
handle_error() {
    echo "ERROR: $1"
    exit 1
}

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
if ! podman images | grep -q $CONTAINER_IMAGE; then
    echo "MongoDB image not found, pulling it..."
    podman pull $CONTAINER_IMAGE || handle_error "Failed to pull MongoDB image"
    echo "✓ MongoDB image pulled successfully"
else
    echo "✓ MongoDB image already available"
fi

# Check if MongoDB container exists, if not create it
if ! podman ps -a | grep -q "auth"; then
    echo "MongoDB container not found, creating it..."
    podman run -d --name auth \
        -e MONGO_INITDB_ROOT_USERNAME=$MONGODB_USER \
        -e MONGO_INITDB_ROOT_PASSWORD=$MONGODB_PASSWORD \
        -p $MONGODB_PORT:$MONGODB_PORT \
        $CONTAINER_IMAGE || handle_error "Failed to create MongoDB container"
    echo "✓ MongoDB container created"
    
    # Wait for MongoDB to start
    echo "Waiting for MongoDB to start..."
    sleep 5
else
    echo "✓ MongoDB container exists"
    
    # Check if container is running, if not start it
    if ! podman ps | grep -q "auth"; then
        echo "MongoDB container is not running, starting it..."
        podman start auth || handle_error "Failed to start MongoDB container"
        echo "✓ MongoDB container started"
        
        # Wait for MongoDB to start
        echo "Waiting for MongoDB to start..."
        sleep 5
    else
        echo "✓ MongoDB container is running"
    fi
fi

# Setup the database and user
echo "Setting up MongoDB database and user..."
if podman exec auth mongosh --eval "
  db = db.getSiblingDB('admin');
  db.auth({user: '$MONGODB_USER', pwd: '$MONGODB_PASSWORD'});
  db = db.getSiblingDB('$MONGODB_DB');
  
  // Check if user already exists
  if (!db.getUser('$MONGODB_USER')) {
    db.createUser({
      user: '$MONGODB_USER',
      pwd: '$MONGODB_PASSWORD',
      roles: [{ role: 'readWrite', db: '$MONGODB_DB' }]
    });
    print('User created successfully');
  } else {
    print('User already exists');
  }
  
  // Create collections if they don't exist
  if (!db.getCollectionNames().includes('users')) {
    db.createCollection('users');
    print('Users collection created');
  }
  if (!db.getCollectionNames().includes('tokens')) {
    db.createCollection('tokens');
    print('Tokens collection created');
  }
  
  print('Database setup completed successfully');
"; then
    echo "✓ MongoDB database and user setup completed"
else
    handle_error "Failed to set up MongoDB database and user"
fi

echo ""
echo "=== Setup Complete ==="
echo "Connection string: mongodb://${MONGODB_USER}:${MONGODB_PASSWORD}@${MONGODB_HOST}:${MONGODB_PORT}/${MONGODB_DB}?authSource=${MONGODB_DB}"
echo ""