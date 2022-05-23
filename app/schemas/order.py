from pydantic import BaseModel
import uuid
import enum


class PaymentStatus(enum.Enum):
    NEW = 0
    PENDING = 1
    DONE = 2
    ERROR = -1


class OrderBase(BaseModel):
    user_id: uuid.UUID
    item_id: uuid.UUID
    amount: int

    class Config:
        orm_mode = True


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: uuid.UUID
    status: int


class OrderUpdate(BaseModel):
    status: PaymentStatus
