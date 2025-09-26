import logging
import uuid
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

from src.config import Config

passwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated='auto'
)


def generate_password_hash(password: str) -> str:
    hash = passwd_context.hash(password.encode('utf8'))
    return hash


def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)


def create_jwt_token(user_data: dict, expiry: timedelta = None, refresh: bool = False) -> str:
    payload = {
        'user': user_data,
        'exp': datetime.now() + (expiry if expiry is not None else timedelta(minutes=60)),
        'jti': str(uuid.uuid4()),
        'refresh': refresh,
    }
    token = jwt.encode(
        payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM
    )
    return token


def decode_jwt_token(token: str) -> dict:
    try:        
        token_data = jwt.decode(jwt=token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
        return token_data
    except jwt.PyJWTError as jwte:
        logging.exception(jwte)
        return None
    except Exception as e:
        logging.exception(e)
        return None
