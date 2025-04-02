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

# Step 1: Create a Podman pod
echo "🚀 Creating Podman pod: $PODMAN_POD_NAME"
podman pod create --name $PODMAN_POD_NAME -p 8000:8000 -p 27017:27017

# Step 2: Start MongoDB container
echo "🐳 Starting MongoDB container..."
podman run -d --pod $PODMAN_POD_NAME --name $PODMAN_MONGO_CONTAINER \
  -e MONGO_INITDB_ROOT_USERNAME="$MONGO_USER" \
  -e MONGO_INITDB_ROOT_PASSWORD="$MONGO_PASSWORD" \
  $PODMAN_MONGO_IMAGE

# Wait for MongoDB to be ready
echo "⏳ Waiting for MongoDB to start up..."
sleep 10

# Step 3: Create MongoDB user for the application
echo "🔑 Creating MongoDB user for the application..."
podman exec $PODMAN_MONGO_CONTAINER mongosh --eval "
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
  print('✅ MongoDB user created successfully.');
} else {
  print('ℹ️  MongoDB user already exists.');
}

// Create collections if they don't exist
if (!db.getCollectionNames().includes('users')) {
  db.createCollection('users');
  print('✅ Users collection created.');
}
if (!db.getCollectionNames().includes('tokens')) {
  db.createCollection('tokens');
  print('✅ Tokens collection created.');
}
"

# Step 4: Create environment file for FastAPI
# using a heredoc with unquoted delimiter EOF to allow variable expansion
echo "📝 Creating environment file for FastAPI..."
cat > .env << EOF
# Application settings
APP_NAME="Authentication API"
APP_VERSION=1.0.0
DEBUG=false
ENVIRONMENT=production

FASTAPI_PORT=8001
API_BASE_URL=https://authapi.christianbueno.tech
API_PREFIX=/api/v1/auth
API_FULL_URL=${API_BASE_URL}${API_PREFIX}

# MongoDB settings
MONGO_USER=chris
MONGO_PASSWORD=maGazine1!devE
MONGO_DB=auth_db
MONGO_HOST=127.0.0.1
MONGO_PORT=27017
MONGODB_URL=mongodb://$MONGO_USER:$MONGO_PASSWORD@$PODMAN_MONGO_CONTAINER:27017/$MONGO_DB?authSource=$MONGO_DB

# Containerized MongoDB settings
# Podman settings
PODMAN_POD_NAME=authapi-pod
PODMAN_MONGO_IMAGE_NAME=docker.io/mongodb/mongodb-community-server
PODMAN_MONGO_IMAGE_TAG=7.0.16-ubi9
PODMAN_MONGO_IMAGE=${PODMAN_MONGO_IMAGE_NAME}:${PODMAN_MONGO_IMAGE_TAG}
PODMAN_MONGO_PORT=27017
PODMAN_MONGO_CONTAINER=authapi-mongo
# FASTAPI settings
PODMAN_FASTAPI_PORT=8001

# JWT settings
JWT_SECRET=42891bae22bf0ac1857c5b9c93cc0bec74399e366a9dbadc73181d95fe8f0d2f
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30

# Security
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:5173","http://localhost:4321","https://yourproductionsite.com"]

# Email configuration
MAIL_USERNAME=prabbzacsspy4tdy
MAIL_PASSWORD=1mrgqdpl3k2jksxi
MAIL_FROM=no-reply@example.com
MAIL_PORT=2525
MAIL_SERVER=smtp.mailmug.net
MAIL_SSL_TLS=False
USE_CREDENTIALS=True
EOF

# Step 5: Build the FastAPI container
echo "🏗️  Building FastAPI container..."
podman build -t $PODMAN_FASTAPI_IMAGE -f Containerfile .

# Step 6: Start the FastAPI container
echo "🚀 Starting FastAPI container..."
podman run -d --pod $PODMAN_POD_NAME --name $PODMAN_FASTAPI_CONTAINER \
  --env-file .env \
  $PODMAN_FASTAPI_IMAGE

# Step 7: Display pod and container status
echo "🔍 Displaying pod and container status..."
podman pod ps
podman ps -p

echo "✅ Setup complete. Your API is now available at http://authapi.christianbueno.tech"