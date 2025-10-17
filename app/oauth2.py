from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "7e4f8b63a0d9e96c1b2a3cfc1a32a1b14ef2f7b91e6b1c93b3a945b6e9dfb7ac"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_token
