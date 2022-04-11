from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app import crud
from app.core.security import verify_password
from app.schemas.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string


def test_create_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(
        full_name=email.split("@")[0],
        email=EmailStr(email),
        password=password,
        password_confirm=password,
    )
    user = crud.crud_user.create(db, user_in)
    assert str(user.email) == email
    assert hasattr(user, "password_hash")


def test_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(
        full_name=email.split("@")[0],
        email=EmailStr(email),
        password=password,
        password_confirm=password,
    )

    user = crud.crud_user.create(db, user_in)
    authenticated_user = crud.crud_user.authenticate(db, email=email, password=password)
    assert authenticated_user
    assert user.email == authenticated_user.email


def test_not_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user = crud.crud_user.authenticate(db, email=email, password=password)
    assert user is None


def test_check_if_user_is_superuser(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(
        full_name=email.split("@")[0],
        email=EmailStr(email),
        password=password,
        password_confirm=password,
    )
    user = crud.crud_user.create(db, user_in)
    crud.crud_user.make_superuser(db, user.id)
    is_superuser = crud.crud_user.is_superuser(db, user.id)
    assert is_superuser is True


def test_get_user(db: Session) -> None:
    password = random_lower_string()
    email = random_email()
    user_in = UserCreate(
        full_name=email.split("@")[0],
        email=EmailStr(email),
        password=password,
        password_confirm=password,
    )
    user = crud.crud_user.create(db, user_in)
    crud.crud_user.make_superuser(db, user.id)
    user_2 = crud.crud_user.get_by_id(db, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


def test_update_user(db: Session) -> None:
    password = random_lower_string()
    email = random_email()
    user_in = UserCreate(
        full_name=email.split("@")[0],
        email=EmailStr(email),
        password=password,
        password_confirm=password,
    )
    user = crud.crud_user.create(db, user_in)
    crud.crud_user.make_superuser(db, user.id)
    new_password = random_lower_string()
    user_in_update = UserUpdate(password=new_password)
    crud.crud_user.update(db, user, user_in_update)
    user_2 = crud.crud_user.get_by_id(db, id=user.id)
    assert user_2
    assert str(user.email) == str(user_2.email)
    assert verify_password(new_password, user_2.password_hash)
