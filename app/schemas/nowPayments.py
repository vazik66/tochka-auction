import typing

from pydantic import BaseModel


class NOWPaymentsCallback(BaseModel):
    payment_id: int
    invoice_id: int
    payment_status: str
    pay_address: str
    price_amount: typing.Union[int, float]
    price_currency: str
    pay_amount: typing.Union[int, float]
    actually_paid: typing.Union[int, float]
    pay_currency: typing.Any
    order_id: str
    order_description: str
    purchase_id: str
    created_at: str
    updated_at: str
    outcome_amount: typing.Union[int, float]
    outcome_currency: str
