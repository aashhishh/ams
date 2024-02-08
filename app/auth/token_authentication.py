from jose import jwe
import jwt
import time
from app.config import Config
from app_logging import logger
from fastapi import Request
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

EXPIRATION_IN_DAY = 30
EXPIRE_AFTER = 24*60*60*EXPIRATION_IN_DAY
TOKEN_ALGORITHM = 'HS256'
ENCRYPT_ALGORITHM = 'A256GCM'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def generate_payload(uuid=None,role ='user',email=None, expire_after=EXPIRE_AFTER):
    return {
        'id': uuid,
        'email':email,
        'exp': int(time.time()+EXPIRE_AFTER)
    }


def sign_jwt(payload, headers=None):
    jwt_token = jwt.encode(payload, key=Config.TOKEN_SECRET, algorithm=TOKEN_ALGORITHM)
    return jwt_token


def encrypt_jwe(jwt_token):
    jwe_token = jwe.encrypt(jwt_token, key=Config.ENCRYPT_SECRET, encryption=ENCRYPT_ALGORITHM)
    return jwe_token


def verify_jwt(jwt_token):
    payload = {}
    try:
        payload = jwt.decode(jwt_token, key=Config.TOKEN_SECRET, algorithms=TOKEN_ALGORITHM)
    except Exception as e:
        logger.warning(f'[AUTH] Verify failed, error = {e}')
    return payload


def decrypt_jwe(jwe_token):
    jwt_token = ''
    try:
        jwt_token = jwe.decrypt(jwe_token, key=Config.ENCRYPT_SECRET)
    except Exception:
        logger.warning('[AUTH] Decrypt failed')
    return jwt_token


async def authorize_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, Config.TOKEN_SECRET, algorithms=TOKEN_ALGORITHM)
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")
        email: str = payload.get("email")
        if user_id is None or user_role is None:
            raise credentials_exception
    except jwt.exceptions.ExpiredSignatureError:
        raise credentials_exception
    except jwt.exceptions.InvalidTokenError:
        raise credentials_exception
    return {"user_id": user_id, 'email':email}