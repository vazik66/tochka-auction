from sqlalchemy.orm import Session
import uuid
from typing import Optional
from app.core.security import get_password_hash, verify_password
from app import models
from app import schemas


def get_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def get_by_id(db: Session, id: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == id).first()


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def update(
    db: Session, user: models.User, user_update: schemas.UserUpdate
) -> models.User:
    for attr, value in user_update.__dict__.items():
        if value is None:
            continue
        if attr == "password":
            user.__setattr__("password_hash", get_password_hash(value))
            continue
        user.__setattr__(attr, value)

    db.commit()
    db.refresh(user)
    return user


def create(db: Session, user_in: schemas.UserCreate) -> models.User:
    db_user = models.User(
        id=uuid.uuid4(),
        email=str(user_in.email),
        full_name=user_in.full_name,
        password_hash=get_password_hash(user_in.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete(db: Session, id: str):
    user = get_by_id(db, id)
    db.delete(user)
    db.commit()


def authenticate(db: Session, email: str, password: str) -> Optional[models.User]:
    user = get_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def make_superuser(db: Session, id: str) -> Optional[models.User]:
    user = get_by_id(db, id)
    user.is_superuser = True
    db.commit()
    db.refresh(user)
    return user
