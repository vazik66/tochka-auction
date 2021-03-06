from typing import Generator

from botocore.client import BaseClient

from app.api import errors
from fastapi import Depends
from jose import jwt
from pydantic import ValidationError
import boto3
from app import models, schemas
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal
from app.core.OAuth2CookieAuth import OAuth2PasswordBearerCookie
from app.crud import crud_user
from sqlalchemy.orm import Session

reusable_oauth2 = OAuth2PasswordBearerCookie(tokenUrl="api/v1/jsonrpc/login")


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(reusable_oauth2), db: Session = Depends(get_db)
) -> schemas.TokenPayload:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise errors.BadCredentials
    user = crud_user.get_by_id(db, token_data.sub)
    if not user:
        raise errors.BadCredentials
    return token_data


def get_current_superuser(
    current_user: models.User = Depends(get_current_user),
) -> str:
    if not current_user.is_superuser:
        raise errors.NotEnoughPrivileges
    return str(current_user.sub)


def get_s3_client() -> BaseClient:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
    )
    yield s3_client
