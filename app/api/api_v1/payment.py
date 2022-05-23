# import hashlib

# import fastapi
import uuid
from app.api.api_v1.bids import rpc
from fastapi import Depends
from sqlalchemy.orm import Session
from app.api import deps
from app import schemas, crud
from app.api import errors
import requests
from app.core.config import settings

# import hmac
import json


@rpc.method(tags=["Payment"])
def get_orders(
    db: Session = Depends(deps.get_db),
    current_user_token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> list[schemas.Order]:
    orders = crud.crud_order.get_multi_by_owner(db, current_user_token.sub)
    print(
        orders[0].user_id,
        orders[0].amount,
        orders[0].item_id,
        orders[0].status,
        orders[0].id,
    )
    return orders


@rpc.method(tags=["Payment"])
def get_payment_link(
    order_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user_token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> str:
    order = crud.crud_order.get_by_id(db, str(order_id))
    if not order:
        raise errors.TODOError

    if not current_user_token.sub == str(order.user_id):
        raise errors.NotEnoughPrivileges

    item = crud.crud_item.get_by_id(db, order.item_id)

    data = {
        "price_amount": order.amount,
        "price_currency": "rub",
        "order_id": str(order.id),
        "order_description": item.title,
        # "ipn_callback_url": "URL_CALLBACK",
        # "success_url": "SUCCESS_URL",
        # "cansel_url": "FAILED_PAYMENT_URL"
    }
    headers = {
        "x-api-key": settings.PAYMENT_API_KEY,
        "Content-Type": "application/json",
    }
    resp = requests.post(
        url="https://api.nowpayments.io/v1/invoice",
        data=json.dumps(data),
        headers=headers,
    )
    resp_data = resp.json()
    print(resp_data)
    print(json.dumps(data))

    return resp_data.get("invoice_url")


@rpc.method(tags=["Payment"])
def check_order_status(
    order_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user_token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> dict:
    order = crud.crud_order.get_by_id(db, str(order_id))
    if not order:
        raise errors.TODOError()  # No such order
    if current_user_token.sub != order.user_id:
        raise errors.NotEnoughPrivileges

    return {"status": order.status.name}


# TODO
# @rpc.method(tags=["Payment"])
# def nowpayments_callback(
#     request: fastapi.Request,
#     callback: schemas.nowPaymentsCallback,
#     db: Session = Depends(deps.get_db),
# ):
