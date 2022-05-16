import fastapi_jsonrpc as jsonrpc
from app.api.deps import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from app.models.user import User

rpc = jsonrpc.Entrypoint("/api/v1/jsonrpc")


@rpc.method()
def health(db: Session = Depends(get_db)):
    db_conn = False
    if db.query(User).first():
        db_conn = True

    return dict(
        db_connection=db_conn,
    )


def ping() -> str:
    return "pong"
