curl -v -X POST http://localhost:8000/api/v1/auth/token \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=christianbueno.1@gmail.com&password=maGazine1\!"

curl -v -X POST http://localhost:8000/api/v1/auth/signup \
    -H "Content-Type: application/json" \
    -d '{
    "username": "bruce1234",
    "email": "bruce123@ibm.com",
    "password": "hello1!A",
    "disabled": false,
    "role": "user"
}'

curl -v -X POST http://localhost:8000/api/v1/auth/token \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=bruce123@ibm.com&password=hello1\!A"

# register a new user, only admin can do this    
curl http://localhost:8000/api/v1/auth/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "username": "tim123",
    "email": "tim@foo.xyz",
    "password": "magazine1!",
    "disabled": false,
    "role": "user"
}'

curl -X POST http://localhost:8000/api/v1/auth/refresh-token \
  -H "Authorization: Bearer $ACCESS"

curl -X GET http://localhost:8000/api/v1/auth/users/me \
  -H "Authorization: Bearer $ACCESS"

curl -X GET http://localhost:8000/api/v1/auth/admin/dashboard \
  -H "Authorization: Bearer $ACCESS"

# Using full domain name
export FULL_DOMAIN_NAME="authapi.christianbueno.tech"
curl -v -X POST http://authapi.christianbueno.tech/api/v1/auth/token \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=christianbueno.1@gmail.com&password=maGazine1\!"
