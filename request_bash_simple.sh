curl -v -X POST http://localhost:8000/api/v1/auth/token \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=christianbueno.1@gmail.com&password=maGazine1\!"

curl -v -X POST http://localhost:8000/api/v1/auth/signup \
    -H "Content-Type: application/json" \
    -d '{
    "username": "bruce123",
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
    "email": "tim123@ibm.com",
    "password": "maGazine1!",
    "disabled": false,
    "role": "user"
}'

curl -X POST http://localhost:8000/api/v1/auth/refresh-token \
  -H "Authorization: Bearer $ACCESS"

curl -X GET http://localhost:8000/api/v1/auth/users/me \
  -H "Authorization: Bearer $ACCESS"

curl -X GET http://localhost:8000/api/v1/auth/admin/dashboards \
  -H "Authorization: Bearer $ACCESS"

# Using full domain name
export FULL_DOMAIN_NAME="authapi.christianbueno.tech"

curl -v -X POST http://authapi.christianbueno.tech/api/v1/auth/token \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=christianbueno.1@gmail.com&password=maGazine1\!"

curl -X GET http://authapi.christianbueno.tech/api/v1/auth/users/me \
  -H "Authorization: Bearer $ACCESS"

# /users/me/items
curl -X GET http://authapi.christianbueno.tech/api/v1/auth/users/me/items \
  -H "Authorization: Bearer $ACCESS" \


# HTTPS
curl -v -X POST https://authapi.christianbueno.tech/api/v1/auth/token \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=christianbueno.1@gmail.com&password=maGazine1\!"

curl -v -X POST https://authapi.christianbueno.tech/api/v1/auth/token \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=tim123@ibm.com&password=maGazine1\!"

curl -v -X POST https://authapi.christianbueno.tech/api/v1/auth/token \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=brucewayne@ibm.com&password=maGazine1\!"

curl -X GET https://authapi.christianbueno.tech/api/v1/auth/users/me \
  -H "Authorization: Bearer $ACCESS"

# /users/me/items
curl -X GET https://authapi.christianbueno.tech/api/v1/auth/users/me/items \
  -H "Authorization: Bearer $ACCESS"

# dashboard
curl -X GET https://authapi.christianbueno.tech/api/v1/auth/admin/dashboards \
-H "Authorization: Bearer $ACCESS"

# /clear-tokens
curl -X POST https://authapi.christianbueno.tech/api/v1/auth/clear-tokens

curl -X POST https://authapi.christianbueno.tech/api/v1/auth/refresh-token \
  -H "Authorization: Bearer $ACCESS"

# public signup
curl -v -X POST https://authapi.christianbueno.tech/api/v1/auth/signup \
    -H "Content-Type: application/json" \
    -d '{
    "username": "brucewayne",
    "email": "brucewayne@ibm.com",
    "password": "maGazine1!",
    "disabled": false,
    "role": "user"
}'

# register a new user, only admin can do this    
curl https://authapi.christianbueno.tech/api/v1/auth/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "username": "tim123",
    "email": "tim123@ibm.com",
    "password": "maGazine1!",
    "disabled": false,
    "role": "user"
}'

### HttpOnly cookies
# export COOKIE_JAR="cookies.txt"
touch cookies.txt

curl -v -X POST http://localhost:8000/api/v1/auth/token \
    -c "$COOKIE_JAR" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=bruce123@ibm.com&password=hello1\!A"

curl -v -X GET http://localhost:8000/api/v1/auth/users/me \
    -b "$COOKIE_JAR"
#    
curl -v -X POST http://localhost:8000/api/v1/auth/token \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=christianbueno.1@gmail.com&password=maGazine1\!" \
    -c cookies.txt

curl -v -X POST http://localhost:8000/api/v1/auth/token \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=bruce123@ibm.com&password=hello1\!A" \
    -c cookies.txt

curl -v -X GET http://localhost:8000/api/v1/auth/users/me \
    -H "Authorization: Bearer $ACCESS" \
    -b cookies.txt

curl -X GET http://localhost:8000/api/v1/auth/admin/dashboards \
  -H "Authorization: Bearer $ACCESS" \
  -b cookies.txt

curl -X POST http://localhost:8000/api/v1/auth/refresh-token \
  -H "Authorization: Bearer $ACCESS" \
  -c "$COOKIE_JAR"