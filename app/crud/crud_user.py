from sqlalchemy.orm import Session
import uuid
from typing import Optional
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserInDB


def get_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_by_id(db: Session, id: str) -> Optional[User]:
    return db.query(User).get(id)


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def update(db: Session, user: User, user_update: UserUpdate) -> User:
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


def create(db: Session, user_in: UserCreate) -> User:
    db_user = User(
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


def authenticate(db: Session, email: str, password: str) -> Optional[User]:
    user = get_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def is_superuser(db: Session, id: Optional[str]) -> bool:
    return get_by_id(db, id).is_superuser


def make_superuser(db: Session, id: Optional[str]) -> Optional[User]:
    user = get_by_id(db, id)
    user.is_superuser = True
    db.commit()
    db.refresh(user)
    return user
