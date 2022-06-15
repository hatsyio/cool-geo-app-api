import datetime

from pydantic import BaseModel


class PostalCode(BaseModel):
    code: str
    the_geom: str


class PaymentAggregation(BaseModel):
    amount: float
    p_gender: str | None
    p_age: str | None
    code: str | None
    p_month: datetime.date | None


class Geometry(BaseModel):
    the_geom: str
    the_geom_as_text: str
