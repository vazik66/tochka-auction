import datetime
import uuid
from typing import Optional
from pydantic import BaseModel


class ItemCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: int
    images: Optional[list[str]] = None


class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None


class ItemInDBBase(BaseModel):
    id: uuid.UUID
    owner_id: uuid.UUID
    title: str
    description: str
    price: int
    is_archived: bool
    is_moderating: bool
    created_at: datetime.datetime
    images: list[str]

    class Config:
        orm_mode = True


# Public Scheme to return to user
class Item(ItemInDBBase):
    pass


# Actual database scheme
class ItemInDB(ItemInDBBase):
    pass
