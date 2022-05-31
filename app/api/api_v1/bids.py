import datetime
import uuid

from app.api.api_v1.items import rpc

from fastapi import Depends

from sqlalchemy.orm import Session
from app import schemas
from app import crud
from app.api import deps, errors

import base64
from io import BytesIO


BID_SNIPING_ADD_MINUTES = 0
BID_SNIPING_CHECK_BEFORE_MINUTES = 0


@rpc.method(tags=["Bid"])
def place_bid(
    bid_in: schemas.BidCreate,
    db: Session = Depends(deps.get_db),
    current_user_token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> schemas.Bid:
    item = crud.crud_item.get_by_id(db, str(bid_in.item_id))
    if not item:
        raise errors.ItemNotFound

    if item.is_ended or item.is_archived:
        raise errors.AuctionHasEnded

    if item.end_date < datetime.datetime.now(tz=datetime.timezone.utc):
        crud.crud_item.end_auction(db, item.id)
        raise errors.AuctionHasEnded

    if str(item.owner_id) == current_user_token.sub:
        raise errors.OwnerCanNotBid

    if len(item.bids) > 0 and bid_in.amount <= item.bids[-1].amount:
        raise errors.InvalidAmount

    if len(item.bids) == 0 and item.min_bid > bid_in.amount:
        raise errors.InvalidAmount

    # Check if bid is greater than minimum bid step
    if len(item.bids) > 0:
        if bid_in.amount - item.bids[-1].amount < item.min_bid_step:
            raise errors.BidIsSmallerThanMinBidStep

    # Add time if slot is about to end and there are people bidding
    if item.end_date - datetime.datetime.now(
        tz=datetime.timezone.utc
    ) <= datetime.timedelta(minutes=BID_SNIPING_CHECK_BEFORE_MINUTES):
        item.end_date += datetime.timedelta(minutes=BID_SNIPING_ADD_MINUTES)

    return crud.crud_bid.create(db, bid_in, current_user_token.sub)


@rpc.method(tags=["Bid"])
def get_bids_by_item(
    item_id: str, db: Session = Depends(deps.get_db)
) -> list[schemas.Bid]:
    item = crud.crud_item.get_by_id(db, item_id)
    if not item:
        raise errors.ItemNotFound
    return item.bids


@rpc.method(tags=["Bid"])
def get_bids_by_owner(
    db: Session = Depends(deps.get_db),
    current_user_token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> list[schemas.Bid]:

    return crud.crud_bid.get_bids_by_owner(db, current_user_token.sub)


@rpc.method(tags=["Bid"])
def test_qrcode(item_id: str, db: Session = Depends(deps.get_db)) -> bytes:
    item = crud.crud_item.get_by_id(db, item_id)
    import app.schemas.order as payment

    # If not item.winner: winner is not chosen yet

    invoice = payment.Invoice(
        id=uuid.uuid4(), item=item, amount=item.bids[-1].amount, status=False
    )
    invoice._convert_currency()

    qrcode = invoice.get_qr_code()
    buffered = BytesIO()
    qrcode.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue())

    return img_base64
