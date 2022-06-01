from pydantic import validate_email
from fastapi import Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api import errors
from app import crud, schemas
from app.api import deps
from app.core import security
from app.api.api_v1.health_check import rpc
from app.core.config import settings


@rpc.method(tags=["Authorization"])
def login(
    response: Response,
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> schemas.Token:
    """
    Returns response with access-token cookie
    if username and password are correct
    """
    try:
        form_data.username = validate_email(form_data.username)[1].lower()
    except Exception:
        raise errors.EmailNotValid

    user = crud.crud_user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise errors.IncorrectEmailOrPassword

    token = schemas.Token(
        access_token=security.create_access_token(
            str(user.id), user.is_superuser, user.full_name
        ),
        token_type="Bearer",
    )
    response.set_cookie(
        "access-token", value=str(token), domain=settings.DOMAIN, secure=True
    )
    return token


@rpc.method(tags=["Authorization"])
def logout(response: Response) -> None:
    """
    Returns response with delete cookie action
    """
    response.delete_cookie("access-token", domain=settings.DOMAIN, secure=True)
