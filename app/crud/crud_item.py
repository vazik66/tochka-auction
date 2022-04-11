import uuid
from typing import List, Optional

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


def create(db: Session, item_in: ItemCreate, owner: User) -> Item:
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


def delete(db: Session, id: str):
    item = get_by_id(db, id)
    db.delete(item)
    db.commit()
