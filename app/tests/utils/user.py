from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string, wrap_to_jsonrpc
from pydantic import EmailStr


def user_authentication_headers(
    client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post("/api/v1/jsonrpc", data=wrap_to_jsonrpc(data, "login_access_token"))
    response = r.json()
    auth_token = response["result"]["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


class random_identity:
    def __init__(self):
        self.email = random_email()
        self.password = random_lower_string()
        self.name = self.email.split("@")[0]


def create_random_user(client: TestClient, db: Session) -> User:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(
        full_name=email.split("@")[0],
        email=EmailStr(email),
        password=password,
        password_confirm=password,
    )
    user = crud.crud_user.create(db, user_in)
    return user


def authentication_token_from_email(
    client: TestClient, email: str, db: Session
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = crud.crud_user.get_by_email(db, email=email)
    if not user:
        user_in_create = UserCreate(
            full_name=email.split("@")[0],
            email=EmailStr(email),
            password=password,
            password_confirm=password,
        )
        user = crud.crud_user.create(db, user_in_create)
    else:
        user_in_update = UserUpdate(password=password)
        user = crud.crud_user.update(db, user, user_in_update)

    return user_authentication_headers(client=client, email=email, password=password)
