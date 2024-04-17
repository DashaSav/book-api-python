import os
import time

from dotenv import load_dotenv
from jose import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer

from src.models.token import Token


load_dotenv()

JWT_SECRET = os.environ["SECRET_KEY"]
JWT_ALGORITHM = os.environ["ALGORITHM"]
SECONDS_TO_EXPIRE = 60 * 60 * 24 * 180


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, token: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(token)
        except:
            payload = None
        
        if payload:
            isTokenValid = True
        return isTokenValid


def signJWT(user_id: str) -> Token:
    payload = {
        "user_id": user_id,
        "expires": time.time() + SECONDS_TO_EXPIRE
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return Token(access_token=token)


def decodeJWT(token: str) -> dict | None:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
