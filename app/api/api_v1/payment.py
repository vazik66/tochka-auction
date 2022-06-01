import uuid
from app.api.api_v1.bids import rpc
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from app.api import deps
from app import schemas, crud
from app.api import errors
import requests
from app.core.config import settings

import json

from app.core.security import create_nowpayments_hmac


@rpc.method(tags=["Payment"])
def get_orders(
    db: Session = Depends(deps.get_db),
    current_user_token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> list[schemas.Order]:
    """
    Returns current user orders
    """
    orders = crud.crud_order.get_multi_by_owner(db, current_user_token.sub)

    return orders


@rpc.method(tags=["Payment"])
def get_payment_link(
    order_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user_token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> str:
    """
    Returns url to pay the invoice
    """
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
        "ipn_callback_url": "https://api.milf-tochka.ru/payment/callback",
        "success_url": "https://app.milf-tochka.ru/payment/success",
        "cancel_url": "https://app.milf-tochka.ru/payment/error",
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
    return resp_data.get("invoice_url")


@rpc.method(tags=["Payment"])
def check_order_status(
    order_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user_token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> dict:
    """
    Returns order payment status
    """
    order = crud.crud_order.get_by_id(db, str(order_id))
    if not order:
        raise errors.TODOError()  # No such order
    if current_user_token.sub != order.user_id:
        raise errors.NotEnoughPrivileges

    return {"status": order.status.name}  # noqa


@rpc.method(tags=["Payment"])
async def nowpayments_callback(
    request: Request,
    callback: schemas.NOWPaymentsCallback,
    db: Session = Depends(deps.get_db),
):
    """
    Receives callback when invoice gets paid.
    If callback status is finished (funds transferred to merchant wallet)
    changes order status to "DONE".
    """
    request_body = await request.json()
    request_signature = request.headers.get("x-nowpayments-sig")
    if not request_signature:
        return

    created_signature = create_nowpayments_hmac(request_body, settings.PAYMENT_IPN_KEY)
    if not created_signature == request_signature:
        return

    order = crud.crud_order.get_by_id(db, callback.order_id)
    if callback.payment_status == "finished":
        order_update = schemas.OrderUpdate(status=schemas.PaymentStatus.DONE)
        _ = crud.crud_order.update(db=db, order=order, order_update=order_update)
