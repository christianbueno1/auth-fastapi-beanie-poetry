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

# /users/me
curl -v -X GET http://localhost:8000/api/v1/auth/users/me \
    -H "Authorization: Bearer $ACCESS" \
    -b "$COOKIE_JAR" | jq '.'

curl -v -X GET http://localhost:8000/api/v1/auth/users/me \
    -b "$COOKIE_JAR" | jq '.'

# /users/me/items
curl -v -X GET http://localhost:8000/api/v1/auth/users/me/items \
    -H "Authorization: Bearer $ACCESS" \
    -b "$COOKIE_JAR" | jq '.'

# /admin/dashboards
curl -X GET http://localhost:8000/api/v1/auth/admin/dashboards \
  -H "Authorization: Bearer $ACCESS" \
  -b "$COOKIE_JAR" | jq '.'

curl -X POST http://localhost:8000/api/v1/auth/refresh-token \
  -H "Authorization: Bearer $ACCESS" \
  -b "$COOKIE_JAR" \
  -c "$COOKIE_JAR.new" | jq '.'

# using json format

# register a new user, only admin can do this
curl http://localhost:8000/api/v1/auth/admin/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -b "$COOKIE_JAR" \
  -d '{
    "username": "brucewayne",
    "email": "brucewayne@ibm.com",
    "password": "maGazine1!",
    "disabled": false,
    "role": "user"
}'

curl http://localhost:8000/api/v1/auth/admin/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -b "$COOKIE_JAR" \
  -d '{
    "username": "peterparker",
    "email": "peterparker@ibm.com",
    "password": "maGazine1!",
    "disabled": false,
    "role": "user"
}' | jq '.'

# signup
curl -v -X POST http://localhost:8000/api/v1/auth/signup \
    -H "Content-Type: application/json" \
    -d '{
    "username": "steverogers",
    "email": "steverogers@ibm.com",
    "password": "maGazine1!",
    "disabled": false,
    "role": "user"
}' | jq '.'

curl -v -X POST http://localhost:8000/api/v1/auth/token \
    -H "Content-Type: application/json" \
    -d '{
    "identifier": "brucewayne@ibm.com",
    "password": "maGazine1!"
    }' \
    -c "$COOKIE_JAR"

curl -v -X POST http://localhost:8000/api/v1/auth/token \
    -H "Content-Type: application/json" \
    -d '{
    "identifier": "peterparker@ibm.com",
    "password": "maGazine1!"
    }' \
    -c "$COOKIE_JAR" | jq '.'

# token
curl -v -X POST http://localhost:8000/api/v1/auth/token \
    -H "Content-Type: application/json" \
    -d '{
    "identifier": "christianbueno.1@gmail.com",
    "password": "maGazine1!"
    }' \
    -c "$COOKIE_JAR" | jq '.'

curl -v -X POST http://localhost:8000/api/v1/auth/token \
    -H "Content-Type: application/json" \
    -d '{
    "identifier": "christianbueno.1@gmail.com",
    "password": "maGazine1!"
    }' \
    -c "$COOKIE_JAR" | jq '.'

curl -v -X POST http://localhost:8000/api/v1/auth/token \
    -H "Content-Type: application/json" \
    -d '{
    "identifier": "steverogers@ibm.com",
    "password": "maGazine1!"
    }' \
    -c "$COOKIE_JAR" | jq '.'

# forgot-password
# new_password="hello1!A"
curl -v -X POST http://localhost:8000/api/v1/auth/forgot-password \
    -H "Content-Type: application/json" \
    -d '{
    "email": "christianbueno.1@gmail.com"
    }' | jq '.'

# reset-password
curl -v -X POST http://localhost:8000/api/v1/auth/reset-password \
  -H "Content-Type: application/json" \
  -d '{
  "token": "$TOKEN",
  "new_password": "maGazine1!"
}' | jq '.'

curl -X POST http://localhost:8000/api/v1/auth/clear-tokens

# logout
curl -X POST http://localhost:8000/api/v1/auth/logout \
  -H "Authorization: Bearer $ACCESS" \
  -b "$COOKIE_JAR" | jq '.'

# check root domain
curl -X GET http://localhost:8000/api/v1/auth/ | jq '.'

# test
# /test-reset
curl -v -X GET http://localhost:8000/test/test-reset

# domain=https://authapi.christianbueno.tech/api/v1/auth
curl -X GET https://authapi.christianbueno.tech/api/v1/auth/ | jq '.'

# token
curl -v -X POST https://authapi.christianbueno.tech/api/v1/auth/token \
    -H "Content-Type: application/json" \
    -d '{
    "identifier": "christianbueno.1@gmail.com",
    "password": "maGazine1!"
    }' \
    -c "$COOKIE_JAR" | jq '.'

# /admin/dashboards
curl -X GET https://authapi.christianbueno.tech/api/v1/auth/admin/dashboards \
  -H "Authorization: Bearer $ACCESS" \
  -b "$COOKIE_JAR" | jq '.'

# logout
curl -X POST https://authapi.christianbueno.tech/api/v1/auth/logout \
  -H "Authorization: Bearer $ACCESS" \
  -b "$COOKIE_JAR" | jq '.'

# signup
curl -v -X POST https://authapi.christianbueno.tech/api/v1/auth/signup \
    -H "Content-Type: application/json" \
    -d '{
    "username": "steverogers",
    "email": "steverogers@ibm.com",
    "password": "maGazine1!",
    "disabled": false,
    "role": "user"
}' | jq '.'

# token
curl -v -X POST https://authapi.christianbueno.tech/api/v1/auth/token \
    -H "Content-Type: application/json" \
    -d '{
    "identifier": "steverogers@ibm.com",
    "password": "maGazine1!"
    }' \
    -c "$COOKIE_JAR" | jq '.'

# /users/me
curl -v -X GET https://authapi.christianbueno.tech/api/v1/auth/users/me \
    -H "Authorization: Bearer $ACCESS" \
    -b "$COOKIE_JAR" | jq '.'

# /users/me/items
curl -v -X GET https://authapi.christianbueno.tech/api/v1/auth/users/me/items \
    -H "Authorization: Bearer $ACCESS" \
    -b "$COOKIE_JAR" | jq '.'

# get token-debug
curl -X GET \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Cookie: access_token=YOUR_COOKIE_ACCESS_TOKEN" \
     https://authapi.christianbueno.tech/api/v1/auth/token-debug | jq '.'
# /refresh-token
curl -X POST https://authapi.christianbueno.tech/api/v1/auth/refresh-token \
  -H "Authorization: Bearer $ACCESS" \
  -b "$COOKIE_JAR" \
  -c "$COOKIE_JAR.new" | jq '.'

# /admin/users
curl -X POST https://authapi.christianbueno.tech/api/v1/auth/admin/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -b "$COOKIE_JAR" \
  -d '{
    "username": "peterparker",
    "email": "peterparker@ibm.com",
    "password": "maGazine1!",
    "disabled": false,
    "role": "user"
}' | jq '.'

# /clear-tokens
curl -X POST https://authapi.christianbueno.tech/api/v1/auth/clear-tokens

# forgot-password
curl -v -X POST https://authapi.christianbueno.tech/api/v1/auth/forgot-password \
    -H "Content-Type: application/json" \
    -d '{
    "email": "christianbueno.1@gmail.com"
    }' | jq '.'

# reset-password
curl -v -X POST https://authapi.christianbueno.tech/api/v1/auth/reset-password
  -H "Content-Type: application/json" \
  -d '{
  "token": "$TOKEN",
  "new_password": "maGazine1!"
}' | jq '.'