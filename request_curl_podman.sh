curl -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=christianbueno.1@gmail.com&password=maGazine1\!"

#!/bin/bash
# filepath: /home/chris/projects/auth-fastapi-beanie-poetry/test_auth_json.sh

# Try using JSON instead of form data
echo "Testing with JSON request..."
curl -v -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"christianbueno.1@gmail.com", "password":"maGazine1!"}'

# If that doesn't work, try proper URL encoding with form data
echo "Testing with properly encoded form data..."
curl -v -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=christianbueno.1%40gmail.com&password=maGazine1%21"

# If container is running on different IP, try accessing through container IP
echo "Testing container IP..."
CONTAINER_IP=$(podman inspect -f '{{.NetworkSettings.IPAddress}}' authapi-fastapi)
curl -v -X POST http://$CONTAINER_IP:8000/api/v1/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=christianbueno.1@gmail.com&password=maGazine1\!"

###
#!/bin/bash
# Direct request to the FastAPI container inside the pod

# Method 1: Use podman exec to make request from inside the container
echo "Method 1: Using podman exec to make request from inside container"
podman exec -it authapi-fastapi curl -v -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=christianbueno.1@gmail.com&password=maGazine1\!"

# Method 2: Fix the port mapping issue
echo "Method 2: Fixing port mapping"
# Stop containers
podman stop authapi-fastapi
podman pod stop authapi-pod

# Recreate pod with correct port mapping
podman pod rm authapi-pod
podman pod create --name authapi-pod -p 8000:8000 -p 27017:27017

# Restart containers with correct pod
# ...

# Method 3: Use the correct port in request
echo "Method 3: Using correct port"
curl -v -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=christianbueno.1@gmail.com&password=maGazine1\!"


### install
# Step 1: Install curl in the container
podman exec -it authapi-fastapi apt-get update
podman exec -it authapi-fastapi apt-get install -y curl

# Step 2: Now try your curl command
podman exec -it authapi-fastapi curl -v -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=christianbueno.1@gmail.com&password=maGazine1\!"


###
#!/bin/bash
# filepath: /home/chris/projects/auth-fastapi-beanie-poetry/fix_mongodb_connection.sh

# Set correct MongoDB connection URL
echo "Setting correct MongoDB connection URL..."
podman exec -it authapi-fastapi bash -c "echo 'MONGODB_URL=mongodb://chris:maGazine1\!devE@authapi-mongo:27017/auth_db?authSource=admin' > /app/.env"
podman exec -it authapi-fastapi bash -c "echo 'MONGODB_NAME=auth_db' >> /app/.env"

# Restart the FastAPI container
echo "Restarting FastAPI container..."
podman restart authapi-fastapi

# Check if environment variables are set correctly
echo "Checking environment variables..."
podman exec -it authapi-fastapi env | grep MONGO

# Test the API
echo "Testing the API..."
podman exec -it authapi-fastapi curl -v -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=christianbueno.1@gmail.com&password=maGazine1\!"