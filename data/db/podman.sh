#create the database
podman run -d --name auth -e MONGO_INITDB_ROOT_USERNAME=chris -e MONGO_INITDB_ROOT_PASSWORD='maGazine1!devE' -p 27017:27017 mongodb-community-server:7.0.16-ubi9

# Create MongoDB user for the application, using the database auth_db which not exist yet
podman exec -it auth mongosh -u chris -p 'maGazine1!devE' --authenticationDatabase admin --eval '
use auth_db;
db.createUser
({
  user: "chris",
  pwd: "maGazine1!devE",
  roles: [
    { role: "readWrite", db: "auth_db" }
  ]
});
db.createCollection("users");
db.createCollection("roles");
db.createCollection("permissions");
'

# verify the database
podman exec -it auth mongosh -u chris -p 'maGazine1!devE' --authenticationDatabase admin --eval '
use auth_db;
db.users.find();
db.roles.find();
db.permissions.find();
'
# Create a new user in the database
podman exec -it auth mongosh -u chris -p 'maGazine1!devE' --authenticationDatabase admin --eval '
use auth_db;
db.users.insertOne({
  username: "testuser",
  password: "testpassword",
  email: "chris@ibm.com",
  roles: ["user"],
  permissions: ["read"]
});
db.roles.insertOne({
  role: "admin",
  permissions: ["read", "write", "delete"]
});
db.permissions.insertOne({
  permission: "read",
  description: "Read access to the database"
});
db.permissions.insertOne({
  permission: "write",
  description: "Write access to the database"
});
db.permissions.insertOne({
  permission: "delete",
  description: "Delete access to the database"
});
'
# Verify the new user
podman exec -it auth mongosh -u chris -p 'maGazine1!devE' --authenticationDatabase admin --eval '
use auth_db;
db.users.find();
db.roles.find();
db.permissions.find();
'

