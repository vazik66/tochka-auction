import base64
import uuid
from typing import List, Optional
from app.core.config import settings
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


def get_by_id(db: Session, id: str) -> Optional[Item]:
    return db.query(Item).get(id)


def get_multi_by_owner(
    db: Session, owner_id: uuid.UUID, skip: int = 0, limit: int = 100
) -> List[Item]:
    return (
        db.query(Item).filter(Item.owner_id == owner_id).offset(skip).limit(limit).all()
    )


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> list[Item]:
    return (
        db.query(Item)
        .filter(Item.is_moderating == False, Item.is_archived == False)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update(db: Session, item: Item, item_update: ItemUpdate) -> Item:
    for attr, value in item_update.__dict__.items():
        if value is None:
            continue
        if "id" == attr or "owner_id" == attr:
            continue
        item.__setattr__(attr, value)

    db.commit()
    db.refresh(item)
    return item


def upload_to_s3(s3, images: list[str]):
    image_urls = []
    for image in images:
        filename = str(uuid.uuid4()) + ".jpg"
        byte = base64.b64decode(image)
        _ = s3.put_object(
            Body=byte, Key=f"images/{filename}", Bucket=settings.S3_BUCKET_NAME
        )
        image_urls.append(filename)

    return image_urls


def create(db: Session, s3, item_in: ItemCreate, owner: User) -> Item:
    if item_in.images:
        images_url = upload_to_s3(s3, item_in.images)

        db_item = Item(
            id=uuid.uuid4(),
            owner_id=owner.id,
            title=item_in.title,
            description=item_in.description,
            price=item_in.price,
            images=images_url,
        )
    else:
        db_item = Item(
            id=uuid.uuid4(),
            owner_id=owner.id,
            title=item_in.title,
            description=item_in.description,
            price=item_in.price,
        )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def remove_moderate(db: Session, item_id: str) -> Item:
    item = get_by_id(db, item_id)
    item.is_moderating = False
    db.commit()
    db.refresh(item)
    return item


def set_moderate(db: Session, item_id: str) -> Item:
    item = get_by_id(db, item_id)
    item.is_moderating = True
    db.commit()
    db.refresh(item)
    return item


def set_archive(db: Session, item_id: str) -> Item:
    item = get_by_id(db, item_id)
    item.is_archived = True
    db.commit()
    db.refresh(item)
    return item


def remove_archive(db: Session, item_id: str) -> Item:
    item = get_by_id(db, item_id)
    item.is_archived = False
    db.commit()
    db.refresh(item)
    return item


def delete(db: Session, s3, id: str):
    item = get_by_id(db, id)
    for image in item.images:
        s3.delete_object(Bucket=settings.S3_BUCKET_NAME, Key=f"images/{image}")

    db.delete(item)
    db.commit()
