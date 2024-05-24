import jwt
from fastapi import Depends

# JWT setup #TODO: hide this
SECRET_KEY = "banana-apple-smoothie"
ALGORITHM = "HS256"

# JWT verification
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        if username is None:
            raise Exception("Invalid token")
    except Exception as e:
        raise Exception("Invalid token") from e
    return token