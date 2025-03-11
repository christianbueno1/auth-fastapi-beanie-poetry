curl -v -X POST http://localhost:8000/api/v1/auth/token \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=christianbueno.1@gmail.com&password=maGazine1\!"

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