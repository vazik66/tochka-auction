import uuid

from fastapi import Depends

from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps, errors
from app.api.api_v1.auth import rpc
from pydantic import parse_obj_as


@rpc.method(tags=["User"])
async def signup(
    form_data: schemas.UserCreate, db: Session = Depends(deps.get_db)
) -> schemas.User:
    """
    Creates user
    """

    user = crud.crud_user.get_by_email(db=db, email=str(form_data.email))
    if user:
        raise errors.EmailAlreadyInUse
    if form_data.password != form_data.password_confirm:
        raise errors.PasswordsDoNotMatch
    user = crud.crud_user.create(db, user_in=form_data)
    return user


@rpc.method(tags=["User"])
async def get_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    _: str = Depends(deps.get_current_superuser),
) -> list[schemas.User]:
    """
    Gets users with skip, limit params.
    Superuser method.
    """

    users = crud.crud_user.get_multi(db, skip=skip, limit=limit)
    return parse_obj_as(list[schemas.User], users)


@rpc.method(tags=["User"])
async def update_user(
    user_in: schemas.UserUpdate,
    db: Session = Depends(deps.get_db),
    current_user_token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> schemas.User:
    """
    Updates user data.
    """

    if user_in.email:
        if crud.crud_user.get_by_email(db, str(user_in.email)):
            raise errors.EmailAlreadyInUse

    user = crud.crud_user.get_by_id(db, current_user_token.sub)
    if not user:
        raise errors.UserNotFound
    updated_user = crud.crud_user.update(db, user=user, user_update=user_in)
    return schemas.User.from_orm(updated_user)


@rpc.method(tags=["User"])
async def get_current_user_data(
    db: Session = Depends(deps.get_db),
    current_user_token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> schemas.User:
    """
    Get current user data.
    """

    user = crud.crud_user.get_by_id(db, current_user_token.sub)
    if not user:
        raise errors.UserNotFound
    return user


@rpc.method(tags=["User"])
async def get_user_by_id(
    user_id: uuid.UUID,
    current_user_token: schemas.TokenPayload = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> schemas.User:
    """
    Get user by id.
    User can only get his data.
    Superuser can get any data.
    """

    user = crud.crud_user.get_by_id(db, id=str(user_id))
    if not user:
        raise errors.UserNotFound
    if user.id == current_user_token.sub or current_user_token.is_superuser:
        return schemas.User.from_orm(user)
    raise errors.NotEnoughPrivileges
