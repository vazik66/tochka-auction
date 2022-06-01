import fastapi_jsonrpc as jsonrpc
import requests

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
    # Check database connection
    db_conn = False
    try:
        if db.query(models.User).first():
            db_conn = True
    except Exception:
        pass

    # Check payment status
    payment_api_working = False
    resp = requests.get(
        url="https://api.nowpayments.io/v1/status",
    )
    data = resp.json()
    if data.get("message") == "ok":
        payment_api_working = True

    return schemas.HealthCheck(
        db_connection=db_conn, payment_api_working=payment_api_working
    )


@rpc.method(tags=["Health"])
def ping() -> str:
    """
    Simple health check
    """
    return "pong"
