import datetime
import typing
import uuid
from typing import Optional
from pydantic import BaseModel
from app.schemas.bid import Bid


class ItemCreate(BaseModel):
    title: str
    description: Optional[str] = None
    min_bid: int
    min_bid_step: Optional[int] = None
    end_date: float
    images: Optional[list[str]] = None


class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    min_bid: Optional[int] = None
    min_bid_step: Optional[int] = None
    end_date: Optional[float] = None


class ItemInDBBase(BaseModel):
    id: uuid.UUID
    owner_id: uuid.UUID
    title: str
    description: str
    min_bid: int
    min_bid_step: int
    is_archived: bool
    is_ended: bool
    created_at: datetime.datetime
    end_date: datetime.datetime
    images: list[str]
    bids: list[Bid]
    winner: Optional[uuid.UUID] = None

    class Config:
        orm_mode = True


# Public Scheme to return to user
class Item(ItemInDBBase):
    pass


# Actual database scheme
class ItemInDB(ItemInDBBase):
    pass


class ListItem(BaseModel):
    __root__: typing.List[Item]
