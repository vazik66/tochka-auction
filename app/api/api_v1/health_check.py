import fastapi_jsonrpc as jsonrpc
from app.api.deps import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.utils.logger import logging_middleware


rpc = jsonrpc.Entrypoint("/api/v1/jsonrpc", middlewares=[logging_middleware])


@rpc.method(tags=["Health"])
def health(db: Session = Depends(get_db)) -> schemas.HealthCheck:
    """
    Checks full api health
    """
    db_conn = False
    if db.query(models.User).first():
        db_conn = True

    return schemas.HealthCheck(db_connection=db_conn)


@rpc.method(tags=["Health"])
def ping() -> str:
    """
    Simple health check
    """
    return "pong"
