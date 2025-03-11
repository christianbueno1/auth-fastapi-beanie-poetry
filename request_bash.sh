#!/bin/bash
# filepath: /home/chris/projects/auth-fastapi-beanie-poetry/test_create_user.sh

# Set variables
API_URL="http://localhost:8000/api/v1/auth"
ADMIN_EMAIL="christianbueno.1@gmail.com"
ADMIN_PASSWORD="maGazine1!"
NEW_USERNAME="testuser"
NEW_EMAIL="testuser@example.com"
NEW_PASSWORD="Test123!"
NEW_ROLE="user"  # Must be lowercase: admin, user, or guest

# Step 1: Get the admin token
echo "Getting admin token..."
TOKEN_RESPONSE=$(curl -s -X POST "${API_URL}/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=${ADMIN_EMAIL}&password=${ADMIN_PASSWORD}")

# Extract the access token
ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$ACCESS_TOKEN" ]; then
    echo "Failed to get access token. Response:"
    echo $TOKEN_RESPONSE
    exit 1
fi

echo "Access token obtained successfully."

# Step 2: Use the token to create a new user
echo "Creating new user..."
USER_RESPONSE=$(curl -s -X POST "${API_URL}/users" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -d '{
    "username": "'$NEW_USERNAME'",
    "email": "'$NEW_EMAIL'",
    "password": "'$NEW_PASSWORD'",
    "role": "'$NEW_ROLE'"
  }')

echo "Response:"
echo $USER_RESPONSE | jq . 2>/dev/null || echo $USER_RESPONSE

# Step 3: Try to login with the new user to confirm it was created
echo -e "\nTesting login with new user..."
LOGIN_RESPONSE=$(curl -s -X POST "${API_URL}/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=${NEW_EMAIL}&password=${NEW_PASSWORD}")

echo "Login response:"
echo $LOGIN_RESPONSE | jq . 2>/dev/null || echo $LOGIN_RESPONSE