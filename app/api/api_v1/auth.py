import fastapi_jsonrpc as jsonrpc

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api import errors
from app import crud, schemas
from app.api import deps
from app.core import security

rpc = jsonrpc.Entrypoint("/api/v1/jsonrpc")


@rpc.method()
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
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

    user = crud.crud_user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise errors.IncorrectEmailOrPassword

    return schemas.Token(
        access_token=security.create_access_token(user.id), token_type="Bearer"
    )
