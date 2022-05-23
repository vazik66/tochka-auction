from sqlalchemy.orm import Session
from app import crud, schemas
from app.core.config import settings
from pydantic import EmailStr


def init_db(db: Session):
    user = crud.crud_user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            full_name="First SuperUser",
            email=EmailStr(settings.FIRST_SUPERUSER),
            password=settings.FIRST_SUPERUSER_PASSWORD,
            password_confirm=settings.FIRST_SUPERUSER_PASSWORD,
        )
        user = crud.crud_user.create(db, user_in)
        _ = crud.crud_user.make_superuser(db, user.id)
