import datetime
import uuid
from pydantic import BaseModel
from app.schemas.user import User


class BidCreate(BaseModel):
    item_id: uuid.UUID
    amount: int


class BidInDBBase(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    item_id: uuid.UUID
    amount: int
    created_at: datetime.datetime
    user: User

    class Config:
        orm_mode = True


# Public Scheme to return to user
class Bid(BidInDBBase):
    pass

    class Config:
        fields = {"user": {"exclude": {"id", "email"}}}
