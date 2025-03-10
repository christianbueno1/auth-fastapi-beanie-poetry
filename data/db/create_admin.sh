#!/bin/bash
# filepath: /home/chris/projects/auth-fastapi-beanie-poetry/create_admin.sh

set -e

# Variables
CONTAINER_NAME="authapi-fastapi"
ADMIN_USERNAME="christianbueno1"
ADMIN_EMAIL="christianbueno.1@gmail.com"
ADMIN_PASSWORD="maGazine1!"

echo "=== Creating Admin User ==="

# Check if container is running
if ! podman ps | grep -q $CONTAINER_NAME; then
    echo "ERROR: Container $CONTAINER_NAME is not running"
    exit 1
fi

# Create a Python script that bypasses the CLI interface
cat > /tmp/create_admin.py << EOF
from auth_fastapi_beanie_poetry.models.user import User, Role
from auth_fastapi_beanie_poetry.core.security import get_password_hash
from auth_fastapi_beanie_poetry.db.mongo import init_db
import asyncio

async def create_admin():
    # Initialize database connection
    await init_db()
    
    # Check if admin exists
    admin = await User.find_one(User.email == "$ADMIN_EMAIL")
    if admin:
        print(f"Admin user already exists with email {admin.email}")
        return
    
    # Create admin user
    admin = User(
        username="$ADMIN_USERNAME",
        email="$ADMIN_EMAIL",
        hashed_password=get_password_hash("$ADMIN_PASSWORD"),
        role=Role.ADMIN,
        disabled=False
    )
    await admin.insert()
    print(f"Admin user created successfully with email {admin.email}")

if __name__ == "__main__":
    asyncio.run(create_admin())
EOF

# Execute the Python script inside the container
echo "Creating admin user: $ADMIN_USERNAME with email: $ADMIN_EMAIL"
podman exec -i $CONTAINER_NAME python -c "$(cat /tmp/create_admin.py)"

# Clean up
rm /tmp/create_admin.py

echo "Admin user creation process completed."
echo "You can now login with:"
echo "Email: $ADMIN_EMAIL"
echo "Password: $ADMIN_PASSWORD"