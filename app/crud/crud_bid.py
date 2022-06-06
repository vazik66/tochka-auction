import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from app import models
from app import schemas


def get_by_id(db: Session, id: str) -> Optional[schemas.Bid]:
    return db.query(models.Bid).filter(models.Bid.id == id).first()


def get_bids_by_owner(
    db: Session,
    owner_id: str,
) -> List[models.Bid]:
    bids: list[models.Bid] = (
        db.query(models.Bid).filter(models.Bid.user_id == owner_id).all()
    )

    result = []
    item_ids = set()
    for bid in bids:
        item_ids.add(bid.item_id)
    for item_id in item_ids:
        maximum_bid = 0
        for bid in bids:
            if not bid.item_id == item_id:
                continue
            if type(maximum_bid) is int:
                if bid.amount > maximum_bid:
                    maximum_bid = bid
            elif bid.amount > maximum_bid.amount:
                maximum_bid = bid
        result.append(maximum_bid)
    return result


def create(db: Session, bid_in: schemas.BidCreate, user_id: str) -> schemas.Bid:
    db_bid = models.Bid(
        id=uuid.uuid4(),
        user_id=uuid.UUID(user_id),
        item_id=bid_in.item_id,
        amount=bid_in.amount,
    )

    db.add(db_bid)
    db.commit()
    db.refresh(db_bid)
    return db_bid


def delete(db: Session, id: str):
    db_bid = get_by_id(db, id)
    db.delete(db_bid)
    db.commit()
