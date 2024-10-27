# This file is responsible for signing , encoding , decoding and returning JWTS
import time
from typing import Dict
from passlib.context import CryptContext 

import jwt
# from decouple import config


JWT_SECRET = "secret"
JWT_ALGORITHM = 'HS256'

pwd_context = CryptContext(schemes=['bcrypt'] , deprecated ='auto')

def get_password_hash(password):
    print("password",password)
    return pwd_context.hash(password) 

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password) 
    
def token_response(token: str):
    return {
        "token": token
    }

# function used for signing the JWT string
def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 31536000 # 1 year exp
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}