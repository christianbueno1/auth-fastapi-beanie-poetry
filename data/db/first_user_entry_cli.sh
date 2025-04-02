#!/bin/bash
# filepath: /home/chris/projects/auth-fastapi-beanie-poetry/data/db/first_user_entry.sh
# This script creates an admin user using the create-admin command in the FastAPI container

set -e  # Exit on any error

# Variables
FASTAPI_CONTAINER_NAME="authapi-fastapi"
USERNAME="christianbueno.1"
EMAIL="christianbueno.1@gmail.com"
PASSWORD="maGazine1!"

echo "=== Creating Admin User ==="

# Function to handle errors
handle_error() {
    echo "ERROR: $1"
    exit 1
}

# Check if container exists and is running
if ! podman ps | grep -q "$FASTAPI_CONTAINER_NAME"; then
    handle_error "FastAPI container is not running. Please start it first using pod_setup.sh"
fi

echo "Creating admin user with username: $USERNAME, email: $EMAIL"

# Create a temporary expect script to handle interactive prompts
cat > /tmp/create_admin_expect.exp << EOL
#!/usr/bin/expect -f
spawn podman exec -it $FASTAPI_CONTAINER_NAME poetry run create-admin
expect "Username: "
send "$USERNAME\r"
expect "Email: "
send "$EMAIL\r"
expect "Password: "
send "$PASSWORD\r"
expect eof
EOL

# Make the expect script executable
chmod +x /tmp/create_admin_expect.exp

# Run the expect script
if command -v expect > /dev/null; then
    /tmp/create_admin_expect.exp
else
    echo "The 'expect' command is not installed. Installing it now..."
    sudo dnf install -y expect || handle_error "Failed to install expect"
    /tmp/create_admin_expect.exp
fi

# Clean up temporary file
rm /tmp/create_admin_expect.exp

echo ""
echo "=== Admin User Creation Complete ==="
echo "Username: $USERNAME"
echo "Email: $EMAIL"
echo ""
echo "You can now log in using these credentials."