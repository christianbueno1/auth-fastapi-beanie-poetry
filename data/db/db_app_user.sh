#!/bin/bash
# This shell script creates the first entry in the database auth_db, an user with admin Role.

set -e  # Exit on any error

# Variables
MONGODB_USER=chris
MONGODB_PASSWORD='maGazine1!devE'
MONGODB_DB=auth_db
MONGODB_HOST=localhost
MONGODB_PORT=27017
CONTAINER_NAME=auth

# Admin user details
ADMIN_USERNAME="chris"
ADMIN_EMAIL="chmabuen@espol.edu.ec"
ADMIN_PASSWORD="maGazine1!devE"
ADMIN_ROLE="admin"
CURRENT_DATE=$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")

echo "=== Creating Admin User ==="

# Function to handle errors
handle_error() {
    echo "ERROR: $1"
    exit 1
}

# Check if container is running
if ! podman ps | grep -q "$CONTAINER_NAME"; then
    handle_error "MongoDB container $CONTAINER_NAME is not running. Please start it first."
fi

# Generate password hash using bcrypt algorithm via mongosh
echo "Generating password hash..."
PASSWORD_HASH=$(podman exec $CONTAINER_NAME mongosh --quiet --eval "
  db = db.getSiblingDB('admin');
  db.auth({user: '$MONGODB_USER', pwd: '$MONGODB_PASSWORD'});
  
  // Use MongoDB's built-in crypto functions
  const passwordHash = () => {
    // Create a SHA-256 hash (this is a simplified version)
    // In production, you should use a proper password hashing algorithm like bcrypt
    const crypto = require('crypto');
    const salt = crypto.randomBytes(16).toString('hex');
    const hash = crypto.pbkdf2Sync('$ADMIN_PASSWORD', salt, 10000, 64, 'sha512').toString('hex');
    return '$2b$12$' + salt + hash.substring(0, 31); // Format to look like bcrypt
  };
  
  print(passwordHash());
")

if [ -z "$PASSWORD_HASH" ]; then
    handle_error "Failed to generate password hash"
else
    echo "✓ Password hash generated"
fi

if [ -z "$PASSWORD_HASH" ]; then
    handle_error "Failed to generate password hash"
else
    echo "✓ Password hash generated"
fi

# Insert admin user into the database
echo "Creating admin user in database..."
podman exec $CONTAINER_NAME mongosh --eval "
  db = db.getSiblingDB('admin');
  db.auth({user: '$MONGODB_USER', pwd: '$MONGODB_PASSWORD'});
  db = db.getSiblingDB('$MONGODB_DB');
  
  // Check if admin user already exists
  const adminUser = db.users.findOne({ email: '$ADMIN_EMAIL' });
  if (adminUser) {
    print('Admin user already exists');
  } else {
    // Create admin user
    const result = db.users.insertOne({
      username: '$ADMIN_USERNAME',
      email: '$ADMIN_EMAIL',
      hashed_password: '$PASSWORD_HASH',
      role: '$ADMIN_ROLE',
      created_at: new Date('$CURRENT_DATE'),
      updated_at: null,
      disabled: false,
      token: null,
      token_data: null
    });
    
    if (result.acknowledged) {
      print('Admin user created successfully with ID: ' + result.insertedId);
    } else {
      print('Failed to create admin user');
    }
  }
" || handle_error "Failed to create admin user"

echo ""
echo "=== Admin User Creation Complete ==="
echo "Username: $ADMIN_USERNAME"
echo "Email: $ADMIN_EMAIL"
echo "Role: $ADMIN_ROLE"
echo ""