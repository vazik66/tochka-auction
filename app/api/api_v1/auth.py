import fastapi_jsonrpc as jsonrpc
from pydantic import validate_email
from fastapi import Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api import errors
from app import crud, schemas
from app.api import deps
from app.core import security

rpc = jsonrpc.Entrypoint("/api/v1/jsonrpc")


@rpc.method()
def login_access_token(
    response: Response,
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> schemas.Token:
    """
    {
        "jsonrpc":"2.0",
        "id":0,
        "method":"login_access_token",
        "params":{
            "username":"string",
            "password":"string",
        }
    }
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
        access_token=security.create_access_token(user.id), token_type="Bearer"
    )
    response.set_cookie("access-token", str(token))
    return token


@rpc.method()
def logout(response: Response) -> None:
    response.delete_cookie("access-token")
