import datetime
import typing

from pydantic import BaseModel


# TODO
class nowPaymentsCallback(BaseModel):
    payment_id: int
    payment_status: str
    pay_address: str
    price_amount: int
    price_currency: str
    pay_amount: float
    actually_paid: float
    pay_currency: str
    order_id: str
    order_description: str
    purchase_id: typing.Any
    created_at: datetime.datetime
    updated_at: datetime.datetime
    outcome_amount: float
    outcome_currency: str
