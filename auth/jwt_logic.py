from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Union, Any
from jose import jwt
from auth.JwtKeys import JwtKeys


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=JwtKeys.ACCESS_TOKEN_LIFE_TIME)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode,
        JwtKeys.ACCESS_TOKEN_KEY,
        JwtKeys.ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=JwtKeys.REFRESH_TOKEN_LIFE_TIME)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode,
        JwtKeys.REFRESH_TOKEN_KEY,
        JwtKeys.ALGORITHM)
    return encoded_jwt


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)
