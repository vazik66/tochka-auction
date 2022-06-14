import datetime
import uuid
from pydantic import BaseModel, validator
from app.schemas.user import User


class BidCreate(BaseModel):
    item_id: uuid.UUID
    amount: int

    @validator("amount")
    def amount_must_be_smaller(cls, v):
        if v > 100000000:
            raise ValueError("Amount must be smaller then 100000000")
        return v


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
