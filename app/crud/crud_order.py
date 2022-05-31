import uuid
from typing import Optional
from sqlalchemy.orm import Session
from app import models
from app import schemas


def get_by_id(db: Session, id: str) -> Optional[models.Order]:
    return db.query(models.Order).filter(models.Order.id == id).first()


def get_by_item(db: Session, item_id: str) -> Optional[models.Order]:
    return db.query(models.Order).filter(models.Order.item_id == item_id).first()


def get_multi_by_owner(db: Session, user_id: str) -> list[models.Order]:
    return db.query(models.Order).filter(models.Order.user_id == user_id).all()


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> list[models.Order]:
    return db.query(models.Order).offset(skip).limit(limit).all()


def update(
    db: Session, order: models.Order, order_update: schemas.OrderUpdate
) -> models.Order:
    order.status = order_update.status.value

    db.commit()
    db.refresh(order)
    return order


def create(db: Session, order_in: schemas.OrderCreate) -> models.Order:
    db_order = models.Order(
        id=uuid.uuid4(),
        user_id=order_in.user_id,
        item_id=order_in.item_id,
        amount=order_in.amount,
        status=schemas.PaymentStatus.NEW.value,
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
