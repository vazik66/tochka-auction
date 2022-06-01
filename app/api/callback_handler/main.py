from fastapi import Depends, Request
from fastapi import FastAPI
from app.core.security import create_nowpayments_hmac
from app.core.config import settings
from app import schemas, crud
from app.api import deps
from sqlalchemy.orm import Session


handler = FastAPI(title="payment_callback_handler")


@handler.post("/callback")
async def handle_callback(request: Request, db: Session = Depends(deps.get_db)) -> None:
    """
    Receives callback about invoice. Chacks callback validity.
    If callback status is finished (funds transferred to merchant wallet)
    changes order status to "DONE".
    """
    # Check signature exists
    request_body = await request.json()
    request_signature = request.headers.get("x-nowpayments-sig")
    if not request_signature:
        return

    # Create own signature and compare to given signature
    created_signature = create_nowpayments_hmac(request_body, settings.PAYMENT_IPN_KEY)
    if not created_signature == request_signature:
        return

    callback = schemas.NOWPaymentsCallback.parse_obj(request_body)
    order = crud.crud_order.get_by_id(db, callback.order_id)
    if callback.payment_status == "finished":
        order_update = schemas.OrderUpdate(status=schemas.PaymentStatus.DONE)
        _ = crud.crud_order.update(db=db, order=order, order_update=order_update)

    return
