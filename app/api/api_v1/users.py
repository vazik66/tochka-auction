import uuid

from fastapi import Depends

from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps, errors
from app.api.api_v1.auth import rpc
from pydantic import parse_obj_as


@rpc.method()
def signup(
    form_data: schemas.user.UserCreate, db: Session = Depends(deps.get_db)
) -> schemas.user.User:
    """
    {
        "jsonrpc":"2.0",
        "id":0,
        "method":"signup",
        "params":{
            "form_data":{
                "email":"user@example.com",
                "full_name":"string",
                "password":"string",
                "password_confirm":"string"
            }
        }
    }
    """

    user = crud.crud_user.get_by_email(db=db, email=str(form_data.email))
    if user:
        raise errors.EmailAlreadyInUse
    if form_data.password != form_data.password_confirm:
        raise errors.PasswordsDoNotMatch
    user = crud.crud_user.create(db, user_in=form_data)
    return user


@rpc.method()
def get_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    _: str = Depends(deps.get_current_superuser),
) -> list[schemas.User]:
    """
    Get users from db

    Example:
    {
        "jsonrpc":"2.0",
        "id":0,
        "method":"get_users",
        "params":{
            "skip":0,
            "limit":100
        }
    }
    """
    users = crud.crud_user.get_multi(db, skip=skip, limit=limit)

    return parse_obj_as(list[schemas.User], users)


@rpc.method()
def update_user(
    user_in: schemas.UserUpdate,
    db: Session = Depends(deps.get_db),
    current_user_token: schemas.token.TokenPayload = Depends(deps.get_current_user),
) -> schemas.User:
    """
    Update own user.

    Example:
    {
        "jsonrpc":"2.0",
        "id":0,
        "method":"update_user",
        "params":{
            "user_in": {
                "password":"string",
                "full_name":"string",
                "email":"user@example.com"
            }
        }
    }
    """

    if crud.crud_user.get_by_email(db, str(user_in.email)):
        raise errors.EmailAlreadyInUse

    user = crud.crud_user.get_by_id(db, current_user_token.sub)
    updated_user = crud.crud_user.update(db, user=user, user_update=user_in)
    return schemas.User.from_orm(updated_user)


@rpc.method()
def get_current_user_data(
    db: Session = Depends(deps.get_db),
    current_user_token: schemas.token.TokenPayload = Depends(deps.get_current_user),
) -> schemas.User:
    """
    Get current user data.

    Example:
    {
        "jsonrpc":"2.0",
        "id":0,
        "method":"get_current_user_data",
        "params":{}
    }
    """
    user = crud.crud_user.get_by_id(db, current_user_token.sub)
    return schemas.User.from_orm(user)


@rpc.method()
def get_user_by_id(
    user_id: uuid.UUID,
    current_user_token: schemas.token.TokenPayload = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> schemas.User:
    """
    Get a specific user by id.

    Example:
    {
      "jsonrpc": "2.0",
      "id": 0,
      "method": "get_user_by_id",
      "params": {
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
      }
    }
    """
    user = crud.crud_user.get_by_id(db, id=str(user_id))

    if user.id == current_user_token.sub or current_user_token.is_superuser:
        return schemas.User.from_orm(user)
    raise errors.NotEnoughPrivileges
