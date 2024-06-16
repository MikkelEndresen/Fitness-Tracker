import jwt
from fastapi import Depends

from datetime import datetime
import os
import json

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

def token_to_user(token: str):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        if username is None:
            raise Exception("Invalid token")
    except Exception as e:
        raise Exception("Invalid token") from e
    return username


def store_query(query: str, result):
    date = datetime.now()
    month = date.strftime("%B")

    filename = month + "_queries.json"
    filepath = "data/" + filename
    if os.path.exists(filepath):
        file = open(filepath, 'r')
        json_data = json.load(file)
    else:
        json_data = {}
    
    file = open(filepath, 'w')

    json_data[query] = result
    json.dump(json_data, file)