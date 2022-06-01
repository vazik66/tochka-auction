import hashlib
import hmac
import json
from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any],
    is_superuser: Union[bool, Any],
    name: str,
    expires_delta: timedelta = None,
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {
        "exp": expire,
        "sub": subject,
        "is_superuser": is_superuser,
        "name": name,
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_nowpayments_hmac(data: dict, key: str) -> str:
    sorted_data = json.dumps(
        dict(sorted(data.items())), indent=None, separators=(",", ":")
    )
    signature = create_hmac(sorted_data, key, hashlib.sha512)
    return signature


def create_hmac(data: str, key: str, digestmod: hashlib) -> str:
    encoded_message = bytes(data, "utf-8")
    signature = hmac.new(
        key=bytes(key, "utf-8"), msg=encoded_message, digestmod=digestmod
    ).hexdigest()
    return signature
