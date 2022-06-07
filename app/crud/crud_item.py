import base64
import datetime
import uuid
from typing import List, Optional

from app.core.config import settings
from sqlalchemy.orm import Session
from app import models
from app import schemas
from app.crud import crud_bid, crud_order


def get_by_id(db: Session, id: str) -> Optional[models.Item]:
    return db.query(models.Item).filter(models.Item.id == id).first()


def get_multi_by_owner(db: Session, owner_id: str) -> List[models.Item]:
    return db.query(models.Item).filter(models.Item.owner_id == owner_id).all()


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> list[models.Item]:
    return (
        db.query(models.Item)
        .filter(models.Item.is_ended == False, models.Item.is_archived == False)  # noqa
        .offset(skip)
        .limit(limit)
        .all()
    )


def update(
    db: Session, item: models.Item, item_update: schemas.ItemUpdate
) -> models.Item:
    for attr, value in item_update.__dict__.items():
        if value is None:
            continue
        if "id" == attr or "owner_id" == attr:
            continue
        if attr == "end_date":
            end_date = datetime.datetime.fromtimestamp(value, datetime.timezone.utc)
            item.__setattr__(attr, end_date)
            continue
        item.__setattr__(attr, value)

    db.commit()
    db.refresh(item)
    return item


def upload_to_s3(s3, images: list[str]):
    image_urls = []
    for image in images:
        if len(image) < 50:
            # IDK how to check if base64 is real image
            continue
        filename = str(uuid.uuid4()) + ".jpg"
        try:
            byte = base64.b64decode(image)
        except Exception:
            raise BaseException("can't decode image")
        s3.put_object(
            Body=byte, Key=f"images/{filename}", Bucket=settings.S3_BUCKET_NAME
        )
        image_urls.append(filename)

    return image_urls


def create(
    db: Session, s3, item_in: schemas.ItemCreate, owner: models.User
) -> models.Item:
    end_date = datetime.datetime.utcfromtimestamp(item_in.end_date)

    db_item = models.Item(
        id=uuid.uuid4(),
        owner_id=owner.id,
        title=item_in.title,
        description=item_in.description,
        min_bid=item_in.min_bid,
        min_bid_step=item_in.min_bid_step,
        end_date=end_date,
    )

    if item_in.images:
        images_url = upload_to_s3(s3, item_in.images)
        db_item.images = images_url

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def end_auction(db: Session, item_id: str) -> models.Item:
    item = get_by_id(db, item_id)
    item.is_ended = True
    if len(item.bids) > 0:
        item.winner = item.bids[-1].user_id
    db.commit()
    db.refresh(item)

    if item.winner:
        order_create = schemas.OrderCreate(
            user_id=item.winner, item_id=item.id, amount=item.bids[-1].amount
        )
        crud_order.create(db, order_create)
    return item


def get_outdated_items(db: Session) -> list[models.Item]:
    return (
        db.query(models.Item)
        .filter(
            models.Item.is_ended == False,  # noqa
            models.Item.is_archived == False,  # noqa
            models.Item.end_date < datetime.datetime.utcnow(),
        )
        .all()
    )


def set_archive(db: Session, item_id: str) -> models.Item:
    item = get_by_id(db, item_id)
    item.is_archived = True
    db.commit()
    db.refresh(item)
    return item


def remove_archive(db: Session, item_id: str) -> models.Item:
    item = get_by_id(db, item_id)
    item.is_archived = False
    db.commit()
    db.refresh(item)
    return item


def delete(db: Session, s3, id: str):
    item = get_by_id(db, id)
    if not item:
        return None
    if item.winner:
        return None
    for image in item.images:
        s3.delete_object(Bucket=settings.S3_BUCKET_NAME, Key=f"images/{image}")
    if item.bids:
        for bid in item.bids:
            crud_bid.delete(db, bid.id)

    db.delete(item)
    db.commit()
