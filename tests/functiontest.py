import jwt #pyjwt

# Define the payload
to_encode = {"some": "payload"}

# Define the secret key and algorithm
SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"

# Encode the payload
encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# The result is a byte string
print(encoded_jwt, f"Type: {type(encoded_jwt)}")
print(f"{encoded_jwt.upper()}")
print(f"{encoded_jwt.capitalize()}")
print(f"{encoded_jwt.split(".")}")
print(f"encoded: {encoded_jwt.encode()}, Type: {type(encoded_jwt.encode())}")

# Decode the byte string into a regular string
# decoded_jwt = encoded_jwt.decode('UTF-8')
decoded_jwt = jwt.decode(encoded_jwt, SECRET_KEY, algorithms=[ALGORITHM])

print(decoded_jwt)